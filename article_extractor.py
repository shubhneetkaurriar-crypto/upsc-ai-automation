from newspaper import Article


def extract_article(url):
    """
    Extract full article text from a news URL.
    Returns the article text or None if extraction fails.
    """

    try:
        article = Article(url)

        article.download()
        article.parse()

        text = article.text.strip()

        if len(text) < 300:
            print("Article too short.")
            return None

        return text

    except Exception as e:
        print("Article extraction failed:", e)
        return None


# -----------------------------
# TEST
# -----------------------------

if __name__ == "__main__":

    test_url = "https://pib.gov.in/PressReleasePage.aspx?PRID=2124786"

    article = extract_article(test_url)

    if article:
        print("\n========== ARTICLE ==========\n")
        print(article[:3000])      # Print first 3000 characters
        print("\n\nLength:", len(article))

    else:
        print("Extraction failed.")
