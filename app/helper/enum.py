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