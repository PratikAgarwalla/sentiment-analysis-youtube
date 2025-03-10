import streamlit as st
import pandas as pd
import re
import os
from googleapiclient.discovery import build
from nltk.sentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import nltk
import matplotlib.pyplot as plt
import googleapiclient.errors
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

# Load environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Download VADER lexicon only once
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

# Initialize Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

# Function to extract video ID from URL
def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

# Function to clean comments
def clean_comment(comment):
    return re.sub(r"\s+", " ", comment).strip()

# Function to fetch comments from YouTube
def get_youtube_comments(video_id, max_results=100):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        comments = []
        next_page_token = None

        while True:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(max_results, 100),
                textFormat="plainText",
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                raw_comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                cleaned_comment = clean_comment(raw_comment)

                # Detect language and keep only English comments
                try:
                    if detect(cleaned_comment) == "en":
                        comments.append(cleaned_comment)
                except:
                    pass  # Ignore detection errors

            next_page_token = response.get("nextPageToken")

            if not next_page_token or len(comments) >= max_results:
                break

        if not comments:
            raise ValueError("No English comments found for this video.")

        return comments[:max_results]  # Return only requested count

    except googleapiclient.errors.HttpError as e:
        st.error(f"API Error: {e}")
        return []
    except Exception as e:
        st.error(f"Error fetching comments: {str(e)}")
        return []

# Function to analyze sentiment
def get_sentiment(comment):
    sentiment_score = sia.polarity_scores(comment)
    return sentiment_score["compound"], sentiment_score

# Streamlit UI
st.set_page_config(page_title="YouTube Comment Sentiment Analysis", page_icon="📊")
st.title("📊 YouTube Comment Sentiment Analysis 🎥")

# Input Fields
video_url = st.text_input("🔗 Enter YouTube Video URL:", value="https://www.youtube.com/watch?v=AKJfakEsgy0")
max_comments = st.number_input("📊 Max Comments to Analyze:", min_value=10, max_value=100000, step=10, value=100)

if st.button("Analyze Sentiments"):
    try:
        video_id = extract_video_id(video_url)

        if not video_id:
            st.error("⚠️ Invalid YouTube URL. Please enter a valid video link.")
        else:
            st.success(f"✅ Extracted Video ID: {video_id}")

            # Fetch and analyze comments
            comments = get_youtube_comments(video_id, max_comments)

            if not comments:
                st.error("⚠️ No English comments found. Try another video.")
            else:
                df = pd.DataFrame(comments, columns=["Comment"])
                df["Sentiment Score"], df["Sentiment Breakdown"] = zip(*df["Comment"].apply(get_sentiment))

                # Determine sentiment categories
                df["Sentiment"] = df["Sentiment Score"].apply(
                    lambda score: "Positive" if score >= 0.05 else "Negative" if score <= -0.05 else "Neutral"
                )

                # Count Sentiments
                sentiment_counts = df["Sentiment"].value_counts()

                # Display results
                st.write(f"📝 **Total Comments Analyzed:** {len(df)}")
                st.write(sentiment_counts)

                # Bar Chart (Positive vs Negative)
                st.subheader("📊 Sentiment Distribution (Bar Chart)")
                fig, ax = plt.subplots()
                sentiment_counts[["Positive", "Negative"]].plot(kind="bar", color=["green", "red"], ax=ax)
                plt.xticks(rotation=0)
                st.pyplot(fig)

                # Pie Chart (All Sentiments)
                st.subheader("🥧 Sentiment Distribution (Pie Chart)")

                # Define custom colors for each sentiment
                colors = {
                    "Positive": "green",
                    "Negative": "red",
                    "Neutral": "gray"
                }

                # Create the Pie Chart
                fig, ax = plt.subplots()
                sentiment_counts.plot(
                    kind="pie",
                    autopct="%1.1f%%", 
                    colors=[colors[sent] for sent in sentiment_counts.index], 
                    ax=ax,
                    startangle=140
                )

                ax.set_ylabel("")  
                ax.set_title("Sentiment Distribution") 

                st.pyplot(fig)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
