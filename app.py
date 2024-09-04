import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the Gemini model response
def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(input)
    # Handle the response structure properly
    return response  # Make sure this is the correct attribute

# Function to extract text from a PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        text += reader.pages[page].extract_text()
    return text

# Prompt template
input_prompt_template = """
Hey Act Like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science, 
data analysis, and big data engineering. Your task is to evaluate the resume based on 
the given job description. You must consider the job market is very competitive 
and you should provide the best assistance for improving the resume. Assign the percentage 
matching based on the JD and the missing keywords with high accuracy.
resume: {text}
description: {jd}

I want the response in one single string having the structure:
{{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
"""

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        text = input_pdf_text(uploaded_file)
        
        # Format the prompt with the extracted resume text and job description
        input_prompt = input_prompt_template.format(text=text, jd=jd)
        
        # Get the Gemini model response
        response = get_gemini_response(input_prompt)
        
        # Display the response in the Streamlit app
        st.subheader(response)
