from sqlalchemy.orm import Session
from app.model.user import User


class UserProvider:
    @classmethod
    def create_user_model(cls, db: Session, commit: bool = False, **data) -> User:
        user = {
            'id': data.get('id', 1),
            "name": data.get("name", "Trinh"),
            "user_id": data.get("user_id", "123456789"),
            "email": data.get("email", "trinhtx.uet@gmail.com"),
            "avatar_url": data.get("avatar_url", "avatar"),
            "source": data.get("source", "google")
        }

        new_user: User = User.create(db, user, commit=commit)

        return new_user

