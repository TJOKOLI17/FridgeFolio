from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .items_router import router as items_router
from .users_router import router as users_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the origin as necessary
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

app.include_router(items_router)
app.include_router(users_router)



@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the FridgeFolio API"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
