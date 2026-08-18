import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

# Contexto de hashing con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
  """Hashea una contraseña en texto plano."""
  return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verifica una contraseña contra su hash."""
  return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
  """Crea un token JWT cifrado con expiración y payload."""
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + (
      expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt