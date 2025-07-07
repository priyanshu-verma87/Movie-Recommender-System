## Movie Recommender System with Content-Based Filtering

A content-based movie recommendation system using Natural Language Processing (NLP) and cosine similarity to suggest similar movies based on plot, genre, cast, and crew features.

## Project Overview

- **Recommendation Accuracy**: Suggests highly relevant movies based on content similarity
- **Dataset Size**: 4,806 movies with rich metadata
- **Features Used**: Plot overview, genres, keywords, top 3 cast members, director

## Live Demo

Try the live deployed app here:
Movie Recommender System on Streamlit Cloud
[https://movie-recommender-system-priyanshuverma87.streamlit.app/]

## Demo

![Movie Recommender App](movie-recommender-demo.png)


## Complete Pipeline Flow
                              ┌─────────────────┐
                              │   TMDB Dataset  │
                              │  movies.csv +   │
                              │  credits.csv    │
                              └────────┬────────┘
                                       │
                                       ▼
                              ┌─────────────────┐     
                              │  Data Merging   │     
                              │  4809 Records   │     
                              │  23 Features    │     
                              └────────┬────────┘     
                                       │
                                       ▼
                              ┌────────────────────────────┐
                              │   Feature Selection        │
                              │   • movie_id, title        │
                              │   • overview, genres       │
                              │   • keywords, cast, crew   │
                              └──────────────┬─────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Data Cleaning            │
                              │  • Remove 3 null overviews  │
                              │  • Final: 4806 movies       │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Feature Extraction       │
                              │  • Parse JSON strings       │
                              │  • Top 3 actors only        │
                              │  • Director from crew       │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Feature Engineering      │
                              │  • Combine into 'tags'      │
                              │  • Remove spaces            │
                              │  • Lowercase conversion     │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Text Processing          │
                              │  • Porter Stemmer           │
                              │  • Root word reduction      │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Vectorization            │
                              │  ┌─────────────────────┐    │
                              │  │ CountVectorizer     │    │
                              │  │ • 5000 features     │    │
                              │  │ • Remove stopwords  │    │
                              │  │ • Matrix: 4806×5000 │    │
                              │  └─────────────────────┘    │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Similarity Matrix        │
                              │  • Cosine Similarity        │
                              │  • Matrix: 4806×4806        │
                              │  • Pre-computed & saved     │
                              └──────────────┬──────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────┐
                              │    Web Deployment           │
                              │  ┌───────────────────────┐  │
                              │  │ • Streamlit UI        │  │
                              │  │ • TMDb API posters    │  │
                              │  │ • Real-time recs      │  │
                              │  └───────────────────────┘  │
                              └─────────────────────────────┘
## Detailed Process Flow

### 1. **Data Collection**
- Two CSV files from The Movie Database (TMDB) 5000 dataset
- **movies.csv**: Contains movie metadata (genres, keywords, overview, etc.)
- **credits.csv**: Contains cast and crew information
- Combined dataset: 4,809 movies with complete information

### 2. **Data Preprocessing**
- **Feature Selection**: Selected 7 relevant columns from 23 available
- **Data Cleaning**: Removed 3 movies with missing overviews
- **JSON Parsing**: Extracted names from JSON-formatted strings using `ast.literal_eval()`

### 3. **Feature Engineering**
- **Cast Limitation**: Only top 3 actors (main characters)
- **Crew Selection**: Only director (most influential)
- **Text Normalization**:
  - Removed spaces ("Science Fiction" → "ScienceFiction")
  - Converted to lowercase
  - Combined all features into single 'tags' column

### 4. **Text Processing**
- **Stemming**: Applied Porter Stemmer to reduce words to root form
  - "loved", "loving", "loves" → "love"
  - Improves matching between similar concepts
- **Purpose**: Reduces vocabulary size and improves similarity matching

### 5. **Vectorization**
- **Method**: Count Vectorizer (Bag of Words)
- **Configuration**:
  - Max features: 5,000 most frequent words
  - Removed English stop words
  - Created sparse matrix representation
- **Output**: 4,806 × 5,000 feature matrix

### 6. **Similarity Computation**
- **Algorithm**: Cosine Similarity
- **Why Cosine**:
  - Scale-invariant (movie length doesn't affect similarity)
  - Measures angle between vectors
  - Range: 0 (different) to 1 (identical)
- **Output**: 4,806 × 4,806 similarity matrix

### 7. **Deployment Architecture**
- **Frontend**: Streamlit web application
- **Storage**:
  - Small files (movies.pkl): GitHub
  - Large files (similarity.pkl): Google Drive with auto-download
- **External API**: TMDb for real-time poster fetching

## Results & Performance

- **Recommendation Quality**: Successfully identifies similar movies (e.g., Batman series)
- **Processing Speed**: Instant recommendations due to pre-computation
- **User Experience**: Clean interface with visual movie posters
- **Scalability**: Can handle thousands of movies efficiently

