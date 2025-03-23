import gradio as gr
import requests

# API endpoint for analysis
API_URL = "http://127.0.0.1:8000/analyze_articles/"


def analyze_tesla_articles(company):
    """Fetches, processes, and analyzes news articles for the selected company."""
    payload = {"company_name": company}

    # Send a POST request to the FastAPI server
    response = requests.post(API_URL, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data["analysis_data"], data["audio_file"]
    return {"Error": "Something went wrong with the API"}, None


# Gradio Interface with dropdown
iface = gr.Interface(
    fn=analyze_tesla_articles,
    inputs=gr.Dropdown(
        ["Apple", "Google", "McDonald's", "Tesla", "Starbucks"], label="Select a Company"
    ),
    outputs=[
        "json",  # JSON output of sentiment analysis
        gr.Audio(type="filepath"),  # Hindi TTS output
    ],
    title="Company News Sentiment Analysis",
    description="Select a company to fetch news, analyze sentiment, and get a Hindi audio summary.",
)

# Launch the Gradio app
iface.launch()