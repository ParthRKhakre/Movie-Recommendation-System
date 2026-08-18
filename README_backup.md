# 🎬 Movie Recommendation System

A **content-based movie recommendation system** that recommends similar movies using **Natural Language Processing (NLP)** and movie metadata.

## 🚀 Overview

This project builds a recommendation engine from scratch by analyzing movie information such as titles, genres, keywords, cast, crew, and descriptions. It uses text processing and similarity techniques to find movies with similar content.

The recommendation engine is exposed through a **FastAPI backend**, making it suitable for real-time applications.

## ✨ Features

* 🎯 Content-based movie recommendations
* 🧠 NLP-based text preprocessing and feature extraction
* 🔍 Similarity-based movie matching
* ⚡ FastAPI REST API
* 📡 Real-time recommendations
* 🛠️ Modular and production-ready architecture

## 🧠 How It Works

```text
Movie Metadata
      ↓
Text Preprocessing
      ↓
Feature Extraction
      ↓
Movie Feature Vectors
      ↓
Similarity Calculation
      ↓
Top-N Recommendations
```

The system creates a combined representation of each movie and calculates similarity between movies to recommend the most relevant titles.

## 🛠️ Tech Stack

* **Python**
* **Pandas & NumPy**
* **Scikit-learn**
* **NLP**
* **FastAPI**
* **Uvicorn**

## 📁 Project Structure

```text
movie-recommendation-system/
│
├── data/
│   └── movies.csv
│
├── model/
│   └── recommendation_model.pkl
│
├── app/
│   ├── main.py
│   └── recommender.py
│
├── notebooks/
│   └── recommendation_system.ipynb
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd movie-recommendation-system
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Run the API

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API Usage

Example request:

```text
GET /recommend/{movie_name}
```

Example:

```text
GET /recommend/Inception
```

The API returns a list of movies with similar content.

## 📌 Future Improvements

* Add collaborative filtering
* Build a hybrid recommendation system
* Add user personalization
* Deploy using Docker and cloud infrastructure
* Add a web-based frontend

## 👨‍💻 Author

**Parth Khakre**

* [LinkedIn](https://www.linkedin.com/in/parth-khakre/)
* [GitHub](https://github.com/ParthRKhakre)
