"""
Prompts module for IPLOps-Env tasks
Contains system and user prompts for guiding AI agents
"""

from .task3_prompts import (
    TASK3_SYSTEM_PROMPT,
    TASK3_USER_PROMPT_TEMPLATE,
    format_task3_prompt,
    CRISIS_PRIORITIES,
    CORRECT_ACTIONS
)

__all__ = [
    "TASK3_SYSTEM_PROMPT",
    "TASK3_USER_PROMPT_TEMPLATE",
    "format_task3_prompt",
    "CRISIS_PRIORITIES",
    "CORRECT_ACTIONS"
]
