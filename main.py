import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from api.auth import router as auth_router
from api.feeds import router as feeds_router
from api.snaps import router as photos_router
from api.users import router as users_router

app = FastAPI(title="Moment", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    print("started")


@app.get("/")
async def docs():
    return RedirectResponse(url="/docs")


@app.on_event("shutdown")
async def shutdown():
    print("shutdown")


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(photos_router.router)
app.include_router(feeds_router.router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
