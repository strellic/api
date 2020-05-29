from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2

# Keycloak setup
from keycloak import KeycloakOpenID
keycloak_openid = KeycloakOpenID(server_url="https://auth.ocf.berkeley.edu/auth/",
                    client_id="ocfapi",
                    realm_name="ocf")

app = FastAPI()

oauth2_scheme = OAuth2()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        KEYCLOAK_PUBLIC_KEY = '-----BEGIN PUBLIC KEY-----\n' + keycloak_openid.public_key() + '\n-----END PUBLIC KEY-----'
        options = {"verify_signature": True, "verify_aud": False, "exp": True}
        return keycloak_openid.decode_token(token.split(" ")[1], key=KEYCLOAK_PUBLIC_KEY, options=options)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/")
async def root(current_user: dict = Depends(get_current_user)):
    return {"message": "Hello World"}

# Some great reference reading: https://github.com/tiangolo/fastapi/issues/12
