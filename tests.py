import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.mark.asyncio
async def test_scenario_1():
     with TestClient(app) as client:
        # 1. /set namespace = "a" key = "b" value = "c"
        response = client.post("/set", json={"namespace": "a", "key": "b", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"message": "Value set successfully"}

        # 2. /set namespace = "z" key = "b" value = "d"
        response = client.post("/set", json={"namespace": "z", "key": "b", "value": "d"})
        assert response.status_code == 200
        assert response.json() == {"message": "Value set successfully"}

        # 3. /get namespace = "a" key = "b" 
        response = client.get("/get", params={"namespace": "a", "key": "b"})
        assert response.status_code == 200
        assert response.json() == {"value": "c"}

        # 4. /get namespace = "z" key = "b" 
        response = client.get("/get", params={"namespace": "z", "key": "b"})
        assert response.status_code == 200
        assert response.json() == {"value": "d"}

        # 5. /delete namespace="a" key="b"
        response = client.delete("/delete", params={"namespace": "a", "key": "b"})
        assert response.status_code == 200
        assert response.json() == {"message": "Key deleted successfully"}

        # 4. /get namespace = "a" key = "b" 
        response = client.get("/get", params={"namespace": "a", "key": "b"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Key not found"}

@pytest.mark.asyncio
async def test_scenario_2():
     with TestClient(app) as client:
        # 1. /set namespace = "a" key = "b" value = "c"
        response = client.post("/set", json={"namespace": "a", "key": "b", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"message": "Value set successfully"}

        # 2. /set namespace = "z" key = "b" value = "c"
        response = client.post("/set", json={"namespace": "z", "key": "b", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"message": "Value set successfully"}

        # 3. /set namespace = "z" key = "bb" value = "d"
        response = client.post("/set", json={"namespace": "z", "key": "bb", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"message": "Value set successfully"}

        # 4. /count namespace = "a" value = "c"
        response = client.get("/count", params={"namespace": "a", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"count": 1}

        # 5. /count namespace = "z" value = "c"
        response = client.get("/count", params={"namespace": "z", "value": "c"})
        assert response.status_code == 200
        assert response.json() == {"count": 2}

        # 6. /count namespace = "z" value = "c"
        response = client.get("/countGlobal", params={"value": "c"})
        assert response.status_code == 200
        assert response.json() == {"global_count": 3}

@pytest.mark.asyncio
async def test_scenario_3():
     with TestClient(app) as client:
        client.post("/set", json={"namespace": "a", "key": "b", "value": "c"})
        client.post("/set", json={"namespace": "a", "key": "b", "value": "d"})
        response = client.get("/get", params={"namespace": "a", "key": "b"})
        assert response.status_code == 200
        assert response.json() == {"value": "d"}

@pytest.mark.asyncio
async def test_edge_cases():
     with TestClient(app) as client:
        # 1. handle long keys and values
        long_key = "k" * 1000
        long_value = "v" * 1000
        client.post("/set", json={"namespace": "long", "key": long_key, "value": long_value})
        response = client.get("/get", params={"namespace": "long", "key": long_key})
        assert response.status_code == 200
        assert response.json() == {"value": long_value}

        # 2. Special characters in keys and values
        special_key = "key@#$%"
        special_value = "val!@#$%"
        client.post("/set", json={"namespace": "special", "key": special_key, "value": special_value})
        response = client.get("/get", params={"namespace": "special", "key": special_key})
        assert response.status_code == 200
        assert response.json() == {"value": special_value}

        # 3. Case sensitivity
        client.post("/set", json={"namespace": "case", "key": "Key", "value": "Value1"})
        client.post("/set", json={"namespace": "case", "key": "key", "value": "Value2"})
        response = client.get("/get", params={"namespace": "case", "key": "Key"})
        assert response.status_code == 200
        assert response.json() == {"value": "Value1"}
        response = client.get("/get", params={"namespace": "case", "key": "key"})
        assert response.status_code == 200
        assert response.json() == {"value": "Value2"}
