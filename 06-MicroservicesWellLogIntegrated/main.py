from fastapi import FastAPI
from routerLog import router as log_route

app = FastAPI()
app.include_router(log_route)

@app.get("/")
async def read_main():
  return{"message": "Hello World!"}