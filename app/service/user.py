import logging
from sqlalchemy import and_, asc
from app.model import User
from sqlalchemy.orm import Session
from app.dto.core.auth import UserDTO
from app.dto.core.user import UserDTO, GetListUserResponse

_logger = logging.getLogger(__name__)

class UserService:    
    @classmethod
    def get_list_user(cls, db: Session, user: UserDTO):
        users = User.q(db, and_(User.email != user.email, User.deleted_at.is_(None))) \
                    .order_by(asc(User.id))
        list_users = []
        for user in users:
            user = UserDTO(**user.to_dict())
            list_users.append(user)
        return GetListUserResponse(users=list_users)
