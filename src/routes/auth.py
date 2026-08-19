from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.security import create_access_token, hash_password, verify_password
from src.config.database import get_db
from src.models.user import Client
from src.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
  # 1. Verificar si el correo ya está registrado
  stmt = select(Client).where(Client.email == user_in.email)
  result = await db.execute(stmt)
  existing_user = result.scalar_one_or_none()

  if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="El correo electrónico ya se encuentra registrado",
    )

  # 2. Hashear la contraseña antes de guardar en BD
  hashed_pwd = hash_password(user_in.password)

  # 3. Crear nuevo usuario en BD usando 'hashed_password'
  new_user = Client(
      name=user_in.name,
      email=user_in.email,
      hashed_password=hashed_pwd,
      phone=getattr(user_in, "phone", None),
  )

  db.add(new_user)
  await db.commit()
  await db.refresh(new_user)

  return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
  # 1. Buscar usuario por email (username en OAuth2)
  stmt = select(Client).where(Client.email == form_data.username)
  result = await db.execute(stmt)
  user = result.scalar_one_or_none()

  # 2. Validar existencia y verificar contraseña comparando contra user.hashed_password
  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas",
        headers={"WWW-Authenticate": "Bearer"},
    )

  # 3. Generar token JWT
  access_token = create_access_token(
      data={"sub": user.email, "role": getattr(user, "role", "Cliente")}
  )

  return {"access_token": access_token, "token_type": "bearer"}