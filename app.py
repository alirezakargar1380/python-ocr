import easyocr
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import time
from PIL import Image

POST_URL = "https://tracking.post.ir"


def extract_numbers_from_image(image_path: str):
    # Initialize the reader (English by default)
    reader = easyocr.Reader(["en"])

    # Run OCR on the image
    results = reader.readtext(image_path, detail=0)  # detail=0 gives only text

    # Combine all detected text into a single string
    text = " ".join(results)
    return text


app = FastAPI()
app.mount("/api", app)


@app.post("/extract-number")
async def extract_number_api(file: UploadFile = File(...)):
    temp_path = Path(f"temp_{file.filename}")
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        result = extract_numbers_from_image(str(temp_path))
    finally:
        temp_path.unlink(missing_ok=True)
    return JSONResponse(content={"number": result})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
