from fastapi import FastAPI
import redis
import uvicorn

app = FastAPI()
r = redis.Redis(host="redis", port=6379)

@app.get("/")
def read_root():
    return {"message": "Hello World! Gudss Change #10"}

@app.get("/hits")
def hits():
    r.incr("hits")
    return {"message": r.get("hits")}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)