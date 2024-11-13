from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
import json

router_protected = APIRouter()

api_key_header = APIKeyHeader(name="Dama-API-Key")

with open("api_keys.json") as read_file:
    api_keys = json.load(read_file)

print(api_keys)
def get_api_key(api_key_header:str = Security(api_key_header)) -> bool:
    if api_key_header in api_keys:
        return api_keys[api_key_header]
    else:    
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
@router_protected.get("/protected-endpoint")
def protected_endpoint(api_key: str = Security(get_api_key)):
    with open("data_tasks.json") as read_file:
            data_tasks = json.load(read_file)
        
    response = []
    for task in data_tasks:
        for task_key, task_value in task.items():
            # print(f"task_key: {task_key}, task_value: {task_value}, api_key: {api_key}")
            # Check if the task key starts with the API key prefix
            if task_key.startswith(api_key):
                response.append(task_value)
    return response