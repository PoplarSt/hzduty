from fastapi import FastAPI
import api.auto_code
app = FastAPI()
app.include_router(api.auto_code.router)
