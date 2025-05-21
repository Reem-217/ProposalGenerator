# 📄 AI Job Proposal Generator

This is a simple web app that generates a **formal, tailored job proposal** from a user's CV (in PDF format) and the job title they’re applying for. The app uses **Groq's LLaMA 3** to write high-quality proposals and **Streamlit** for the UI.

---

## 🚀 Features

* Upload a PDF resume.
* Enter a desired job title.
* Automatically:

  * Extracts text from the CV.
  * Identifies the candidate's name.
  * Generates a personalized job proposal using **LLaMA 3 via Groq**.
  * Formats the proposal into a clean **PDF**.

---

##  Tech Stack

* **Python**
* **Streamlit** – UI
* **PyMuPDF** (`fitz`) – Extract text from PDF
* **FPDF** – Create styled PDF files
* **Groq + LLaMA 3** – Generate proposal using AI

---


