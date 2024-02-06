from sqlalchemy.orm import Session
from fastapi import Depends
from app.db import get_db
from typing import Annotated

DBConnectionDep = Annotated[Session, Depends(get_db)]