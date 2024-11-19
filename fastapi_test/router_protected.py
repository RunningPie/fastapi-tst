from fastapi import APIRouter, HTTPException, Security
from fastapi.security import APIKeyHeader
import json
import secrets
from datetime import *

router_protected = APIRouter()

api_key_header = APIKeyHeader(name="X-API-Key")
user_keys = {}


@router_protected.get("/get-api-key/{username}")
def key_request(username: str) -> dict:
    global user_keys
    with open("user_keys.json") as read_file:
        user_keys = json.load(read_file)
    with open("data_tasks.json") as read_file:
        data_tasks = json.load(read_file)
    
    try:
        key_expire = datetime.strptime(user_keys[username]["expire_timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    except KeyError:
        user_keys[username] = {"key": secrets.token_hex(16), "expire_timestamp": (datetime.now() + timedelta(minutes=100)).strftime("%Y-%m-%d %H:%M:%S.%f")}
        data_tasks[username] = ["default_new_task"]
    finally:
        key_expire = datetime.strptime(user_keys[username]["expire_timestamp"], "%Y-%m-%d %H:%M:%S.%f")
    print(key_expire, datetime.now())
    if  key_expire < datetime.now():
        user_keys[username]["key"] = secrets.token_hex(16)
        user_keys[username]["expire_timestamp"] = (datetime.now() + timedelta(minutes=100)).strftime("%Y-%m-%d %H:%M:%S.%f")
    
    with open("user_keys.json", "w") as write_file:
        json.dump(user_keys, write_file, indent=4)
    with open("data_tasks.json", "w") as write_file:
        json.dump(data_tasks, write_file, indent=4)
        
    return {"api_key": user_keys[username]["key"], "expires": user_keys[username]["expire_timestamp"]}

def get_api_key(username: str, request_header_key:dict = Security(api_key_header)) -> dict:
    global user_keys
    print(request_header_key, user_keys)
    try:
        if request_header_key == user_keys[username]["key"]:
            return {"user": "found", "key": "valid"}
        else:    
            raise HTTPException(status_code=401, detail="Invalid API Key")
    except KeyError:
        raise HTTPException(status_code=401, detail="User not found")
    
@router_protected.get("/protected-endpoint/{username}")
def protected_endpoint(
    username: str,
    valid: dict = Security(get_api_key)
    ):
    if valid:
        with open("data_tasks.json") as read_file:
                data_tasks = json.load(read_file)

        return data_tasks[username]