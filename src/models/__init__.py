from typing import TypeVar
from .cycle import WhoopCycle
from .recovery import WhoopRecovery
from .sleep import WhoopSleep
from .workout import WhoopWorkout

Model = TypeVar("Model", WhoopCycle, WhoopRecovery, WhoopSleep, WhoopWorkout)
