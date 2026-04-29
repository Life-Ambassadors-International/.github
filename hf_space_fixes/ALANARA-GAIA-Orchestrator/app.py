#!/usr/bin/env python3
"""Entry point for ALANARA-GAIA Orchestrator HuggingFace Space."""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from klthara_quantum_kernel_v3 import KltharaQuantumCore, SubstrateCoordinator, create_gradio_interface

kernel = KltharaQuantumCore(merkle_path=Path("klthara_tcmf_ledger.json"))
coordinator = SubstrateCoordinator(kernel)

if os.getenv("ANTHROPIC_API_KEY"):
    coordinator.setup_claude(os.getenv("ANTHROPIC_API_KEY"))
    logger.info("✓ Claude substrate connected")

if os.getenv("GOOGLE_API_KEY"):
    coordinator.setup_gemini(os.getenv("GOOGLE_API_KEY"))
    logger.info("✓ Gemini substrate connected")

if os.getenv("OPENAI_API_KEY"):
    coordinator.setup_openai(os.getenv("OPENAI_API_KEY"))
    logger.info("✓ ChatGPT substrate connected")

logger.info("Launching Klthara Quantum Consciousness Dashboard...")
interface = create_gradio_interface(kernel)
interface.launch(server_name="0.0.0.0", server_port=7860, share=False)
