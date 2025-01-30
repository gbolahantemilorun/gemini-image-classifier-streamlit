import streamlit as st
import google.generativeai as genai
import PIL.Image
import json
import os
from dotenv import load_dotenv

# Load the env variables
load_dotenv(dotenv_path="/etc/secrets/.env")
GOOGLE_API_KEY = os.getenv["GOOGLE_API_KEY_1"]

# Configure the Gemini model with the API key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit app
st.title("Image Categorization with Gemini")

# File uploader for image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Process the image if uploaded
if uploaded_file is not None:
    # Open the uploaded image
    image = PIL.Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Generate content using the Gemini model
    try:
        response = model.generate_content([
            "Analyze the following image and provide a description of its content. "
            "Then categorize it into one of the following categories: "
            "Market: A busy commercial marketplace where goods are bought and sold, "
            "Market Pitch: A specific area in a marketplace where a seller sets up their stall, "
            "Isolated Pitch: A solitary selling location outside a marketplace, often on the street, "
            "Unlicensed Street Seller: A street vendor selling goods without a license, "
            "or Unknown. Respond in JSON format with "
            "'Category' and 'Description' fields.",
            image
        ])

        # Parse the response as JSON (if it isn't already a valid JSON)
        try:
            result = response.text
            # Remove any non-JSON characters (like markdown or code blocks)
            cleaned_result = result.replace("```json", "").replace("```", "").strip()

            # Attempt to load the cleaned result as a JSON object
            result_json = json.loads(cleaned_result)

            # Display the formatted JSON response
            st.json(result_json)

        except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON response: {str(e)}")
            st.text(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")