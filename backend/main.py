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
    map.findShortestPath(lat=item.lat, lon=item.lon, target_id=item.id, type=item.type)
    return {
        "status": "success",
        "solution": [
          [106.7665444, 10.8558775],
          [106.7665667, 10.8557118],
          [106.7665451, 10.8555151],
          [106.7665224, 10.855431],
          [106.766505, 10.8553668],
          [106.7664804, 10.855276],
          [106.7664551, 10.8551992],
          [106.7664878, 10.8551155],
          [106.7665263, 10.8550564],
          [106.766603, 10.8549609],
          [106.7667269, 10.8548645],
          [106.766807, 10.8547889],
          [106.7668655, 10.8547163],
          [106.7670535, 10.8543985],
          [106.7671069, 10.8543265],
          [106.7674016, 10.8539295],
          [106.7675742, 10.8536844],
          [106.7676728, 10.8535543],
          [106.7678268, 10.8533969],
          [106.7679158, 10.8532987],
          [106.768133, 10.8531248],
          [106.7683896, 10.8528781],
          [106.7684931, 10.8528338],
          [106.7685505, 10.8528093],
          [106.7690178, 10.8527016]]
    }
   