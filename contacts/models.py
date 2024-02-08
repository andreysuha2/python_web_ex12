from app.db import Base
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date

class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False) 
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=True)
    additional_data: Mapped[str] = mapped_column(String, nullable=True)
    