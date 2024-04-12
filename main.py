from fastapi import FastAPI
from pydantic import BaseModel
import AuthSC as sc
from fastapi.middleware.cors import CORSMiddleware
class Wallet(BaseModel):
    pk: str
    privKey: str



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/connect")
async def connect(wallet:Wallet):
     if(sc.verify_keys(wallet.pk,wallet.privKey) and sc.containAdmin(wallet.pk)):
          return {"authentication": "Success"}
     return {"authentication":"failed"}
    