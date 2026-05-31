import uvicorn

# Run the FastAPI server locally
# Command: py run.py
# Or: python run.py
# Then open: http://127.0.0.1:8000/docs

if __name__ == "__main__":
    uvicorn.run("app.api.api:app", reload=True)