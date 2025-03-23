# News Summarization and Sentiment Analysis with TTS

## Overview
This project fetches news articles, summarizes them, performs sentiment analysis, extracts topics, and provides a Hindi text-to-speech (TTS) summary. The backend is built using FastAPI, and the frontend uses Gradio for a simple web interface.

## Features
- **News Fetching:** Scrapes news articles from BBC News.
- **Summarization:** Uses `facebook/bart-large-cnn` for text summarization.
- **Sentiment Analysis:** Uses `ProsusAI/finbert` for financial sentiment classification.
- **Topic Extraction:** Uses `facebook/bart-large-mnli` for zero-shot classification of key topics from summaries.
- **Comparative Sentiment Analysis:** Analyzes sentiment trends across multiple articles.
- **Translation & TTS:** Translates final sentiment insights to Hindi using `deep_translator` and converts them to speech with `gTTS`.
- **API Development:** Backend API built using FastAPI.
- **Web Interface:** Uses Gradio for a user-friendly interface.
- **Performance Optimization:** Threading is used to speed up execution, enabling parallel processing of tasks.

## Live Demo
Try the deployed version here : **[Hugging Face Spaces Deployment](https://huggingface.co/spaces/aswinbenny/news-sentiment-analysis)**

## Performance Optimization with Threading
To enhance performance, threading is employed to handle multiple tasks concurrently, reducing processing time for:
- **Summarization and Sentiment Analysis**
- **Comparative Sentiment Analysis and Topic Overlap**

This improves efficiency and responsiveness.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/aswinbenny/news-summarization-tts.git
cd news-summarization-tts
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI Backend
```bash
uvicorn api:app --reload
```
FastAPI will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 5. Run the Gradio Frontend
```bash
python app.py
```
Gradio will launch at a local web address.

---

## API Endpoints

### 1. **Health Check**
**GET /**
#### Response:
```json
{ "message": "Hello, World!" }
```

### 2. **Analyze Articles**
**POST /analyze_articles/**
#### Request Body:
```json
{
    "company_name": "Tesla"
}
```
#### Response:
```json
{
    "analysis_data": { ... },
    "audio_file": "output_hindi.mp3",
    "translated_text": "Hindi summary"
}
```

---

## Model Details
### 1. **Summarization**  
- **Model:** `facebook/bart-large-cnn`
- **Function:** Generates concise summaries of news articles.

### 2. **Sentiment Analysis**  
- **Model:** `ProsusAI/finbert`
- **Function:** Classifies sentiment as positive, negative, or neutral with a financial focus.

### 3. **Topic Extraction**  
- **Model:** `facebook/bart-large-mnli`
- **Function:** Performs zero-shot classification to extract key topics from summaries.

### 4. **Translation & TTS**  
- **Library:** `deep_translator`
- **Function:** Translates English text to Hindi.
- **Library:** `gTTS`
- **Function:** Converts Hindi text into speech and saves as `output_hindi.mp3`.

---

## Assumptions & Limitations
- **Topic extraction is performed on the summary** instead of the full text for efficiency.
- **Limited labels for zero-shot classification** to optimize processing time.
- **Only the first 3200 words** of each article are processed for better performance.
- **Articles are sourced from BBC News** for easier scraping using a single URL pattern.
- **Hugging Face Transformers and Pipelines** are used for summarization, sentiment analysis, and topic extraction.

---

## Future Enhancements
- Support for more news sources.
- Improve Hindi translation accuracy.
- Optimize performance for large-scale analysis.

---

## API Usage
- **Backend:** FastAPI serves endpoints for processing articles.
- **Frontend:** Gradio interacts with the API and displays results.
- **How to Test:** Use Postman or `curl` commands to send requests to `http://127.0.0.1:8000/analyze_articles/`.

---

## Contributing
Feel free to submit pull requests or report issues.

---

## License
This project is licensed under the **MIT License**.

