import uvicorn

if __name__ == "__main__":
    uvicorn.run("weather.app:app", host="localhost", port=8080, reload=True)