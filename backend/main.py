from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import asyncio
import json
import time
import random
from ai_engine import AIEngine
from log_generator import generate_log

app = FastAPI(title="CyberShield JOJ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ai = AIEngine()
attack_mode = {"active": False, "type": None}

@app.get("/")
async def dashboard():
    return FileResponse("../frontend/index.html")

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("Dashboard connecté !")
    try:
        while True:
            log = generate_log()

            if attack_mode["active"]:
                if attack_mode["type"] == "ddos":
                    log["req_rate"]    = random.randint(10000, 20000)
                    log["bytes"]       = random.randint(100000, 600000)
                    log["port"]        = 8080
                    log["duration_ms"] = random.randint(1, 10)
                elif attack_mode["type"] == "brute":
                    log["req_rate"]    = random.randint(800, 1200)
                    log["bytes"]       = random.randint(50, 300)
                    log["port"]        = 22
                    log["duration_ms"] = random.randint(1, 15)
                elif attack_mode["type"] == "scan":
                    log["req_rate"]    = random.randint(500, 900)
                    log["bytes"]       = random.randint(50, 150)
                    log["port"]        = random.choice([22, 3306, 5432, 8080])
                    log["duration_ms"] = random.randint(1, 5)
                elif attack_mode["type"] == "sqli":
                    log["req_rate"]    = random.randint(200, 500)
                    log["bytes"]       = random.randint(5000, 20000)
                    log["port"]        = 3306
                    log["duration_ms"] = random.randint(1, 8)

            score, is_anomaly = ai.analyze(log)

            log["anomaly_score"] = round(score, 3)
            log["is_anomaly"]    = is_anomaly
            log["timestamp"]     = time.strftime("%H:%M:%S")
            log["attack_type"]   = attack_mode["type"] if attack_mode["active"] else None

            await ws.send_text(json.dumps(log))
            await asyncio.sleep(0.8)

    except WebSocketDisconnect:
        print("Dashboard déconnecté.")

@app.post("/simulate/{attack_type}")
async def simulate_attack(attack_type: str):
    attack_mode["active"] = True
    attack_mode["type"]   = attack_type
    asyncio.create_task(stop_attack_after(15))
    return {"status": "attaque lancée", "type": attack_type, "duree": "15s"}

async def stop_attack_after(seconds: int):
    await asyncio.sleep(seconds)
    attack_mode["active"] = False
    attack_mode["type"]   = None
    print("Attaque terminée — retour au trafic normal")

@app.post("/stop")
async def stop_attack():
    attack_mode["active"] = False
    attack_mode["type"]   = None
    return {"status": "arrêté"}

@app.get("/stats")
async def get_stats():
    return {
        "total_requests":     ai.total,
        "anomalies_detected": ai.anomalies,
        "blocked_ips":        list(ai.blocked),
        "security_score":     ai.security_score(),
    }

app.mount("/static", StaticFiles(directory="../frontend"), name="static")
