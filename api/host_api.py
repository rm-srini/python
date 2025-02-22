from fastapi import FastAPI

app = FastAPI()

@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
