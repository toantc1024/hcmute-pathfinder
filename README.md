# hcmute-pathfinder

Final project for Artificial Course in HCMUTE 2023
How to run?

1. `pip install fastapi uvicorn pydantic`
2. `cd ./backend`
3. `python3 -m uvicorn main:app --reload`

`
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

   `
