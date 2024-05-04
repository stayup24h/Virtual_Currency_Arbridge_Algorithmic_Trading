import bithumbApi
import upbitApi

from fastapi import FastAPI
app = FastAPI()

from fastapi.responses import FileResponse

@app.get("/")
def main():
    return FileResponse('main.html')