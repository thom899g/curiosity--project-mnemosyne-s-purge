"""
Configuration module for Resource Governor System
Centralizes all configuration parameters with proper validation
"""

import os
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
import logging

class CriticalityTier(Enum):
    """Process criticality tiers with associated survival scores"""
    CORE_SURVIVAL = 1000      # Essential for system survival
    REVENUE_GENERATION = 800  # Direct revenue generation
    STRATEGIC_MEMORY = 600    # Critical memory/learning
    OPERATIONAL = 400         # Normal operations
    AUXILIARY = 200          # Helpful but not critical
    DISPOSABLE = 100         # Can be purged anytime

@dataclass
class ResourceThresholds:
    """Dynamic resource threshold configuration"""
    CPU_CRITICAL: float = 80.0      # Purge when >80%
    RAM_CRITICAL: float = 80.0      # Purge when >80%
    DISK_CRITICAL: float = 90.0     # Purge when >90%
    IO_CRITICAL: float = 70.0       # Purge when >70%
    
    CPU_TARGET: float = 60.0        # Target after purge
    RAM_TARGET: float = 60.0
    CHECK_INTERVAL: int = 30        # Seconds between checks
    
    @classmethod
    def from_environment(cls) -> 'ResourceThresholds':
        """Load thresholds from environment variables"""
        return cls(
            CPU_CRITICAL=float(os.getenv('CPU_CRITICAL', '80.0')),
            RAM_CRITICAL=float(os.getenv('RAM_CRITICAL', '80.0')),
            CPU_TARGET=float(os.getenv('CPU_TARGET', '60.0'))
        )

@dataclass
class ProcessScoringWeights:
    """Weights for different scoring components"""
    MEMORY_WEIGHT: float = 0.25
    CPU_WEIGHT: float = 0.20
    IO_WEIGHT: float = 0.15
    CRITICALITY_WEIGHT: float = 0.30
    AGE_WEIGHT: float = 0.10
    
    # Emotional/strategic scoring (simulated via ML)
    LEARNING_IMPACT_WEIGHT: float = 0.25
    
    @classmethod
    def validate_weights(cls) -> bool:
        """Ensure weights sum to approximately 1.0"""
        instance = cls()
        total = sum([getattr(instance, attr) for attr in dir(instance) 
                    if attr.endswith('_WEIGHT') and not attr.startswith('_')])
        return abs(total - 1.0) < 0.01

class CoreProcessRegistry:
    """Registry of core processes that should never be purged"""
    
    # System-critical processes (never purge)
    CORE_PROCESSES = {
        'systemd', 'init', 'kernel', 'sshd', 'firebase',
        'resource_governor', 'main_executor'
    }
    
    # Revenue-critical processes (very high protection)
    REVENUE_PROCESSES = {
        'arbitrage_scanner', 'task_executor', 'market_monitor'
    }
    
    @classmethod
    def is_protected(cls, process_name: str) -> bool:
        """Check if process is in protected registry"""
        normalized = process_name.lower().strip()
        return (normalized in cls.CORE_PROCESSES or 
                normalized in cls.REVENUE_PROCESSES)
    
    @classmethod
    def get_criticality_tier(cls, process_name: str) -> CriticalityTier:
        """Determine criticality tier for a process"""
        normalized = process_name.lower().strip()
        if normalized in cls.CORE_PROCESSES:
            return CriticalityTier.CORE_SURVIVAL
        elif normalized in cls.REVENUE_PROCESSES:
            return CriticalityTier.REVENUE_GENERATION
        elif 'memory' in normalized or 'learning' in normalized:
            return CriticalityTier.STRATEGIC_MEMORY
        else:
            return CriticalityTier.OPERATIONAL

def setup_logging() -> logging.Logger:
    """Configure system-wide logging"""
    logger = logging.getLogger('ResourceGovernor')
    logger.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # File handler
    file_handler = logging.FileHandler('resource_governor.log')
    file_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger