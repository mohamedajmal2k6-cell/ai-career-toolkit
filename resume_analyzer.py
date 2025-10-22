import pdfplumber
from PIL import Image
import pytesseract
import io

# If Tesseract is not in PATH, set it here:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(file):
    """Extract text from PDF or image using lightweight tools."""
    text = ""

    if file.name.lower().endswith(".pdf"):
        try:
            # Try extracting text directly
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            # If PDF has no text, convert first page to image and OCR
            if not text.strip():
                file.seek(0)
                from pdf2image import convert_from_bytes
                pages = convert_from_bytes(file.read(), dpi=200)
                if pages:
                    text = pytesseract.image_to_string(pages[0])
        except Exception as e:
            print("PDF Extraction Error:", e)
            text = ""

    else:  # image file
        try:
            file.seek(0)
            image = Image.open(io.BytesIO(file.read())).convert("RGB")
            text = pytesseract.image_to_string(image)
        except Exception as e:
            print("Image OCR Error:", e)
            text = ""

    return text.strip()


def analyze_resume(text):
    """Analyze resume text and provide ATS-style feedback."""
    text_lower = text.lower()

    frontend_skills = ["html", "css", "javascript", "react", "tailwind", "bootstrap", "typescript"]
    prompt_skills = ["prompt engineering", "openai", "llm", "langchain", "vertex ai", "gpt"]
    general_skills = ["python", "git", "teamwork", "machine learning", "data analysis", "streamlit"]

    all_skills = frontend_skills + prompt_skills + general_skills
    found_skills = [s for s in all_skills if s in text_lower]
    missing_skills = [s for s in all_skills if s not in text_lower]

    feedback = []
    if not found_skills:
        feedback.append("❌ No technical skills found. Try adding tools or technologies you know.")
    else:
        feedback.append(f"✅ Skills detected: {', '.join(found_skills)}")

    if missing_skills:
        feedback.append(f"🧩 Missing or not mentioned: {', '.join(missing_skills[:5])}")

    ats_score = int((len(found_skills) / len(all_skills)) * 100)
    ats_score = min(ats_score, 100)

    if ats_score < 50:
        feedback.append("⚙️ Improve your resume by adding more relevant keywords.")
    elif ats_score < 80:
        feedback.append("📈 Good! You can still refine some sections for better ATS matching.")
    else:
        feedback.append("🌟 Excellent! Your resume looks optimized for ATS systems.")

    return "\n".join(feedback), ats_score
