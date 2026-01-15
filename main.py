import os
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Dict, List
import asyncio

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Default data structure
default_data = {
    "scene": "intro",
    "team_a": {
        "name": "Team A",
        "score": 0,
        "logo": "",
        "players": [{"name": "", "agent": "", "kills": 0, "deaths": 0, "assists": 0, "weapon": ""} for _ in range(5)]
    },
    "team_b": {
        "name": "Team B",
        "score": 0,
        "logo": "",
        "players": [{"name": "", "agent": "", "kills": 0, "deaths": 0, "assists": 0, "weapon": ""} for _ in range(5)]
    },
    "match_time": "00:00",
    "killfeed": []
}

# Load or create data file
data_file = "data/overlay_data.json"
os.makedirs("data", exist_ok=True)

try:
    with open(data_file, "r") as f:
        overlay_data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    overlay_data = default_data
    with open(data_file, "w") as f:
        json.dump(overlay_data, f, indent=2)

def save_data():
    with open(data_file, "w") as f:
        json.dump(overlay_data, f, indent=2)

async def broadcast_update():
    for connection in active_connections:
        try:
            await connection.send_json(overlay_data)
        except:
            active_connections.remove(connection)

@app.get("/", response_class=HTMLResponse)
async def get_control_panel(request: Request):
    return templates.TemplateResponse("control_panel.html", {"request": request, "data": overlay_data})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        # Send current data to new connection
        await websocket.send_json({"type": "initial_data", **overlay_data})
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_json()
            if data.get('type') == 'update_team':
                team = data['team']
                team_data = data['data']
                
                # Update the specific team data while preserving existing data
                if team in overlay_data:
                    # Update team info
                    overlay_data[team].update({
                        'name': team_data.get('name', overlay_data[team].get('name', '')),
                        'score': team_data.get('score', overlay_data[team].get('score', 0)),
                        'logo': team_data.get('logo', overlay_data[team].get('logo', ''))
                    })
                    
                    # Update players while preserving agent selections
                    if 'players' in team_data:
                        for i, player in enumerate(team_data['players']):
                            if i < len(overlay_data[team]['players']):
                                # Preserve existing agent if not provided in update
                                if 'agent' not in player and 'agent' in overlay_data[team]['players'][i]:
                                    player['agent'] = overlay_data[team]['players'][i]['agent']
                                # Update player data
                                overlay_data[team]['players'][i].update(player)
                
                save_data()  # Save to file
                # Broadcast the specific update to all clients
                for connection in active_connections:
                    try:
                        await connection.send_json({
                            "type": "update_team",
                            "team": team,
                            "data": overlay_data[team]
                        })
                    except:
                        active_connections.remove(connection)
                        continue
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        active_connections.remove(websocket)

@app.post("/update")
async def update_data(data: dict):
    # Update the overlay data
    overlay_data.update(data)
    save_data()
    
    # Broadcast the update to all connected clients
    for connection in active_connections:
        try:
            # Send the full state to ensure everything is in sync
            await connection.send_json({
                "type": "initial_data",
                **overlay_data
            })
        except:
            active_connections.remove(connection)
            continue
    
    return {"status": "success"}

@app.get("/overlay", response_class=HTMLResponse)
async def get_overlay(request: Request):
    return templates.TemplateResponse("overlay.html", {"request": request, "data": overlay_data})

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
