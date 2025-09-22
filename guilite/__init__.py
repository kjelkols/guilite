"""
Guilite - A very lightweight GUI library for input-output oriented programs

This package provides:
- HTML report generation from Pydantic data structures
- A Simulator framework for input-output processing
- A minimal Flask web interface for GUI access
"""

__version__ = "0.1.0"

from .report_generator import ReportGenerator
from .simulator import Simulator
from .web_interface import WebInterface

__all__ = ["ReportGenerator", "Simulator", "WebInterface"]