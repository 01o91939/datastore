from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Store Services")

# In-memory data store
data_store = {}
value_counts = {}

# Models for requests
class KeyValueRequest(BaseModel):
    namespace: str
    key: str
    value: str

class NamespaceKeyRequest(BaseModel):
    namespace: str
    key: str

# Helper methods
def update_value_counts(namespace, key, value, operation):
    """
    Update the value count based on operation.
    """
    if operation=="set":
        if namespace in data_store and key in data_store[namespace]:
            old_value = data_store[namespace][key]
            if value_counts[namespace].get(old_value, 0) > 0:
                value_counts[namespace][old_value] -= 1
        data_store.setdefault(namespace, {})[key] = value
        value_counts.setdefault(namespace, {})
        value_counts[namespace][value] = value_counts[namespace].get(value, 0) + 1
    elif operation == "delete":
        if namespace in data_store and key in data_store[namespace]:
            old_value = data_store[namespace].pop(key)
            if value_counts[namespace].get(old_value, 0) > 0:
                value_counts[namespace][old_value] -= 1
            if not data_store[namespace]:
                del data_store[namespace]

# API Endpoints
@app.post("/set")
def set_key_value(request: KeyValueRequest):
    """
    """
    logger.info(f"Setting value: {request.namespace}:{request.key} -> {request.value}")
    update_value_counts(request.namespace, request.key, request.value, "set")
    return {"message": "Value set successfully"}

@app.get("/get")
def get_key_value(namespace:str, key:str):
    """
    """
    logger.info(f"Getting value: {namespace}:{key}")
    if namespace in data_store and key in data_store[namespace]:
        return {"value": data_store[namespace][key]}
    raise HTTPException(status_code=404, detail="Key not found")

@app.delete("/delete")
def delete_key_value(namespace:str, key: str):
    """
    """
    logger.info(f"Deleting key: {namespace}:{key}")
    if namespace in data_store and key in data_store[namespace]:
        update_value_counts(namespace, key, None, "delete")
        return {"message": "Key deleted successfully"}
    raise HTTPException(status_code=404, detail="Key not found")

@app.get("/count")
def count_value(namespace:str, value:str):
    """
    """
    logger.info(f"Counting values in namespace {namespace}: {value}")
    if namespace in value_counts:
        return {"count": value_counts[namespace].get(value, 0)}
    return {"count": 0}

@app.get("/countGlobal")
def count_global(value: str):
    """
    """
    logger.info(f"Counting global value {value}")
    global_count = 0
    for namespace_counts in value_counts.values():
        global_count += namespace_counts.get(value, 0)
    return {"global_count": global_count}
