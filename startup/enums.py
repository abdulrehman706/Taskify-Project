from enum import Enum


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
