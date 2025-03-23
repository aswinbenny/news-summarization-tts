import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


# Function to extract headline and content from a BBC article
def get_article_headline_and_content(url):
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the article: {url}")
        return None, None

    soup = BeautifulSoup(response.text, "lxml")

    # Extract the headline
    headline = soup.find("h1")
    headline = headline.text if headline else "No headline found"

    article_body = soup.find("article")  # Find the main article section
    if not article_body:
        return headline, "No article content found"

    paragraphs = article_body.find_all("p")  # Get only <p> inside <article>
    content = " ".join([p.text for p in paragraphs])  # Combine all paragraphs

    return headline, content


# Function to fetch multiple articles in parallel
def fetch_articles_parallel(article_urls):
    results = {}

    with ThreadPoolExecutor(max_workers=5) as executor:  # Using 5 threads
        future_to_url = {
            executor.submit(get_article_headline_and_content, url): url
            for url in article_urls
        }

        for future in future_to_url:
            url = future_to_url[future]
            try:
                headline, content = future.result()
                if headline and content:
                    results[url] = {"headline": headline, "content": content}
            except Exception as e:
                print(f"Error processing {url}: {e}")

    return results
