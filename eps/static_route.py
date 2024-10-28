from fastapi import APIRouter, HTTPException, Depends, Request, Response
from modules.authentication_db import AuthenticationDB
from modules.email import EmailService
import json


COOKIE_NAME = "session"
static_router = APIRouter()


@static_router.get("/states")
async def get_states():
    with open("./static/states_cities.json", "r") as f:
        data = json.load(f)
        keys = list(data.keys())
        return {"success": True, "data": keys}


@static_router.get("/countries")
async def get_countries():
    print("here")
    with open("./static/countries.json", "r") as f:
        data = json.load(f)
        countries = []
        for c in data:
            countries.append(c["name"])
        return {"success": True, "data": countries}


@static_router.get("/cities")
async def get_cities(state: str):
    with open("./static/states_cities.json", "r") as f:
        data = json.load(f)
        cities = data[state]
        return {"success": True, "data": cities}