# News Summarization and Sentiment Analysis with TTS

## Overview
This project fetches news articles, summarizes them, performs sentiment analysis, extracts topics, and provides a Hindi text-to-speech (TTS) summary. The backend is built using **FastAPI**, and the frontend uses **Gradio** for a simple web interface.

## Features
- **News Fetching:** Scrapes news articles from **BBC News**.
- **Summarization:** Uses `facebook/bart-large-cnn` for text summarization.
- **Sentiment Analysis:** Uses `distilbert-base-uncased-finetuned-sst-2-english` for sentiment classification.
- **Topic Extraction:** Uses **BERTopic** to extract key topics from summaries.
- **Comparative Sentiment Analysis:** Analyzes sentiment trends across multiple articles.
- **Translation & TTS:** Translates final sentiment insights to Hindi and converts them to speech.
- **API Development:** Backend API built using **FastAPI**.
- **Web Interface:** Uses **Gradio** for a user-friendly interface.
- - **Performance Optimization:** **Threading** is employed for faster task execution, enabling parallel processing of sentiment analysis, summarization, and topic extraction tasks.

---

## Performance Optimization with Threading

To enhance performance, threading is used in various parts of the application to handle multiple tasks concurrently. For example:

- **Summarization and Sentiment Analysis:** Tasks such as summarizing the text and analyzing sentiments are processed concurrently, reducing the overall time needed for these operations.
  
- **Comparative Sentiment Analysis and Topic Overlap:** Sentiment distribution, thematic comparisons, and topic overlap are all handled concurrently, further speeding up the analysis process.

This concurrent processing approach significantly improves the efficiency and responsiveness of the system

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
FastAPI will start at `http://127.0.0.1:8000`.

### 5. Run the Gradio Frontend
```bash
python app.py
```
Gradio will launch at a local web address.

---

## API Endpoints

### 1. Health Check
**GET `/`**
- Response: `{ "message": "Hello, World!" }`

### 2. Analyze Articles
**POST `/analyze_articles/`**
- **Request Body:**
  ```json
  {
      "company_name": "Tesla"
  }
  ```
- **Response:**
  ```json
  {
      "analysis_data": { ... },
      "audio_file": "path/to/audio.mp3",
      "translated_text": "Hindi summary"
  }
  ```

---

## Assumptions & Limitations
- **Topic extraction is performed on the summary** instead of the full text to improve efficiency.
- **Limited labels for classification** to optimize processing time.
- **Only the first 3200 words** of each article are processed for better performance.
- **All articles are from BBC News** to simplify scraping.
- **Hugging Face Transformers and Pipelines are used** for summarization, sentiment analysis, and topic extraction.

---

## Future Enhancements
- Support for more news sources.
- Improve Hindi translation accuracy.
- Optimize performance for large-scale analysis.

---

## Contributing
Feel free to submit pull requests or report issues.

---

## License
This project is licensed under the MIT License.

