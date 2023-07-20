from fastapi import FastAPI

app = FastAPI()

@app.post("/string_length")
async def get_string_length(string: str):
    return {"length": len(string)}
