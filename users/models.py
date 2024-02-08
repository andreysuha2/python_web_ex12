from app.db import Base
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String) 