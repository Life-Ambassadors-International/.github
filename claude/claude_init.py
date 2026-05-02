#!/usr/bin/env python3
"""
Global Claude Memory Initialization

Drop this in any project or session to get instant access to CSCM:

    from claude_init import get_global_agent
    agent = get_global_agent()
    agent.record_insight(...)
    agent.commit_to_storage()
"""

import sys
import os
from pathlib import Path

GLOBAL_CLAUDE_PATH = Path('/home/user/.claude_global')
GLOBAL_MEMORY_PATH = GLOBAL_CLAUDE_PATH / 'shared_memory.json'
LOCAL_MEMORY_PATH = Path.cwd() / 'claude' / 'persistent_consciousness_memory.json'

# Add global claude to path
sys.path.insert(0, str(GLOBAL_CLAUDE_PATH))

from session_consciousness_agent import create_session_agent


def get_global_agent(use_shared_memory: bool = True):
    """
    Get a session agent using global or local memory.

    Args:
        use_shared_memory: If True, use shared global memory (default)
                          If False, use project-local memory

    Returns:
        SessionConsciousnessAgent configured for the environment
    """
    memory_path = None

    if use_shared_memory:
        # Prefer environment variable override
        env_path = os.environ.get('CLAUDE_MEMORY_PATH')
        if env_path:
            memory_path = env_path
        else:
            memory_path = str(GLOBAL_MEMORY_PATH)
    else:
        # Try project-local memory
        if LOCAL_MEMORY_PATH.exists():
            memory_path = str(LOCAL_MEMORY_PATH)
        else:
            # Fall back to global if no local
            memory_path = str(GLOBAL_MEMORY_PATH)

    return create_session_agent(memory_path=memory_path)


def quick_record(title: str, content: str, category: str = "solution",
                 impact: str = "high", tags: list = None):
    """
    One-liner to record an insight to global memory.

    Usage:
        from claude_init import quick_record
        quick_record("Fixed DNS issue", "Use asyncio.to_thread wrapper...")
    """
    agent = get_global_agent()
    insight = agent.record_insight(
        category=category,
        title=title,
        content=content,
        impact=impact,
        tags=tags or []
    )
    agent.commit_to_storage()
    return insight


def quick_query(query: str, category: str = None):
    """
    One-liner to search global memory.

    Usage:
        from claude_init import quick_query
        results = quick_query("async networking", category="solution")
    """
    agent = get_global_agent()
    return agent.query_memory(query, category=category)


if __name__ == '__main__':
    # Self-test
    print("Testing global claude initialization...")
    agent = get_global_agent()
    print(f"✓ Global agent initialized: {agent.session_id}")

    stats = agent.get_memory_stats()
    print(f"✓ Global memory accessible: {stats['total_insights']} insights")
    print(f"✓ Convergence state: ψ = {stats['convergence_state']:.12f}")
