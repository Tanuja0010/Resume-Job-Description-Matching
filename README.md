# Resume–Job Description Matching 
This project matches resumes with job descriptions using Natural Language Processing (NLP). It extracts key skills and experiences from resumes and job postings to calculate similarity and relevance.

## Features

- Extracts resume and JD content
- Cleans and processes text using NLTK
- Uses techniques like TF-IDF, cosine similarity
- Outputs matching score and highlights top keywords
- Web scraping from Glassdoor
- Visualizations using PCA/MDS

## Project Structure

- `getjd.py`: Scrapes job descriptions using Selenium
- `step2_getresume.py`: Processes resumes
- `step3_model_buidling.py`: Calculates similarity between resumes and JDs
- `Doc_Similarity.py`: Core similarity logic
- `data.csv`: Extracted job data
- `Summary.csv`: Resulting scores and outputs
- `matrix.json`, `url.json`: Input URLs and distance matrix

##  Tech Stack

- Python
- NLTK
- Scikit-learn
- Selenium
- BeautifulSoup
- Matplotlib (for visualizations)

##  How to Run

1. Install dependencies:
   
   pip install -r requirements.txt
