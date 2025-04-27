import streamlit as st
from PIL import Image
import pytesseract

# Page configuration
st.set_page_config(page_title="Personal Loan Document Processing", page_icon="🏦")

# Title and instructions
st.title("🏦 Personal Loan Document Processing")
st.write("Upload your Loan Document (Only JPG, JPEG, or PNG)")

# File uploader
uploaded_file = st.file_uploader("Upload a loan document", type=["jpg", "jpeg", "png"])

# Processing the uploaded file
if uploaded_file is not None:
    try:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_column_width=True)

        # Extract text from the image
        with st.spinner("Extracting text from document..."):
            text = pytesseract.image_to_string(image)
        
        # Display extracted text
        st.subheader("Extracted Document Text:")
        st.text_area("Document Text", text, height=300)

    except Exception as e:
        st.error(f"Error processing the file: {e}")
