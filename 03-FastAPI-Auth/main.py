from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import uvicorn

SECRET_KEY = "9588a517044c1da4bee1fcec316e9b166969c996b80aadd066f9e53b19ff4f2f4ff078a956543ad83d102531dd971a31cc42a4fecc4a99afbe94046c1f5c181bc22cebc6844a73afd69b0e731c1919d2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



db = {
    "tim":{
        "username" : "tim",
        "full_name" : "Tim Ruscica",
        "email" : "tim@gmail.com",
        "hashed_password" : "$2b$12$C.i5dqpYw7EzfoQxWwofmO6elkesidI1oGcT6DMovfpMsQvm3DxeG",
        "disabled" : False
    }
}

class User(BaseModel):
    username: str
    email: str or None = None
    full_name : str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username: str or None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()

#helper methods
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)


# Validate User
def authenticate_user(db, username: str, password: str):
    # 1. check user exists in our db
    user = get_user(db, username)
    if not user:
        return False

    # 2. check the provided password
    if not verify_password(password, user.hashed_password):
        return False
    return user

# generating token from payload
def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes = 15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):

    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    try:
        # 1. decoding provided jwt token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        # 2. creating a DTO.TokenData from username
        token_data = TokenData(username = username)

    except JWTError:
        raise credential_exception

    # 3. check username exists in DB
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credential_exception

    return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):

    if current_user.disabled:
        raise HTTPException(status_code=400, detail = "Inactive user")

    return current_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    # 1. Debug these methods for better understanding
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data = {"sub":user.username}, expires_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Change the function definition, play with authentication
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

# Check once:
#   1. Does debugging makes easier, or facing difficulty while running 
#   cmd: "uvicorn main:app --reload"

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info", reload=True)
