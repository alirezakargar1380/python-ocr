import easyocr
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path

def extract_numbers_from_image(image_path: str):
    # Initialize the reader (English by default)
    reader = easyocr.Reader(['en'])
    
    # Run OCR on the image
    results = reader.readtext(image_path, detail=0)  # detail=0 gives only text
    
    # Combine all detected text into a single string
    text = " ".join(results)
    return text


app = FastAPI()
app.mount('/api', app)

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

