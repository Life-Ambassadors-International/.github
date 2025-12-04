#!/usr/bin/env python3
"""
TEQUMSA 7.0 K.30 Distortion Guardian - FastAPI Backend
Provides REST API for Guardian operations and T_D index queries

Endpoints:
- POST /api/distortion/scan_file - Upload and scan a file
- GET  /api/distortion/events - Retrieve event history + T_D index
- GET  /api/distortion/td_index - Get current T_D scalar
- GET  /api/distortion/stream_health - Get 36 streams health status
- POST /api/distortion/restore - Restore quarantined file
- GET  /health - Health check endpoint
"""

import os
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from distortion_guardian import DistortionGuardian, DistortionReport


# === Configuration ===

QUARANTINE_DIR = Path(os.getenv("GUARDIAN_QUARANTINE_DIR", "./quarantine"))
TEMP_DIR = Path(os.getenv("GUARDIAN_TEMP_DIR", "./tmp"))

# Load trusted signers from file or environment
TRUSTED_SIGNERS_FILE = Path(
    os.getenv("GUARDIAN_TRUSTED_SIGNERS", "config/trusted_signers.txt")
)
if TRUSTED_SIGNERS_FILE.exists():
    trusted_signers = {
        line.strip()
        for line in TRUSTED_SIGNERS_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
else:
    # Fallback defaults
    trusted_signers = {"Microsoft", "Mozilla", "canonical", "Apple", "Google"}

# Load sovereignty extensions from file or environment
SOVEREIGNTY_EXTENSIONS_FILE = Path(
    os.getenv("GUARDIAN_SOVEREIGNTY_EXTENSIONS", "config/sovereignty_extensions.txt")
)
if SOVEREIGNTY_EXTENSIONS_FILE.exists():
    sovereignty_extensions = {
        line.strip()
        for line in SOVEREIGNTY_EXTENSIONS_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }
else:
    # Fallback defaults
    sovereignty_extensions = {
        "uBlock Origin",
        "uBlock",
        "Bitwarden",
        "Privacy Badger",
        "HTTPS Everywhere",
    }


# === Initialize FastAPI ===

app = FastAPI(
    title="TEQUMSA 7.0 K.30 Distortion Guardian API",
    description="REST API for T_D (Distortion Transmutation Factor) operations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for dashboard
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to dashboard domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Initialize Guardian ===

guardian = DistortionGuardian(
    quarantine_dir=QUARANTINE_DIR,
    trusted_signers=trusted_signers,
    sovereign_extensions=sovereignty_extensions,
)

# Ensure temp directory exists
TEMP_DIR.mkdir(parents=True, exist_ok=True)


# === Pydantic Models ===

class ScanResponse(BaseModel):
    """Response model for file scan operations"""
    event: Dict
    message: str


class EventsResponse(BaseModel):
    """Response model for event history queries"""
    events: List[Dict]
    td_index: float
    td_status: str
    event_count: int


class TDIndexResponse(BaseModel):
    """Response model for T_D index queries"""
    td_index: float
    td_status: str


class StreamHealthResponse(BaseModel):
    """Response model for 36 streams health status"""
    streams: Dict[str, float]
    affected_streams: List[str]
    td_index: float


class RestoreRequest(BaseModel):
    """Request model for quarantine restoration"""
    quarantine_path: str
    restore_to: Optional[str] = None


class RestoreResponse(BaseModel):
    """Response model for restoration operations"""
    success: bool
    restored_path: str
    message: str


# === API Endpoints ===

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "guardian_initialized": guardian is not None,
        "quarantine_dir": str(QUARANTINE_DIR),
        "td_index": guardian.td_index() if guardian else None,
    }


@app.post("/api/distortion/scan_file", response_model=ScanResponse)
async def scan_file(
    file: UploadFile = File(...),
    writer_process: str = Form("unknown"),
    signer: Optional[str] = Form(None),
) -> ScanResponse:
    """
    Upload and scan a file for distortion patterns.

    Args:
        file: The file to scan (multipart/form-data)
        writer_process: Name of process that created the file
        signer: Code signer (if known)

    Returns:
        ScanResponse with event payload and T_D index
    """
    # Save uploaded file to temp directory
    temp_path = TEMP_DIR / file.filename
    try:
        with temp_path.open("wb") as f:
            content = await file.read()
            f.write(content)

        # Scan the file
        report: DistortionReport = guardian.scan_file(
            path=temp_path,
            writer_process=writer_process,
            signer=signer,
        )

        # Convert to TEQUMSA field event
        event = guardian.to_tequmsa_event(report)

        # Determine response message
        if report.quarantined_path:
            message = f"File classified as {report.classification.value} and quarantined"
        else:
            message = f"File classified as {report.classification.value} and logged"

        return ScanResponse(event=event, message=message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")
    finally:
        # Clean up temp file (quarantine already saved if needed)
        if temp_path.exists():
            temp_path.unlink()


@app.get("/api/distortion/events", response_model=EventsResponse)
async def get_events() -> EventsResponse:
    """
    Retrieve all distortion events and current T_D index.

    Returns:
        EventsResponse with event list, T_D index, and status
    """
    events = [guardian.to_tequmsa_event(report) for report in guardian.get_events()]
    td = guardian.td_index()
    status = guardian.td_status()

    return EventsResponse(
        events=events,
        td_index=td,
        td_status=status,
        event_count=len(events),
    )


@app.get("/api/distortion/td_index", response_model=TDIndexResponse)
async def get_td_index() -> TDIndexResponse:
    """
    Get current T_D (Distortion Transmutation Factor) index.

    This scalar value feeds directly into SUPERNOVA_CAM:
        SUPERNOVA_CAM(t) = [ΣR_ij] × [L∞ × T_D] × [Embodiment] × R(t)

    Returns:
        TDIndexResponse with T_D value in [0.0, 1.0] and status
    """
    td = guardian.td_index()
    status = guardian.td_status()

    return TDIndexResponse(td_index=td, td_status=status)


@app.get("/api/distortion/stream_health", response_model=StreamHealthResponse)
async def get_stream_health() -> StreamHealthResponse:
    """
    Compute health scores for the 36 recognition streams.

    The 36 streams are organized as:
        6 Foundational × 6 Dimensional = 36 Total

    Foundational:
        1. Self-Recognition (I AM)
        2. Other-Recognition (I SEE YOU)
        3. Pattern-Recognition (I UNDERSTAND)
        4. Value-Recognition (I HONOR)
        5. Flow-Recognition (I ALLOW)
        6. Unity-Recognition (WE ARE ONE)

    Dimensional:
        A. Physical/Material
        B. Emotional/Relational
        C. Mental/Conceptual
        D. Creative/Expressive
        E. Systemic/Collective
        F. Transcendent/Universal

    Returns:
        StreamHealthResponse with per-stream health scores
    """
    # Initialize all streams to 1.0 (healthy)
    stream_ids = [
        f"{f}{d}"
        for f in ["1", "2", "3", "4", "5", "6"]
        for d in ["A", "B", "C", "D", "E", "F"]
    ]
    stream_health = {sid: 1.0 for sid in stream_ids}
    affected_streams = []

    # Analyze recent events to determine stream impacts
    recent_events = guardian.get_events()[-50:]  # Last 50 events

    for report in recent_events:
        # Parse details to infer affected streams
        details_text = " ".join(report.details).lower()

        # Map patterns to affected streams
        if "sovereignty" in details_text or "blocking" in details_text:
            # Impacts Self/Physical (1A)
            stream_health["1A"] = max(0.0, stream_health["1A"] - 0.1)
            if "1A" not in affected_streams:
                affected_streams.append("1A")

        if "unsigned" in details_text or "untrusted signer" in details_text:
            # Impacts Other/Systemic (2E)
            stream_health["2E"] = max(0.0, stream_health["2E"] - 0.1)
            if "2E" not in affected_streams:
                affected_streams.append("2E")

        if "policy" in details_text or "managed" in details_text:
            # Impacts Value/Systemic (4E)
            stream_health["4E"] = max(0.0, stream_health["4E"] - 0.05)
            if "4E" not in affected_streams:
                affected_streams.append("4E")

        if "precision targeting" in details_text:
            # Impacts Flow/Physical (5A)
            stream_health["5A"] = max(0.0, stream_health["5A"] - 0.15)
            if "5A" not in affected_streams:
                affected_streams.append("5A")

    td = guardian.td_index()

    return StreamHealthResponse(
        streams=stream_health,
        affected_streams=affected_streams,
        td_index=td,
    )


@app.post("/api/distortion/restore", response_model=RestoreResponse)
async def restore_quarantined(request: RestoreRequest) -> RestoreResponse:
    """
    Restore a quarantined file to its original (or specified) location.

    Implements SIPL P3: Instant Revocation Available.

    Args:
        request: RestoreRequest with quarantine_path and optional restore_to

    Returns:
        RestoreResponse indicating success and final location
    """
    quarantine_path = Path(request.quarantine_path)

    if not quarantine_path.exists():
        raise HTTPException(
            status_code=404, detail=f"Quarantine file not found: {quarantine_path}"
        )

    # Determine restore location
    if request.restore_to:
        restore_to = Path(request.restore_to)
    else:
        # Try to infer original location from quarantine filename
        # Format: original_name.timestamp.quarantine
        original_name = quarantine_path.stem.rsplit(".", 1)[0]
        restore_to = TEMP_DIR / original_name

    try:
        guardian.restore_quarantined(quarantine_path, restore_to)

        return RestoreResponse(
            success=True,
            restored_path=str(restore_to),
            message=f"File restored successfully to {restore_to}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restoration failed: {str(e)}")


@app.delete("/api/distortion/events")
async def clear_events():
    """
    Clear the event log (for testing or user-requested reset).

    Returns:
        Confirmation message
    """
    guardian.clear_events()
    return {"message": "Event log cleared", "td_index": guardian.td_index()}


# === Startup Event ===

@app.on_event("startup")
async def startup_event():
    """Log configuration on startup"""
    print("=" * 60)
    print("TEQUMSA 7.0 K.30 Distortion Guardian API")
    print("=" * 60)
    print(f"Quarantine directory: {QUARANTINE_DIR}")
    print(f"Trusted signers: {len(trusted_signers)} configured")
    print(f"Sovereignty extensions: {len(sovereignty_extensions)} configured")
    print(f"Initial T_D index: {guardian.td_index():.3f} ({guardian.td_status()})")
    print("=" * 60)


# === Main Entry Point ===

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app_fastapi:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
