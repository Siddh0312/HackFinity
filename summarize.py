import fitz  # PyMuPDF for PDF text extraction
import os
import re
from groq import Groq
from google.colab import files

# ✅ Set the GROQ API key (Ensure it's securely stored in your environment)
os.environ["GROQ_API_KEY"] = "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"

# ✅ Initialize GROQ client
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ✅ Function to Extract Sections Dynamically from PDF
def extract_sections_from_pdf(pdf_path):
    """Automatically detects section headers and extracts content section-wise, excluding references."""
    doc = fitz.open(pdf_path)
    full_text = "\n".join([page.get_text("text") for page in doc])

    sections = {}
    current_section = None
    exclude_sections = ["References", "Bibliography", "Citations"]  # Sections to exclude

    for line in full_text.split("\n"):
        line = line.strip()

        # 🔹 Automatically detect section headers
        if (
            len(line.split()) < 12  # Short lines are more likely to be titles
            and (line.isupper() or re.match(r"^\d+\.\s", line))  # Uppercase or numbered
        ):
            section_title = line.title().strip()  # Normalize case

            # Skip references or citation sections
            if section_title in exclude_sections:
                current_section = None  # Stop collecting data
            else:
                current_section = section_title
                sections[current_section] = []

        elif current_section:
            sections[current_section].append(line)

    # Convert lists into complete section text
    for section in sections:
        sections[section] = "\n".join(sections[section])

    return sections

# ✅ Function to Summarize Each Section Using Groq with More Detail
def summarize_section(section_name, section_text):
    """Generates a more detailed summary for each section using Groq’s Mixtral model."""
    prompt = [
      {
        "role": "system",
        "content": (
            "You are an advanced AI model specialized in summarizing research papers with exceptional accuracy. "
            "Your goal is to deliver comprehensive, well-structured summaries that cover all critical aspects, including:\n"
            "- Key points and core arguments\n"
            "- Research objectives and questions\n"
            "- Detailed methodology (study design, data collection, analysis techniques)\n"
            "- Major findings and results\n"
            "- Discussions, implications, and conclusions\n\n"
            "Ensure the summary maintains the original meaning, avoids missing any significant details, and presents information logically. "
            "Use clear, concise language suitable for academic and professional readers."
        )
    },
    {
        "role": "user",
        "content": (
            "Provide an in-depth, structured summary of the following section from a research paper:\n\n"
            f"**Section Title:** {section_name}\n\n"
            f"**Section Content:**\n{section_text}\n\n"
            "Ensure the summary highlights key details, critical data, and nuanced insights from the original text."
        )
    }
]


    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",  # Groq’s Mixtral model
        messages=prompt,
        max_tokens=1200,  # Increased token limit for detailed summaries
        temperature=0.2  # Lower temperature for factual summaries
    )

    return response.choices[0].message.content.strip()

# ✅ Function to Process & Summarize the Entire Paper
def summarize_research_paper(pdf_path):
    """Extracts and summarizes each dynamically detected section."""
    sections = extract_sections_from_pdf(pdf_path)
    summary_by_section = {}

    for section, text in sections.items():
        if text.strip():  # Only summarize non-empty sections
            print(f"⏳ Summarizing {section}...")
            summary_by_section[section] = summarize_section(section, text)

    return summary_by_section

# ✅ Upload and Process the PDF
uploaded = files.upload()
pdf_path = list(uploaded.keys())[0]  # Get uploaded file name

# ✅ Generate Section-wise Summaries
summarized_sections = summarize_research_paper(pdf_path)

# ✅ Save Summaries to a Text File
summary_filename = "detailed_section_summaries.txt"
with open(summary_filename, "w", encoding="utf-8") as f:
    for section, summary in summarized_sections.items():
        f.write(f"=== {section.upper()} ===\n{summary}\n\n")

# ✅ Provide Download Link for Summaries
files.download(summary_filename)
print("✅ Detailed section-wise summaries saved and ready for download!")
