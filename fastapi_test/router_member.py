from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import json

class BaseMember(BaseModel):
    id: Optional[str] = None 
    name: str
    team: str
    
router_member = APIRouter()

with open("data_team.json") as read_file:
    data_team = json.load(read_file)
    
@router_member.get("/team_members", summary="Get information about all team members")
async def getAllTeamMembers() -> list:
    return data_team

@router_member.get("/team_member/{id}", summary="Get information about certain team members")
async def getTeamMemberById(id: str) -> dict:
    id = id
    for data in data_team:
        if data["id"] == id:
            return data
    return {"message": f"member dengan id {id} tidak ditemukan"}
    
@router_member.post("/update_member/{id}", summary="Update certain member information by id")
async def rename(id: str, member: BaseMember) -> dict:
    # id = member.id
    name_baru = member.name
    team_baru = member.team


    renamed = False
    relocation = False
    # Update the data in memory
    for data in data_team:
        if data["id"] == id:
            if name_baru != "sama":
                data["name"] = name_baru
                renamed = True
            if team_baru != "sama":
                data["team"] = team_baru
                relocation = True
            break
    
    response_message = f"member dengan id {id}"
    if renamed:
        response_message += f" namenya menjadi {name_baru}"
    if relocation:
        response_message += f" teamnya menjadi {team_baru}"
    # Write the updated data back to the JSON file
    with open("data_team.json", "w") as write_file:
        json.dump(data_team, write_file, indent=4)  # Add indentation for readability

    return {"message": response_message}