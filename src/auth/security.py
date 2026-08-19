import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from dotenv import load_dotenv
from jose import JWTError, jwt

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
)
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def hash_password(password: str) -> str:
  """Hashea una contraseña en texto plano."""
  pwd_bytes = password.encode("utf-8")
  salt = bcrypt.gensalt()
  hashed = bcrypt.hashpw(pwd_bytes, salt)
  return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
  """Verifica una contraseña contra su hash."""
  pwd_bytes = plain_password.encode("utf-8")
  hashed_bytes = hashed_password.encode("utf-8")
  return bcrypt.checkpw(pwd_bytes, hashed_bytes)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
  """Crea un token JWT cifrado con expiración y payload."""
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + (
      expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  )
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt