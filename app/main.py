import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.middleware.cors import CORSMiddleware

# Keycloak setup
from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="https://auth.ocf.berkeley.edu/auth/",
    client_id="ocfapi",
    realm_name="ocf",
)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# These URLs aren't completely necessary, but they let people authenticate from
# the /docs to test endpoints. Not sure how to get this working with Keycloak yet
oauth2_scheme = OAuth2AuthorizationCodeBearer(authorizationUrl="", tokenUrl="")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            + keycloak_openid.public_key()
            + "\n-----END PUBLIC KEY-----"
        )
        return keycloak_openid.decode_token(
            token,
            key=KEYCLOAK_PUBLIC_KEY,
            options={"verify_signature": True, "verify_aud": False, "exp": True},
        )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user")
async def get_user(current_user: dict = Depends(get_current_user)):
    logging.info(current_user)
    return current_user


# Some great reference reading: https://github.com/tiangolo/fastapi/issues/12
