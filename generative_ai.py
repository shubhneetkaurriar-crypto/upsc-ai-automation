import os
from google import genai

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)


def analyze_news(title, description):

    prompt = f"""
You are a UPSC Civil Services current affairs expert.

Analyze this news article.

Title:
{title}

Description:
{description}

Return:

Important: Yes/No
GS Paper: GS1/GS2/GS3/GS4
Topic:
Short Note:
Prelims Facts:
Mains Angle:

Reject entertainment, sports, celebrity and irrelevant local news.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {e}"
