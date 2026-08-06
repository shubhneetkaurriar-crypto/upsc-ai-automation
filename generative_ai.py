import os
import google.generativeai as genai

# Connect Gemini API
genai.configure(
    api_key=os.environ.get("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def analyze_news(title, description):

    prompt = f"""
You are a UPSC Civil Services current affairs expert.

Analyze this news article:

Title:
{title}

Description:
{description}

Decide whether this is useful for UPSC.

Return in this format:

Important: Yes/No
GS Paper: GS1/GS2/GS3/GS4
Topic:
Short Note:
Prelims Facts:
Mains Angle:

Reject:
- entertainment
- sports
- celebrity news
- irrelevant local news
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"AI Error: {e}"
