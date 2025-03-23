from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline

# Load models (CPU mode)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)
sentiment_analyzer = pipeline(
    "text-classification", model="ProsusAI/finbert", device=-1, batch_size=8
)
keyphrase_classifier = pipeline(
    "zero-shot-classification", model="facebook/bart-large-mnli", device=-1
)

# Predefined labels for zero-shot classification (topics)
LABELS = [
    "Financial Growth",
    "Stock Market Performance",
    "Regulatory Issues",
    "Legal Disputes",
    "Public Sentiment & Protests",
    "Government Policies",
    "Technological Innovations",
    "Market Competition",
    "Leadership Decisions",
]


def split_text(text, max_length=1024):
    """Splits text into chunks of max_length without breaking words."""
    words, chunks, current_chunk = text.split(), [], []

    for word in words:
        current_chunk.append(word)
        if len(" ".join(current_chunk)) > max_length:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def get_weighted_sentiment(sentiment_results):
    """Aggregates sentiment scores and returns the dominant sentiment."""
    sentiment_scores = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}

    for result in sentiment_results:
        for entry in result:
            label = entry["label"].upper()
            if label in sentiment_scores:
                sentiment_scores[label] += entry["score"]

    return max(sentiment_scores, key=sentiment_scores.get)


def summarize_text(text):
    """Generates a summary of the input text."""
    return summarizer(text, max_length=200, min_length=100, do_sample=False)[0][
        "summary_text"
    ]


def analyze_sentiments(chunks):
    """Performs sentiment analysis using FinBERT on chunked text."""
    sentiment_results = sentiment_analyzer(chunks, batch_size=8)
    return get_weighted_sentiment([sentiment_results])


def extract_topics(summary):
    """Extracts top 2 relevant topics using zero-shot classification on the summary."""
    response = keyphrase_classifier(summary, LABELS, multi_label=True)
    return sorted(
        response["labels"],
        key=lambda x: response["scores"][response["labels"].index(x)],
        reverse=True,
    )[:2]


def process_article(text):
    """Processes an article to extract summary, sentiment, and key topics efficiently."""
    text = text[:3200]
    chunks = split_text(text, max_length=1024)

    # Run tasks in parallel with 4 threads
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_summary = executor.submit(summarize_text, text)
        future_sentiments = executor.submit(analyze_sentiments, chunks)

        summary = future_summary.result()
        sentiment = future_sentiments.result()
        topics = extract_topics(summary)

    return {"Summary": summary, "Sentiment": sentiment, "Topics": topics}