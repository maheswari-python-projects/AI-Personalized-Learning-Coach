# AI Personalized Learning Coach

## Project Overview
AI Personalized Learning Coach is an AI-powered web application designed to help students improve their learning experience through personalized study plans, quizzes, and progress tracking.

## Technologies Used
- Python
- Streamlit
- Google Gemini AI
- SQLite Database

## Features
1. Student Registration and Login
2. AI-Based Personalized Study Plan Generation
3. AI-Based Quiz Generation
4. Multiple Choice Questions (MCQs)
5. Automatic Score and Percentage Calculation
6. Student Progress History
7. Database Storage

## Project Structure
- `app.py` – Main Streamlit application
- `ai_service.py` – Gemini AI integration
- `learning_plan.py` – Study plan generation
- `quiz_manager.py` – Quiz generation
- `auth.py` – Student authentication
- `database.py` – Database operations
- `requirements.txt` – Required Python packages
- `.env.example` – Environment variable example

## Installation and Setup

1. Clone the repository:

   `git clone https://github.com/maheswari-python-projects/AI-Personalized-Learning-Coach.git`

2. Open the project folder.

3. Create a virtual environment:

   `python -m venv venv`

4. Activate it:

   `venv\Scripts\activate`

5. Install dependencies:

   `pip install -r requirements.txt`

6. Create a `.env` file and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

7. Run the application:

   `python -m streamlit run app.py`

## Future Enhancements
- More subjects and quiz categories
- Advanced student performance analytics
- Personalized learning recommendations

## Author
Maheswari

## Project Type
AI and Python Internship Project