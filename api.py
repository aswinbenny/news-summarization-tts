from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from article_analysis import process_article
from article_fetcher import get_article_headline_and_content
from sentiment_analysis import comparative_analysis
from hindi_translation_tts import translate_and_speak

# FastAPI App instance
app = FastAPI()


# Define a model to receive the company name
class CompanyRequest(BaseModel):
    company_name: str


# Dictionary of article IDs for each company
COMPANY_ARTICLES = {
    "Apple": [
        "c9vy0m8ggz3o", "c0l1kpz3w32o", "c8rkpv50x01o", "ce980m2xv30o", "c798xv5qwylo",
        "c4g0rr51gn3o", "clyjv8e49deo", "cn524lx9445o", "cvgw30dr0w3o", "c20g288yldko"
    ],
    "Google": [
        "c39v2ykwgdno", "ckgzm1lgv22o", "cm21g0052dno", "crlky380wd7o", "cp820m733p3o",
        "c3rw3e5je5po", "cy081nqx2zjo", "cx2j15r1g09o", "c5y6eq2zxlno", "c4g91kyjw07o"
    ],
    "McDonald's": [
        "cr423p4e7qdo", "ce34j3qpjqko", "c337m3v3mgzo", "c4gp2npen26o", "c4g007qgll8o",
        "ce8vdjd91z4o", "c5yr5xvkelzo", "cj3e6yrl5nlo", "cde9p7wld3wo", "c87dwrnplwdo"
    ],
    "Tesla": [
        "c0kgy20x0x4o", "cp8vd0j5zk2o", "c201z4lv5xxo", "cqjdg4x08ylo", "cnvze9dzq8vo",
        "cvgd9v3r69qo", "c204yvv1eexo", "cz61vwjel2zo", "crkn28dpl4no", "cvgm21zjggro"
    ],
    "Starbucks": [
        "cp3y0j558l7o", "czedrregr0wo", "c625n63epyzo", "c3rnq2lv1lzo", "c80yerynrp9o",
        "cy9lg8pgjreo", "cdxnv4rjdq4o", "cz0rp80er7jo", "cevgzweexdno", "cwy1jegx74jo"
    ],
}


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/analyze_articles/")
def analyze_articles(company_request: CompanyRequest):
    """Fetches, processes, and analyzes news articles for the selected company."""
    company = company_request.company_name

    if company not in COMPANY_ARTICLES:
        raise HTTPException(status_code=404, detail="Invalid company selection")

    article_ids = COMPANY_ARTICLES[company]
    articles_data = []

    # Fetch and process articles for the selected company
    for article_id in article_ids:
        article_url = f"https://www.bbc.com/news/articles/{article_id}"
        headline, content = get_article_headline_and_content(article_url)
        results = process_article(content)

        articles_data.append({
            "headline": headline,
            "Summary": results["Summary"],
            "Sentiment": results["Sentiment"],
            "Topics": results["Topics"],
        })

    # Perform comparative analysis
    analysis_data = {"Company": company, "Articles": articles_data}
    analysis_result = comparative_analysis(analysis_data)

    # Merge results into analysis_data
    analysis_data["Comparative Sentiment Score"] = analysis_result

    final_sentiment_analysis = analysis_result["Final Sentiment Analysis"]
    translated_text, audio_output = translate_and_speak(final_sentiment_analysis)

    return {
        "analysis_data": analysis_data,
        "audio_file": audio_output,  # Path to the audio file
        "translated_text": translated_text,
    }