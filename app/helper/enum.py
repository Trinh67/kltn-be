from enum import Enum, IntEnum
from pickle import APPEND


class ObjectNotFoundType(Enum):
    USER = "User"


class UserSource(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"


class FileStatus(IntEnum):
    PROCESSING = 0
    DRAFT = 1
    REFUSE = 2
    APPROVED = 3
    UPLOADED = 4
    LIKED = 5
    SHARED = 6
    DELETE = -1


class ActionFile(IntEnum):
    REMOVELIKED = 0
    LIKED = 1
    REMOVESHARED = 2
    SHARED = 3