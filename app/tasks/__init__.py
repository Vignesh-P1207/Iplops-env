"""Task generators for IPLOps-Env"""
from app.tasks.task1_staffing import StaffAllocationTask
from app.tasks.task2_selection import PlayingXITask
from app.tasks.task3_crisis import CrisisManagementTask

__all__ = ["StaffAllocationTask", "PlayingXITask", "CrisisManagementTask"]
