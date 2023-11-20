from fastapi import FastAPI
from app import Map
from pydantic import BaseModel

class Item(BaseModel):
    lat: float
    lon: float

class Route(BaseModel):
    lat: float
    lon: float 
    id: str 
    type: str

app = FastAPI()

map = Map()

@app.post("/map/get_nearest_node/")
async def get_nearest_node(item: Item):
    return map.getNearestNode(lat=10.8501, lon=106.7718)

@app.get("/map/get_destination")
async def get_destionation():
    return {
        "destionations": map.getAllBuildings()
    }

@app.post("/map/find-route")
async def findShortestPath(item: Route):
    path = map.findShortestPath(lat=item.lat, lon=item.lon, target_id=item.id, type=item.type)
    if (path == 'FAILURE'):
        return {
            "status": "failure"
        }
    return {
        "status": "success",
        "solution": path
    }
   