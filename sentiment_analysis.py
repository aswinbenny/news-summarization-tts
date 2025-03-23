from collections import Counter
import random
from concurrent.futures import ThreadPoolExecutor


def generate_final_sentiment(sentiment_counts, company):
    """Generates a final sentiment summary based on the dominant sentiment."""
    dominant_sentiment = max(sentiment_counts, key=sentiment_counts.get)

    sentiment_phrases = {
        "POSITIVE": (
            f"{company}’s latest news coverage is mostly positive. "
            "Potential stock growth expected."
        ),
        "NEGATIVE": (
            f"{company}’s recent news coverage is largely negative. "
            "Market confidence may decline."
        ),
        "NEUTRAL": (
            f"{company}’s news coverage remains neutral. "
            "Investors may adopt a wait-and-see approach."
        ),
    }

    return sentiment_phrases[dominant_sentiment]


def compute_sentiment_distribution(sentiments):
    """Computes sentiment distribution."""
    sentiment_counts = Counter(sentiments)
    return {
        "POSITIVE": sentiment_counts.get("POSITIVE", 0),
        "NEGATIVE": sentiment_counts.get("NEGATIVE", 0),
        "NEUTRAL": sentiment_counts.get("NEUTRAL", 0),
    }


def compute_thematic_comparison(themes):
    """Generates a comparative thematic summary."""
    connection_words = ["while", "whereas", "however", "on the other hand"]
    conjunctions = [
        "is about", "focuses on", "discusses",
        "highlights", "explores", "centers on"
    ]

    theme_sentences = []
    for i in range(len(themes) - 1):
        conj = random.choice(conjunctions)
        conn_word = random.choice(connection_words)
        theme_sentences.append(f"Article {i+1} {conj} {themes[i]}, {conn_word}")

    # Last article sentence without a connection word
    if len(themes) > 1:
        last_article_num = len(themes)
        last_conj = random.choice(conjunctions)
        last_sentence = (
            f"Article {last_article_num} {last_conj} {themes[last_article_num - 1]}."
        )
        theme_sentences.append(last_sentence)

    return " ".join(theme_sentences)  # Concatenate into a single sentence


def compute_topic_overlap(topics_list, articles_data):
    """Finds common and unique topics across articles."""
    all_topics = [topic for topics in topics_list.values() for topic in topics]

    # Count occurrences of each topic
    topic_counts = Counter(all_topics)

    # Identify common topics (topics appearing in ALL articles)
    common_topics = {
        topic for topic, count in topic_counts.items() if count == len(articles_data)
    }

    # Identify unique topics for each article
    unique_topics = {
        f"Unique Topics in Article {i+1}": list(topics - common_topics)
        if topics - common_topics else []
        for i, topics in topics_list.items()
    }

    return {
        "Common Topics": list(common_topics),
        **unique_topics,
    }


def comparative_analysis(analysis_data):
    """
    Performs comparative sentiment analysis and thematic classification.

    Args:
        analysis_data (dict): Dictionary containing summaries, sentiments,
        and topics of articles.

    Returns:
        dict: Analysis results including sentiment distribution
        and comparative thematic insights.
    """
    articles_data = analysis_data["Articles"]
    company = analysis_data["Company"]
    sentiments = []
    themes = {}
    topics_list = {}

    for i, article in enumerate(articles_data):
        sentiments.append(article["Sentiment"])
        themes[i] = article["Topics"][0]
        topics_list[i] = set(article["Topics"])

    # Execute sentiment analysis, thematic comparison, and topic overlap in parallel
    with ThreadPoolExecutor() as executor:
        future_sentiment_distribution = executor.submit(
            compute_sentiment_distribution, sentiments
        )
        future_thematic_comparison = executor.submit(
            compute_thematic_comparison, themes
        )
        future_topic_overlap = executor.submit(
            compute_topic_overlap, topics_list, articles_data
        )

        sentiment_distribution = future_sentiment_distribution.result()
        final_theme_comparison = future_thematic_comparison.result()
        topic_overlap = future_topic_overlap.result()

    final_sentiment_analysis = generate_final_sentiment(sentiment_distribution, company)

    analysis_result = {
        "Sentiment Distribution": sentiment_distribution,
        "Comparative Thematic Insights": final_theme_comparison,
        "Topic Overlap": topic_overlap,
        "Final Sentiment Analysis": final_sentiment_analysis,
    }

    return analysis_result
