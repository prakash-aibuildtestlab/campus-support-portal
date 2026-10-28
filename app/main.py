from fastapi import FastAPI
from pathlib import Path

from fastapi.responses import FileResponse

app = FastAPI(
    title="Campus Support Portal",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}

### 2
STATIC_DIR = Path(__file__).resolve().parent / "static"  #Locates the HTML relative to the Python file

#app.get Handles requests to the website’s root URL 
#file response - Sends the HTML file to the browser
#include_in_schema=False - Keeps this website route out of the API documentation
@app.get("/", response_class=FileResponse, include_in_schema=False)
def home():
    """Serve the Campus Support Portal landing page."""
    return FileResponse(STATIC_DIR / "index.html")