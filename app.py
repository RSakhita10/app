
import streamlit as st
import pytesseract
import cv2
import re
import json
import tempfile
import os

# Preprocessing function
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

# OCR Extraction
def extract_text(image):
    text = pytesseract.image_to_string(image)
    return text

# Field Extraction
def extract_fields(text):
    fields = {}
    name_match = re.search(r"Name[:\s]*(.*)", text)
    address_match = re.search(r"Address[:\s]*(.*)", text)
    income_match = re.search(r"Income[:\s]*([\d,]+)", text)
    loan_amount_match = re.search(r"Loan Amount[:\s]*([\d,]+)", text)

    fields['Name'] = name_match.group(1) if name_match else ''
    fields['Address'] = address_match.group(1) if address_match else ''
    fields['Income'] = income_match.group(1) if income_match else ''
    fields['Loan Amount'] = loan_amount_match.group(1) if loan_amount_match else ''

    return fields

# Save Data
def save_to_system(data, filename="loan_applications.json"):
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            json.dump([], f)

    with open(filename, "r+") as f:
        file_data = json.load(f)
        file_data.append(data)
        f.seek(0)
        json.dump(file_data, f, indent=4)

# Streamlit UI
st.title("🏦 Personal Loan Document Processing")

uploaded_file = st.file_uploader("Upload your Loan Document (Image/PDF)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    processed_img = preprocess_image(temp_file_path)
    extracted_text = extract_text(processed_img)
    fields = extract_fields(extracted_text)

    st.subheader("Extracted Fields (You can edit them):")
    name = st.text_input("Name", value=fields['Name'])
    address = st.text_input("Address", value=fields['Address'])
    income = st.text_input("Income", value=fields['Income'])
    loan_amount = st.text_input("Loan Amount", value=fields['Loan Amount'])

    if st.button("Submit Data"):
        final_data = {
            "Name": name,
            "Address": address,
            "Income": income,
            "Loan Amount": loan_amount
        }
        save_to_system(final_data)
        st.success("✅ Data saved successfully!")
