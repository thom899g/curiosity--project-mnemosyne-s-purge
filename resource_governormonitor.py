"""
Resource monitoring module with comprehensive system metrics collection
Uses psutil for cross-platform system monitoring
"""

import psutil
import time
from typing import Dict, List, Tuple, Optional
from dataclasses