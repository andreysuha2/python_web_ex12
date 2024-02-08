from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
from typing import Optional
from enum import Enum
from app.settings import TOKEN_CONFIG, TokenConfig
from app.db import get_db
from users.models import User

class TokenScopes(Enum):
    ACCESS='access_token'
    REFRESH='refresh_token'

class Password:
    def __init__(self, pwd_context: CryptContext):
        self.pwd_context = pwd_context

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify(self, password: str, hash: str) -> bool:
        return self.pwd_context.verify(password, hash)
    
class Token:
    def __init__(self, config: TokenConfig, coder: jwt, coder_error: JWTError) -> None:
        self.config = config
        self.coder = coder,
        self.coder_error = coder_error
         
    async def create(self, data: dict, scope: TokenScopes, expires_delta: Optional[float] = None) -> str:
        to_encode_data = data.copy()
        now = datetime.utcnow()
        expired = now + timedelta(seconds=expires_delta) if expires_delta else now + timedelta(minutes=self.config.default_expired)
        to_encode_data.update({"iat": now, "exp": expired, "scope": scope.value})
        token = self.coder.encode(data, self.config.secret_key, algorithm=self.config.algorithm)
        return token
    
    async def decode(self, token: str, scope: TokenScopes) -> str:
        try:
            payload = self.coder.decode(token, self.config.secret_key, algorithms=[self.config.algorithm])
            if payload['scope'] == scope.value:
                return payload["sub"]
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except self.coder_error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    async def create_access(self, data: dict, expires_delta: Optional[float] = None) -> str:
        return self.create(data=data, scope=TokenScopes.ACCESS, expires_delta=expires_delta or self.config.access_expired)
    
    async def create_refresh(self, data: dict, expires_delta: Optional[float] = None) -> str:
        return self.create(data=data, scope=TokenScopes.REFRESH, expires_delta=expires_delta or self.config.refresh_expired)

    async def decode_access(self, token: str) -> str:
        return self.decode(token, TokenScopes.ACCESS)

    async def decode_refresh(self, token: str) -> str:
        return self.decode(token, TokenScopes.REFRESH)

class Auth:
    oauth2_scheme = OAuth2PasswordBearer(TOKEN_CONFIG.url)

    def __init__(self, password: Password, token: Token, user_model: User, credentionals_exception: HTTPException) -> None:
        self.password = password
        self.token = token
        self.user_model = user_model
        self.credentionals_exception = credentionals_exception

    async def __get_user(self, email: str, db: Session) -> User | None:
        return db.query(self.user_model).filter(self.user_model.email == email).first()

    async def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        email = self.token.decode_access(token)
        if email is None:
            raise self.credentionals_exception
        user = self.__get_user(email, db)
        if user is None:
            raise self.credentionals_exception
        return user
        

auth = Auth(
    password=Password(CryptContext(schemes=['bcrypt'])),
    token=Token(config=TOKEN_CONFIG, coder=jwt, coder_error=JWTError),
    user_model=User,
    credentionals_exception=HTTPException(
        status=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
)