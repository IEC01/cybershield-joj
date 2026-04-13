import random
import time

SYSTEMS = [
    "billetterie.joj2026.sn",
    "accreditations.joj2026.sn",
    "resultats.joj2026.sn",
    "site-officiel.joj2026.sn"
]

IPS = [
    "196.8.42.17", "41.223.15.88", "102.89.33.201",
    "154.66.12.9", "77.32.100.4", "203.0.113.55",
    "192.168.1.10", "10.0.0.5"
]

METHODS = ["GET", "POST", "PUT", "DELETE"]

PATHS = [
    "/login", "/api/tickets", "/results",
    "/admin", "/api/athletes", "/auth", "/dashboard"
]

def generate_log():
    return {
        "ip":          random.choice(IPS),
        "method":      random.choice(METHODS),
        "path":        random.choice(PATHS),
        "system":      random.choice(SYSTEMS),
        "req_rate":    random.randint(10, 300),
        "bytes":       random.randint(200, 8000),
        "status":      random.choice([200, 200, 200, 401, 403, 500]),
        "port":        random.choice([80, 443, 8080]),
        "duration_ms": random.randint(20, 600),
    }
