
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS for any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"]
)

# Define input model
class TelemetryRequest(BaseModel):
    regions: list
    threshold_ms: int

# Sample telemetry data
# You’ll replace this with real telemetry CSV if required
# For now, you can load from the sample bundle uploaded in the repo

telemetry_data = pd.read_csv("telemetry.csv")  # upload telemetry CSV in repo root

@app.post("/")
def get_metrics(req: TelemetryRequest):
    response = {}
    for region in req.regions:
        region_data = telemetry_data[telemetry_data["region"] == region]
        if len(region_data) == 0:
            response[region] = {}
            continue
        avg_latency = region_data["latency_ms"].mean()
        p95_latency = np.percentile(region_data["latency_ms"], 95)
        avg_uptime = region_data["uptime"].mean()
        breaches = (region_data["latency_ms"] > req.threshold_ms).sum()
        response[region] = {
            "avg_latency": avg_latency,
            "p95_latency": p95_latency,
            "avg_uptime": avg_uptime,
            "breaches": int(breaches)
        }
    return response
