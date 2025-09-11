import easyocr
import os
import time
from pathlib import Path

# ✅ Initialize the OCR reader once (heavy operation)
reader = easyocr.Reader(["en"])

def extract_numbers_from_image(image_path: str) -> str:
    # Run OCR on the image (using the global reader)
    results = reader.readtext(image_path, detail=0)  # detail=0 gives only text
    return " ".join(results)

def process_images():
    root_dir = Path(__file__).resolve().parent
    while True:
        # List all .png files
        for file in os.listdir(root_dir):
            if file.lower().endswith(".png"):
                base_name = os.path.splitext(file)[0]
                txt_file = f"{base_name}.txt"

                # Only process if txt file doesn't exist
                if not os.path.exists(root_dir / txt_file):
                    image_path = root_dir / file
                    print(f"Processing {image_path}...")

                    try:
                        # Extract numbers
                        result = extract_numbers_from_image(str(image_path))

                        # Save result
                        with open(root_dir / txt_file, "w", encoding="utf-8") as f:
                            f.write(result)

                        # Delete processed image
                        # image_path.unlink(missing_ok=True)

                        print(f"Saved result to {txt_file}")
                    except Exception as e:
                        print(f"⚠️ Failed to process {image_path}: {e}")

        time.sleep(5)  # Run every 5s

if __name__ == "__main__":
    print("running...")
    process_images()