from users.models import User
from sqlalchemy.orm import Session

class UserController:
    base_model = User

    async def get_user_by_email(self, email: str, db: Session) -> User | None:
        return db.query(self.base_model).filter(self.base_model.email == email).first()