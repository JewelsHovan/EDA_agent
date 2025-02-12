from smolagents import tool, OpenAIServerModel
from PIL import Image
import io
import base64

@tool
def analyze_image(image_path: str, query: str) -> str:
    """
    Analyze an image and return a description of the image based on the query.

    Args:
        image_path: The path to the image file.
        query: The question or description you want to know about the image.
    """
    try:
        model = OpenAIServerModel(model_id="gpt-4o-mini")

        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Convert image to RGB if it is in a mode (e.g., RGBA) that is not compatible with JPEG
        if image.mode in ("RGBA", "LA"):
            image = image.convert("RGB")
            
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{img_str}"},
                    },
                ],
            }
        ]

        response = model(messages)
        return response.content

    except Exception as e:
        return f"Error analyzing image: {e}"
