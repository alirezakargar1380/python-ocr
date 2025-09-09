import easyocr
import os
import time
from pathlib import Path

def extract_numbers_from_image(image_path: str) -> str:
    # Initialize the reader (English by default)
    reader = easyocr.Reader(["en"])

    # Run OCR on the image
    results = reader.readtext(image_path, detail=0)  # detail=0 gives only text

    # Combine all detected text into a single string
    text = " ".join(results)
    return text

def process_images():
    root_dir = "."
    while True:
        # List all .png files
        for file in os.listdir(root_dir):
            if file.lower().endswith(".png"):
                base_name = os.path.splitext(file)[0]
                txt_file = f"{base_name}.txt"

                # Only process if txt file doesn't exist
                if not os.path.exists(os.path.join(root_dir, txt_file)):
                    image_path = os.path.join(root_dir, file)
                    print(f"Processing {image_path}...")

                    # Extract numbers
                    result = extract_numbers_from_image(image_path)

                    # Save result
                    with open(os.path.join(root_dir, txt_file), "w", encoding="utf-8") as f:
                        f.write(result)
                        
                    temp_path = Path(f"{image_path}")
                    temp_path.unlink(missing_ok=True)    
                        
                    print(f"Saved result to {txt_file}")

        time.sleep(1)  # Run every 1s

if __name__ == "__main__":
    process_images()
