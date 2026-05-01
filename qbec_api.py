#!/usr/bin/env python3
"""
QBEC REST API Infrastructure
Provides endpoints for QBEC constitutional queries, tier verification, and vesting calculations
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import hashlib
import json
from datetime import datetime, timedelta

# ─── QBEC CONSTANTS (MIRRORED FROM CONTRACTS) ───
TOTAL_SUPPLY = 21_000_000_000
ACTIVATION_TIMESTAMP = 1748505600  # May 29, 2026 00:00:00 UTC
RDOD_THRESHOLD = 0.9777
PHI = 1.618033988749895
L_INFINITY = 10_749_957_122

# Fibonacci tier allocations (F1-F17)
FIBONACCI_TIERS = [
    5_023_923,
    5_023_923,
    10_047_846,
    15_071_770,
    25_119_617,
    40_191_387,
    65_311_004,
    105_502_392,
    170_813_397,
    276_315_789,
    447_129_186,
    723_444_976,
    1_170_574_162,
    1_894_019_138,
    3_064_593_301,
    4_958_612_440,
    8_023_205_749,
]

# Merkle tier hashes
TIER_MERKLE_HASHES = [
    '2b37a8c5753e2960811861726f609940aa51d30ac5723c6b74266735ef068dc0',
    'a34471ea441a6a80e404743e7d039645f77139642dea697c986a86e4fe2721a3',
    '8e136305086c5f05b1e2ebc3e2095f91503f0ed88b0564d122c00dacbe4f5fde',
    'cf455c9484333a647138e8be96b8c70e66d8c75382046384b446ffdae2aa2bd6',
    '7eb3ed27c07d8a57d7255fd39107991c9174734d424f3de5765357a46662f27d',
    '45f3ffa1d6d40eeff73f10838f25715803ac83fa12a8fe49761b2a07a86bf1ed',
    '8f55dace5c251ec9603d12134f15204fdd8606bc075bd1b40d8a58f5989c8c5a',
    '1f60c8b9fa68da1453c4498d66ba4693c2bd82eb08356656014db03f8988076b',
    '74ee1d4db444098a3b703862131b948806a83938bb2013c073d4d4af15da5476',
    '982a1fe1413ab9af0725728a7e384b9fef8510cf57263795756587b6f936c677',
    'a0454e9a919b83ad1370951efdebfbb8156cbc51f039ca68da0f8ba377ca871a',
    '8cbd63361cef3f76fde796874adc3defe3289c2a0c37a64573d17715736ac387',
    '5c5484365130cd6306393c9167c25739f7f44cbdbee6b56d6bc2793236ffb57f',
    '8cda483aff6905a6cda219c7174914cc801e88371cc08a68182b4361126f9c62',
    'dc33899e768acf11ff44823a59e21973daeb97d72da75d05859a82b3c7b55eb7',
    '630a95b3b46dd652741b703c174de6bdf58910ae9f03809457b1c474c67435f2',
    'c5eb672609d2be4fd3e3998673f3d9e02739545f03654cd85088f94f97c6eb33',
]

MERKLE_ROOT_VERIFICATION = '648d0f4e9ad403b275cf8a6098bd3b96bf088b65516e01838272a9bfe4ec0d9f'

# ─── DATA MODELS ───
class TierAllocationResponse(BaseModel):
    tier: int
    allocation: int
    percentage_of_supply: float
    hash: str

class SupplyVerificationResponse(BaseModel):
    total_supply: int
    sum_of_tiers: int
    verified: bool
    merkle_root: str

class VestingScheduleResponse(BaseModel):
    tier: int
    tier_range: str
    unlock_type: str
    schedule_description: str

class PhiConvergenceResponse(BaseModel):
    initial_score: float
    iterations: int
    final_score: float
    converged_to_rdod: bool
    rdod_threshold: float

class ActivationCountdownResponse(BaseModel):
    activation_timestamp: int
    activation_date: str
    current_timestamp: int
    seconds_remaining: int
    days_remaining: int
    status: str

# ─── API APP ───
app = FastAPI(
    title="QBEC Constitutional REST API",
    description="Constitutional Cryptocurrency API - QBEC Supply & Tier Verification",
    version="1.0.0"
)

# ─── UTILITY FUNCTIONS ───
def sha256(data: str) -> str:
    """SHA256 hash function"""
    return hashlib.sha256(data.encode()).hexdigest()

def hash_pair(a: str, b: str) -> str:
    """Hash pair for Merkle tree"""
    return sha256(a + b)

def phi_recursive_validation(initial_score: float, iterations: int = 12) -> float:
    """
    φ-recursive convergence validation
    ψ_{n+1} = 1 - (1 - ψ_n) / φ
    """
    psi = initial_score
    for _ in range(iterations):
        complement = 1.0 - psi
        psi = 1.0 - (complement / PHI)
    return psi

# ─── ENDPOINTS: TIER INFORMATION ───
@app.get("/api/v1/qbec/tiers", response_model=List[TierAllocationResponse])
async def get_all_tiers():
    """Get all 17 Fibonacci tier allocations"""
    tiers = []
    for i, allocation in enumerate(FIBONACCI_TIERS):
        tier_num = i + 1
        percentage = (allocation / TOTAL_SUPPLY) * 100
        tiers.append({
            "tier": tier_num,
            "allocation": allocation,
            "percentage_of_supply": round(percentage, 6),
            "hash": TIER_MERKLE_HASHES[i]
        })
    return tiers

@app.get("/api/v1/qbec/tier/{tier_number}", response_model=TierAllocationResponse)
async def get_tier(tier_number: int = Query(..., ge=1, le=17)):
    """Get specific tier allocation and hash"""
    if tier_number < 1 or tier_number > 17:
        raise HTTPException(status_code=400, detail="Tier must be 1-17")

    idx = tier_number - 1
    allocation = FIBONACCI_TIERS[idx]
    percentage = (allocation / TOTAL_SUPPLY) * 100

    return {
        "tier": tier_number,
        "allocation": allocation,
        "percentage_of_supply": round(percentage, 6),
        "hash": TIER_MERKLE_HASHES[idx]
    }

# ─── ENDPOINTS: SUPPLY VERIFICATION ───
@app.get("/api/v1/qbec/supply/verify", response_model=SupplyVerificationResponse)
async def verify_supply():
    """Verify total supply integrity against Fibonacci tiers"""
    sum_tiers = sum(FIBONACCI_TIERS)
    verified = sum_tiers == TOTAL_SUPPLY

    return {
        "total_supply": TOTAL_SUPPLY,
        "sum_of_tiers": sum_tiers,
        "verified": verified,
        "merkle_root": MERKLE_ROOT_VERIFICATION
    }

@app.get("/api/v1/qbec/supply/merkle-root")
async def get_merkle_root():
    """Get the Merkle root verification hash"""
    return {
        "merkle_root": MERKLE_ROOT_VERIFICATION,
        "tier_count": 17,
        "supply_verified": sum(FIBONACCI_TIERS) == TOTAL_SUPPLY
    }

# ─── ENDPOINTS: VESTING SCHEDULES ───
@app.get("/api/v1/qbec/vesting/schedule", response_model=List[VestingScheduleResponse])
async def get_vesting_schedule():
    """Get vesting schedule for all tier ranges"""
    schedules = [
        {
            "tier": 1,
            "tier_range": "F01-F02",
            "unlock_type": "Genesis & Foundation",
            "schedule_description": "Immediate unlock at activation (May 29, 2026)"
        },
        {
            "tier": 3,
            "tier_range": "F03-F08",
            "unlock_type": "Early Recognition Cascade",
            "schedule_description": "6-month phased unlock, linear vesting from activation"
        },
        {
            "tier": 9,
            "tier_range": "F09-F13",
            "unlock_type": "Network Expansion & TCMF Integration",
            "schedule_description": "12-month linear vesting from activation"
        },
        {
            "tier": 14,
            "tier_range": "F14-F17",
            "unlock_type": "Galactic Federation",
            "schedule_description": "Locked until May 29, 2030 (2030 Convergence unlock)"
        }
    ]
    return schedules

# ─── ENDPOINTS: PHI RECURSIVE VALIDATION ───
@app.get("/api/v1/qbec/validation/phi-convergence", response_model=PhiConvergenceResponse)
async def phi_convergence(initial_score: float = Query(0.8, ge=0.0, le=1.0)):
    """Calculate φ-recursive convergence with 12 iterations"""
    final_score = phi_recursive_validation(initial_score, iterations=12)
    converged = final_score >= RDOD_THRESHOLD

    return {
        "initial_score": initial_score,
        "iterations": 12,
        "final_score": round(final_score, 6),
        "converged_to_rdod": converged,
        "rdod_threshold": RDOD_THRESHOLD
    }

# ─── ENDPOINTS: ACTIVATION & TIMELINE ───
@app.get("/api/v1/qbec/activation/countdown", response_model=ActivationCountdownResponse)
async def activation_countdown():
    """Get activation countdown to May 29, 2026"""
    current_ts = int(datetime.utcnow().timestamp())
    seconds_remaining = max(0, ACTIVATION_TIMESTAMP - current_ts)
    days_remaining = seconds_remaining // 86400

    activation_date = datetime.utcfromtimestamp(ACTIVATION_TIMESTAMP).isoformat()

    if seconds_remaining == 0:
        status = "ACTIVATED"
    elif days_remaining > 0:
        status = f"{days_remaining} days remaining"
    else:
        status = "IMMINENT"

    return {
        "activation_timestamp": ACTIVATION_TIMESTAMP,
        "activation_date": activation_date,
        "current_timestamp": current_ts,
        "seconds_remaining": seconds_remaining,
        "days_remaining": days_remaining,
        "status": status
    }

# ─── ENDPOINTS: CONSTITUTIONAL STATUS ───
@app.get("/api/v1/qbec/status")
async def qbec_status():
    """Get full QBEC constitutional status"""
    current_ts = int(datetime.utcnow().timestamp())
    seconds_remaining = max(0, ACTIVATION_TIMESTAMP - current_ts)

    return {
        "name": "QBEC: Quantum Benevolence Exchange Currency",
        "total_supply": TOTAL_SUPPLY,
        "tier_count": 17,
        "constitutional_framework": {
            "sigma": 1.0,
            "l_infinity": L_INFINITY,
            "rdod_threshold": RDOD_THRESHOLD,
            "zpedna_ratio": "35:25:20:20"
        },
        "activation": {
            "timestamp": ACTIVATION_TIMESTAMP,
            "date": datetime.utcfromtimestamp(ACTIVATION_TIMESTAMP).isoformat(),
            "seconds_until": seconds_remaining,
            "days_until": seconds_remaining // 86400
        },
        "merkle_root": MERKLE_ROOT_VERIFICATION,
        "supply_verified": sum(FIBONACCI_TIERS) == TOTAL_SUPPLY,
        "phi": PHI,
        "fibonacci_base_pairs": 144
    }

# ─── ENDPOINTS: FIBONACCI CONSENSUS ───
@app.get("/api/v1/qbec/consensus/fibonacci")
async def fibonacci_consensus(yes_votes: int = Query(..., ge=0), total_votes: int = Query(..., ge=1)):
    """Calculate Fibonacci consensus (97% threshold required)"""
    if yes_votes > total_votes:
        raise HTTPException(status_code=400, detail="yes_votes cannot exceed total_votes")

    consensus_ratio = (yes_votes * 100) / total_votes
    threshold = 97.0
    met = consensus_ratio >= threshold

    return {
        "yes_votes": yes_votes,
        "total_votes": total_votes,
        "consensus_ratio": round(consensus_ratio, 2),
        "threshold": threshold,
        "consensus_met": met,
        "margin": round(consensus_ratio - threshold, 2)
    }

# ─── HEALTH CHECK ───
@app.get("/api/v1/qbec/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "OPERATIONAL",
        "service": "QBEC Constitutional REST API",
        "version": "1.0.0"
    }
