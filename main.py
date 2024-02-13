from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bye"}

@app.get("/oop")
async def worst_subject():
    return {"message": "Worst subject ever"}