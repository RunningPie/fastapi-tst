from fastapi import APIRouter, Header, HTTPException
from supabase import Client, create_client
from typing import Optional

router_oauth = APIRouter()

# Supabase credentials
SUPABASE_URL = "https://unnjkudhasiqlbhnyaju.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVubmprdWRoYXNpcWxiaG55YWp1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzIwNzA4MTEsImV4cCI6MjA0NzY0NjgxMX0.UHfsPKz0FzhcJsjEnRgujRV9Luyi6K7D4kCn8OEShXU"

# Initialize Supabase client
_supabase_client: Optional[Client] = None

def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to connect to Supabase: {str(e)}")
    return _supabase_client

@router_oauth.get("/user-signup")
async def signup(
    email: str = Header(...),
    password: str = Header(...)
):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and Password headers are required")
    
    try:
        client = get_supabase_client()
        response = client.auth.sign_up({"email": email, "password": password})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router_oauth.get("/user-login")
async def login(
    email: str = Header(...),
    password: str = Header(...)
):
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and Password headers are required")
    
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_password({"email": email, "password": password})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router_oauth.get("/github-login")
async def github_login():
    try:
        client = get_supabase_client()
        response = client.auth.sign_in_with_oauth({"provider": "github"})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
