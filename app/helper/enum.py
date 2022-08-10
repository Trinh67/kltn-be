from enum import Enum, IntEnum


class ObjectNotFoundType(Enum):
    USER = "User"


class UserSource(Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"