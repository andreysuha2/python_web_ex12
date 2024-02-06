from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db import has_date_next_days
from contacts.models import Contact
from contacts import schemas
from typing import List

class ContactController:
    base_model = Contact

    async def list(self, q: str,  skip: int, limit: int, db: Session) -> List[Contact]:
        query = db.query(self.base_model)
        if q:
            query = query.filter(or_(Contact.first_name.like(f'{q}%'), Contact.last_name.like(f'{q}%'), Contact.email.like(f'{q}%')))
        return query.offset(skip).limit(limit).all()

    async def create(self, body: schemas.ContactModel, db: Session) -> Contact:
        contact = self.base_model(**body.model_dump())
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact
        
    async def read(self, id: int, db: Session) -> Contact |  None:
        return db.query(self.base_model).filter(self.base_model.id == id).first()
    
    async def update(self, id: int, body: schemas.ContactModel, db: Session) -> Contact | None:
        contact = db.query(self.base_model).filter(self.base_model.id == id).first()
        if contact:
            for key, value in body.model_dump().items():
                setattr(contact, key, value)
            db.commit()
        return contact
    
    async def delete(self, id: int, db: Session) -> Contact | None:
        contact = db.query(self.base_model).filter(self.base_model.id == id).first()
        if contact:
            db.delete(contact)
            db.commit()
        return contact
    
    async def upcoming_birthdays(self, db: Session, days: int = 7) -> List[Contact]:
        return db.query(Contact).filter(has_date_next_days(Contact.birthday, days)).all()