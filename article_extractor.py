from newspaper import Article


def extract_article(url):

    try:

        article = Article(url)

        article.download()

        article.parse()

        text = article.text.strip()

        if len(text) < 300:
            return None

        return text

    except Exception as e:

        print("Article extraction failed:", e)

        return None
