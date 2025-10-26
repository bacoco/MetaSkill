#!/usr/bin/env python3
"""
Configuration manager for Synapse pattern detection
"""

import os
import json
import logging
from typing import Dict, Optional


class ConfigManager:
    """Manages configuration and thresholds"""

    DEFAULT_CONFIG = {
        "thresholds": {
            "pattern_frequency_min": 3,
            "pattern_frequency_high": 6,
            "impact_score_threshold": 0.5,
            "trend_score_threshold": 0.3,
            "urgency_score_threshold": 0.6,
            "roi_score_threshold": 0.7,
            "recommendation_min_score": 0.5
        },
        "analysis": {
            "max_sessions_to_analyze": 50,
            "file_correlation_threshold": 2,
            "problem_recurrence_threshold": 2,
            "temporal_pattern_window_days": 7,
            "enable_ml_clustering": False,
            "enable_nlp_analysis": False
        },
        "scoring": {
            "frequency_weight": 0.25,
            "impact_weight": 0.25,
            "trend_weight": 0.15,
            "urgency_weight": 0.20,
            "roi_weight": 0.15
        },
        "output": {
            "report_format": "both",  # "json", "text", "both"
            "include_examples": True,
            "include_visualizations": False,
            "verbose": True
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        self.config = self.load_config(config_path)
        self.logger = logging.getLogger(__name__)

    def load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        config = self.DEFAULT_CONFIG.copy()

        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                    # Deep merge
                    for key, value in user_config.items():
                        if isinstance(value, dict) and key in config:
                            config[key].update(value)
                        else:
                            config[key] = value
                self.logger.info(f"Loaded configuration from {config_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")

        return config

    def get(self, *keys, default=None):
        """Get nested config value"""
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
            if value is None:
                return default
        return value

    def validate(self) -> bool:
        """Validate configuration"""
        # Check required keys
        required_keys = ["thresholds", "analysis", "scoring", "output"]
        for key in required_keys:
            if key not in self.config:
                self.logger.error(f"Missing required config key: {key}")
                return False

        # Validate scoring weights sum to 1.0
        weights = self.config["scoring"]
        total_weight = sum([
            weights["frequency_weight"],
            weights["impact_weight"],
            weights["trend_weight"],
            weights["urgency_weight"],
            weights["roi_weight"]
        ])

        if abs(total_weight - 1.0) > 0.01:
            self.logger.warning(f"Scoring weights sum to {total_weight}, not 1.0")

        return True