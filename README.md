# ai-data-analyst-assistant
# AI-Powered Data Analyst Assistant

An interactive AI-powered data analysis application built with Python, Pandas, Gemini API, and Streamlit. Users can upload a CSV dataset, explore key business metrics and visualizations, and ask questions about their data using natural language.

## Features

- Upload and analyze CSV datasets
- Automatic dataset summary and data quality checks
- Key metrics including sales, profit, averages, and record counts
- Product and regional performance analysis
- Monthly sales and profit trends
- Interactive charts and visualizations
- Natural-language questions about the dataset
- Pandas-based calculations for common analytical questions
- Gemini API for more complex business questions
- Streaming AI responses for faster results

## Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Google Gemini API**
- **Matplotlib / Streamlit charts**

## How It Works

1. Upload a CSV dataset through the Streamlit interface.
2. Pandas loads and analyzes the dataset.
3. The application calculates key metrics and business summaries.
4. Users can explore products, regions, and trends through the dashboard.
5. Users can ask questions using natural language.
6. Common numerical questions are answered directly using Pandas.
7. More complex analytical questions are sent to Gemini for natural-language insights.

## Example Questions

You can ask questions such as:

- What is the total sales?
- Which product generated the most profit?
- Which region has the highest sales?
- What is the overall profit margin?
- Which product has the highest profit margin?
- Which product should management focus on based on sales and profit?
- What trends do you see in the dataset?

## Project Structure

```text
ai-data-analyst-assistant/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── data/
    └── sales_data.csv
