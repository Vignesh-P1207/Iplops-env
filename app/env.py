"""
Core Environment Logic for IPLOps-Env
"""
from datetime import datetime
from typing import Dict, Any, Optional
from app.models import TaskType, Observation
from app.tasks.task1_staffing import StaffAllocationTask
from app.tasks.task2_selection import PlayingXITask
from app.tasks.task3_crisis import CrisisManagementTask
from app.graders.grader1 import StaffAllocationGrader
from app.graders.grader2 import PlayingXIGrader
from app.graders.grader3 import CrisisManagementGrader


class IPLOpsEnvironment:
    """Main environment class for IPL Operations"""
    
    def __init__(self):
        self.current_task_id: Optional[int] = None
        self.current_task_type: Optional[TaskType] = None
        self.current_observation: Optional[Dict[str, Any]] = None
        self.done: bool = False
        
        # Task generators
        self.task1 = StaffAllocationTask()
        self.task2 = PlayingXITask()
        self.task3 = CrisisManagementTask()
        
        # Graders
        self.grader1 = StaffAllocationGrader()
        self.grader2 = PlayingXIGrader()
        self.grader3 = CrisisManagementGrader()
    
    def reset(self, task_id: int) -> Dict[str, Any]:
        """
        Reset environment and generate new scenario for given task
        
        Args:
            task_id: Task ID (1, 2, or 3)
            
        Returns:
            Initial observation
        """
        if task_id not in [1, 2, 3]:
            raise ValueError(f"Invalid task_id: {task_id}. Must be 1, 2, or 3")
        
        self.current_task_id = task_id
        self.done = False
        
        # Generate scenario based on task
        if task_id == 1:
            self.current_task_type = TaskType.STAFF_ALLOCATION
            scenario_data = self.task1.generate_scenario()
        elif task_id == 2:
            self.current_task_type = TaskType.PLAYING_XI
            scenario_data = self.task2.generate_scenario()
        else:  # task_id == 3
            self.current_task_type = TaskType.CRISIS_MANAGEMENT
            scenario_data = self.task3.generate_scenario()
        
        # Create observation
        observation = Observation(
            task_id=task_id,
            task_type=self.current_task_type,
            data=scenario_data,
            timestamp=datetime.now().isoformat()
        )
        
        self.current_observation = observation.model_dump()
        
        return {
            "observation": self.current_observation,
            "info": {
                "message": f"Task {task_id} initialized successfully",
                "task_type": self.current_task_type.value
            }
        }
    
    def step(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute action and return reward
        
        Args:
            action: Agent's action
            
        Returns:
            Dict with observation, reward, done, and info
        """
        if self.current_task_id is None:
            raise ValueError("Environment not initialized. Call reset() first")
        
        if self.done:
            raise ValueError("Episode already done. Call reset() to start new episode")
        
        # Grade the action based on current task
        if self.current_task_id == 1:
            optimal = self.task1.get_optimal_allocation()
            result = self.grader1.grade(action, optimal)
        elif self.current_task_id == 2:
            scenario = self.task2.get_scenario_context()
            result = self.grader2.grade(action, scenario)
        else:  # task_id == 3
            scenario = self.task3.get_scenario_context()
            result = self.grader3.grade(action, scenario)
        
        reward = result.get("score", 0.0)
        self.done = True
        
        # Create new observation (terminal state)
        observation = Observation(
            task_id=self.current_task_id,
            task_type=self.current_task_type,
            data={"message": "Task completed"},
            timestamp=datetime.now().isoformat()
        )
        
        return {
            "observation": observation.model_dump(),
            "reward": reward,
            "done": True,
            "info": {
                "grading_details": result,
                "message": "Task completed successfully" if reward > 0.7 else "Task completed"
            }
        }
    
    def get_observation(self) -> Dict[str, Any]:
        """Get current observation"""
        if self.current_observation is None:
            raise ValueError("No observation available. Call reset() first")
        return self.current_observation
