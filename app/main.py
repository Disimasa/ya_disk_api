from fastapi import FastAPI
from api.disk.controller import router as disk_router


app = FastAPI()
app.include_router(disk_router, prefix="/api/disk", tags=["DISK"])


@app.get('/')
async def index():
    return {'Hello': 'world'}
