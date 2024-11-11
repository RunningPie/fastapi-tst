from fastapi import APIRouter
from pydantic import BaseModel
import json

class BaseMahasiswa(BaseModel):
    nim: str
    nama: str
    asal: str
    
router_mahasiswa = APIRouter()

with open("data_mahasiswa.json") as read_file:
    data_mahasiswa = json.load(read_file)
    
@router_mahasiswa.get("/info_mahasiswa")
async def infomhs(request: dict) -> dict:
    nim = request["nim"]
    for data in data_mahasiswa:
        if data["nim"] == nim:
            res_data = data
    return res_data
    
@router_mahasiswa.post("/update_mahasiswa")
async def rename(mahasiswa: BaseMahasiswa) -> dict:
    nim = mahasiswa.nim
    nama_baru = mahasiswa.nama
    asal_baru = mahasiswa.asal


    renamed = False
    relocation = False
    # Update the data in memory
    for data in data_mahasiswa:
        if data["nim"] == nim:
            if nama_baru != "sama":
                data["nama"] = nama_baru
                renamed = True
            if asal_baru != "sama":
                data["asal"] = asal_baru
                relocation = True
            break
    
    response_message = f"Mahasiswa dengan NIM {nim}"
    if renamed:
        response_message += f" namanya menjadi {nama_baru}"
    if relocation:
        response_message += f" asalnya menjadi {asal_baru}"
    # Write the updated data back to the JSON file
    with open("data_mahasiswa.json", "w") as write_file:
        json.dump(data_mahasiswa, write_file, indent=4)  # Add indentation for readability

    return {"message": response_message}