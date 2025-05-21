import streamlit as st
from fpdf import FPDF
import re
from datetime import date
import fitz  # PyMuPDF for PDF text extraction
from groq import Groq

# --- GROQ SETUP ---
client = Groq(api_key="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")

# --- Extract text from uploaded PDF ---
def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# --- Extract candidate name from CV text ---
def extract_name(cv_text):
    lines = cv_text.strip().splitlines()
    for line in lines:
        # Heuristic: first non-empty line with 2 or 3 words and capitalized
        if line.strip() and 2 <= len(line.strip().split()) <= 3 and line[0].isupper():
            return line.strip()
    return "Candidate Name"

# --- Extract email from CV text ---
def extract_email(cv_text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", cv_text)
    return match.group(0) if match else "email@example.com"

# --- Generate proposal using Groq + LLaMA ---
def generate_proposal(cv_text, job_title):
    prompt = f"""You are a professional assistant helping a candidate apply for jobs.

Based on the following CV:\n\n{cv_text}\n\n
Write a formal job proposal tailored for the position of '{job_title}'.
Keep it concise, persuasive, and professional."""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# --- Save proposal to PDF ---
def save_to_pdf(proposal_text, filename, candidate_name):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, "Job Proposal", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Times", size=12)
    for paragraph in proposal_text.strip().split("\n\n"):
        pdf.multi_cell(0, 8, paragraph.strip())
        pdf.ln(2)

    pdf.ln(10)
    pdf.set_font("Times", 'I', 12)
    pdf.cell(0, 10, "Sincerely,", ln=True)
    pdf.ln(10)
    pdf.cell(0, 10, candidate_name, ln=True)

    pdf.set_y(-15)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(150)
    pdf.cell(0, 10, "Generated using Groq + LLaMA 3", align="C")

    pdf.output(filename)


# --- Streamlit UI ---
st.set_page_config(page_title="Job Proposal Generator", layout="centered")
st.title("📄 Job Proposal Generator")
st.write("Upload your CV (PDF) and enter the position you're applying for. A formal proposal will be generated.")

cv_file = st.file_uploader("Upload your CV (PDF format)", type=["pdf"])
job_title = st.text_input("Job Title You're Applying For")

if st.button("Generate Proposal") and cv_file and job_title:
    with st.spinner("Extracting text from PDF and generating proposal..."):
        pdf_bytes = cv_file.read()
        cv_text = extract_text_from_pdf(pdf_bytes)
        name = extract_name(cv_text)
        email = extract_email(cv_text)
        proposal = generate_proposal(cv_text, job_title)
        save_to_pdf(proposal, "proposal.pdf", name)

    st.success("✅ Proposal generated successfully!")
    with open("proposal.pdf", "rb") as f:
        st.download_button("📥 Download Proposal PDF", f, file_name="proposal.pdf", mime="application/pdf")
