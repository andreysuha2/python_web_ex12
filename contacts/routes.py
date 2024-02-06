from fastapi import APIRouter, HTTPException, Depends, status
from app.types import DBConnectionDep
from typing import Annotated, List
from contacts.controllers import ContactController 
from contacts import schemas

router = APIRouter(prefix='/contacts', tags=['contacts'])
ContactControllerDep = Annotated[ContactController, Depends(ContactController)]

@router.get('/', response_model=List[schemas.ContactResponse])
async def contacts_list(controller: ContactControllerDep, db: DBConnectionDep, q: str = '', skip: int = 0, limit: int = 100):
    return await controller.list(skip=skip, limit=limit, db=db, q=q)

@router.post('/', response_model=schemas.ContactResponse)
async def create_contact(controller: ContactControllerDep, db: DBConnectionDep, body: schemas.ContactModel):
    return await controller.create(body, db)

@router.get('/upcoming_birthdays', response_model=List[schemas.ContactResponse])
async def get_upcoming_birthdays(controller: ContactControllerDep, db: DBConnectionDep, days: int = 7):
    return await controller.upcoming_birthdays(db, days)

@router.get('/{contact_id}', response_model=schemas.ContactResponse)
async def read_contact(controller: ContactControllerDep, db: DBConnectionDep, contact_id: int):
    contact = await controller.read(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact

@router.put('/{contact_id}', response_model=schemas.ContactResponse)
async def update_contact(controller: ContactControllerDep, db: DBConnectionDep, body: schemas.ContactModel, contact_id: int):
    contact = await controller.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return contact

@router.delete('/{contact_id}', response_model=schemas.ContactResponse)
async def delete_contact(controller: ContactControllerDep, db: DBConnectionDep, contact_id: int):
    contact = await controller.delete(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return contact