
import streamlit as st

from auth import create_users_table, register_user, login_user
from learning_plan import generate_study_plan
from quiz_manager import generate_quiz
from database import (
    create_database,
    save_quiz_result,
    get_quiz_results
)

# Page settings
st.set_page_config(
    page_title="AI Personalized Learning Coach",
    page_icon="🎓",
    layout="wide"
)

# Create database
create_database()
create_users_table()

# Login session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# LOGIN AND REGISTER
if not st.session_state["logged_in"]:

    st.title("🎓 Student Login")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with register_tab:
        st.subheader("Create New Account")

        new_username = st.text_input("Create Username")
        new_password = st.text_input(
            "Create Password",
            type="password"
        )

        if st.button("Register"):
            if new_username.strip() and new_password:
                if register_user(new_username.strip(), new_password):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists.")
            else:
                st.warning("Enter username and password.")

    with login_tab:
        st.subheader("Student Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username.strip(), password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username.strip()
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.stop()

# SIDEBAR
st.sidebar.success(
    f"Welcome, {st.session_state['username']}!"
)

if st.sidebar.button("Logout"):
    st.session_state["logged_in"] = False
    st.rerun()

# MAIN PAGE
st.title("🎓 AI Personalized Learning Coach")
st.write("Your personal AI study planner and quiz assistant")

st.divider()

# STUDY PLAN GENERATOR
st.header("📚 AI Study Plan Generator")

subject = st.text_input("Enter your subject", value="Python")

goal = st.text_input(
    "What is your learning goal?",
    value="Learn Python programming"
)

level = st.selectbox(
    "Select your current level",
    ["Beginner", "Intermediate", "Advanced"]
)

duration = st.selectbox(
    "Select study duration",
    ["7 days", "15 days", "30 days"]
)

daily_minutes = st.number_input(
    "Daily study time (minutes)",
    min_value=15,
    max_value=600,
    value=60
)

if st.button("Generate Study Plan"):
    try:
        with st.spinner("Creating your study plan..."):
            plan = generate_study_plan(
                subject,
                goal,
                level,
                duration,
                daily_minutes
            )

        st.subheader("Your Personalized Study Plan")
        st.markdown(plan)

    except Exception as e:
        st.error("Study plan generation failed.")
        st.exception(e)

st.divider()

# QUIZ GENERATOR
st.header("📝 AI Quiz Generator")

quiz_subject = st.text_input(
    "Enter subject for quiz",
    value="Python"
)

quiz_level = st.selectbox(
    "Select quiz difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

num_questions = st.selectbox(
    "Number of questions",
    [5, 10]
)

if st.button("Generate Quiz"):
    try:
        with st.spinner("Generating your quiz..."):
            questions = generate_quiz(
                quiz_subject,
                quiz_level,
                num_questions
            )

        st.session_state["quiz_questions"] = questions
        st.session_state["quiz_subject"] = quiz_subject
        st.session_state["quiz_submitted"] = False

    except Exception as e:
        st.error("Quiz generation failed.")
        st.exception(e)

# DISPLAY QUIZ
if "quiz_questions" in st.session_state:

    st.subheader("Your Quiz")

    if not st.session_state.get("quiz_submitted", False):

        with st.form("quiz_form"):

            for i, question in enumerate(
                st.session_state["quiz_questions"]
            ):
                st.write(
                    f"**Q{i + 1}. {question['question']}**"
                )

                st.radio(
                    "Choose your answer",
                    question["options"],
                    key=f"quiz_q_{i}"
                )

            submitted = st.form_submit_button("Submit Quiz")

        if submitted:
            score = 0
            questions = st.session_state["quiz_questions"]

            for i, question in enumerate(questions):
                selected = st.session_state.get(f"quiz_q_{i}")

                if selected == question["answer"]:
                    score += 1

            total_questions = len(questions)

            st.session_state["quiz_score"] = score
            st.session_state["quiz_submitted"] = True

            save_quiz_result(
                st.session_state["username"],
                st.session_state["quiz_subject"],
                score,
                total_questions
            )

            st.rerun()

    # QUIZ RESULT
    if st.session_state.get("quiz_submitted", False):

        score = st.session_state["quiz_score"]
        total_questions = len(st.session_state["quiz_questions"])

        percentage = (score / total_questions) * 100

        st.success("Quiz submitted successfully!")

        st.metric("Your Score", f"{score} / {total_questions}")
        st.metric("Your Percentage", f"{percentage:.0f}%")

        if percentage >= 80:
            st.success("Excellent! You have a very good understanding.")
        elif percentage >= 50:
            st.info("Good effort! Revise the topics and practice more.")
        else:
            st.warning("Keep practicing. Review the basics and try again.")

        if st.button("Try Another Quiz"):
            for key in [
                "quiz_questions",
                "quiz_submitted",
                "quiz_score",
                "quiz_subject"
            ]:
                st.session_state.pop(key, None)

            st.rerun()

st.divider()

# STUDENT PROGRESS HISTORY
st.header("📈 Student Progress History")

if st.button("View Progress History"):

    results = get_quiz_results(
        st.session_state["username"]
    )

    if results:
        for i, row in enumerate(results):
            st.write(f"Quiz {i + 1}")
            st.write(f"Subject: {row['subject']}")
            st.write(
                f"Score: {row['score']} / {row['total_questions']}"
            )
            st.write(
                f"Percentage: {row['percentage']:.1f}%"
            )
            st.write(f"Date: {row['date']}")
            st.divider()

        average_score = sum(
            row["percentage"] for row in results
        ) / len(results)

        st.metric("Average Quiz Score", f"{average_score:.1f}%")

    else:
        st.info("No quiz results saved yet.")

st.caption("AI Personalized Learning Coach")

