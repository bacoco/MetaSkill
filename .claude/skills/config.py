#!/usr/bin/env python3
"""
Centralized configuration for EvolveSkill (shared across Cortex/Synapse/Forge)
"""

class EvolveSkillConfig:
    # Cortex
    MAX_EVENTS = 1000
    LOG_SIZE_MB = 10

    # Synapse
    PATTERN_THRESHOLD = 5
    MAX_LOG_PARSE_BYTES = 2_097_152  # 2 MB
