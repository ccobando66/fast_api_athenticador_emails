from fastapi import FastAPI
from routers import(
    user_route,auth_route
)
import uvicorn


app = FastAPI()
app.title = "Email Authenticate"
app.version = "0.0.1"

globa_prefix = "/api/v1"
app.include_router(
    user_route.user,
    prefix=f"{globa_prefix}/user",
    tags=['User']
    )

app.include_router(
    auth_route.auth,
    prefix=f"{globa_prefix}/auth",
    tags=['Auth']
    )



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
         reload=True
    )