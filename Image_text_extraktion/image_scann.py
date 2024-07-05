import easyocr
from PIL import Image

# Function to extract and format text from image
def extract_text_from_image(image_path):
    try:
        # Initialize easyocr reader
        reader = easyocr.Reader(['en'])
        # Read the image and extract text
        result = reader.readtext(image_path, detail=0)
        # Format text: convert to uppercase and join into paragraphs
        formatted_text = '\n\n'.join([text.upper() for text in result])
        return formatted_text
    except Exception as e:
        return str(e)

# Example usage
image_path = '009.jpg'
extracted_text = extract_text_from_image(image_path)
print(extracted_text)