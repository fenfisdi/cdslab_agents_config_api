from enum import Enum


class ExecutionStatus(Enum):
    RUNNING: str = 'running'
    EXECUTED: str = 'executed'
    FAILED: str = 'failed'
