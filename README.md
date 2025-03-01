# 🎥 YouTube Comment Sentiment Analysis

## 📌 Description

The **YouTube Comment Sentiment Analysis App** analyzes the sentiment of comments on a given YouTube video. It helps users understand whether viewers are reacting **positively, negatively, or neutrally** to a video. This can be useful for **content creators, marketers, and businesses** to gauge audience reactions and feedback effectively.

### 🚀 **Use Cases**

- **Content Creators**: Understand how viewers feel about their videos.
- **Businesses**: Analyze customer feedback on promotional videos.
- **Researchers**: Study audience engagement trends.
- **Viewers**: Check sentiment before watching a video.

## 🔄 **Process Flow**

1. **User Inputs**: A **YouTube video URL** and the **number of comments** to analyze.
2. **Extract Video ID**: The app extracts the video ID from the provided URL.
3. **Fetch Comments**: Retrieves comments using the **YouTube Data API**.
4. **Preprocessing**: Cleans and processes the extracted comments.
5. **Sentiment Analysis**: Uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** to classify each comment as **Positive, Negative, or Neutral**.
6. **Data Visualization**:
   - **Bar Chart**: Compares positive and negative sentiments.
   - **Pie Chart**: Shows the distribution of all sentiments.
7. **Results Display**: Total analyzed comments and sentiment distribution.

## 🧠 **Model Used: VADER (Sentiment Analysis)**

**VADER (Valence Aware Dictionary and sEntiment Reasoner)** is a **lexicon-based** sentiment analysis model designed specifically for text from **social media, reviews, and comments**.

### 🔍 **Why VADER?**

- **Pre-trained**: No additional training required.
- **Handles Emojis, Slang, and Capitalization**: Works well with **social media language**.
- **Highly Accurate for Short Text**: Optimized for comment-based data.

### 📊 **VADER Sentiment Scores**

VADER calculates sentiment scores based on predefined word sentiments and assigns:

- **Positive (compound score ≥ 0.05)** ✅
- **Negative (compound score ≤ -0.05)** ❌
- **Neutral (otherwise)** ⚪

## 🛠 **Tech Stack & Libraries**

### 🎯 **Frontend (UI)**

- **Streamlit** - Interactive UI for input and visualization.

### ⚙ **Backend (Processing & API Calls)**

- **Python** - Core programming language.
- **Google API Client** - Fetches YouTube comments.
- **NLTK** - Natural Language Toolkit for sentiment analysis.
- **Matplotlib** - Data visualization.
- **dotenv** - Manages environment variables securely.
- **pandas** - Handles data processing.

## 🏗 **Installation & Setup**

### 🔹 **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/youtube-sentiment-analysis.git
cd youtube-sentiment-analysis
```

### 🔹 **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### 🔹 **3. Set Up API Key Securely**

Create a `.env` file and add your **YouTube API Key**:

```bash
YOUTUBE_API_KEY=your_api_key_here
```

### 🔹 **4. Run the Streamlit App**

```bash
streamlit run app.py
```

## 🎨 **Features**

✅ Extracts & cleans comments from **any YouTube video**

✅ **Real-time Sentiment Analysis** using **VADER**

✅ **Bar Chart** (Positive vs. Negative Sentiments)

✅ **Pie Chart** (Overall Sentiment Distribution)

✅ **User-friendly UI** powered by **Streamlit**

✅ **Secure API Handling** using environment variables
