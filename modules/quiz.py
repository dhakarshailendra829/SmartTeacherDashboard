import streamlit as st
import pandas as pd
import random
import datetime
import os  

def quiz_tab():
    st.markdown("## Student Quiz")
    st.write("Enter your details and take a 10-question quiz!")

    student_name = st.text_input(" Student Name")
    student_id = st.text_input(" Student ID")

    if student_name and student_id:
        if "quiz_started" not in st.session_state:
            st.session_state.quiz_started = False

        df = pd.read_csv("data/quiz_questions_dataset.csv")

        if not st.session_state.quiz_started:
            if st.button("Start Quiz"):
                st.session_state.questions = df.sample(n=10).reset_index(drop=True)
                st.session_state.answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_started = True

        if st.session_state.quiz_started and not st.session_state.quiz_submitted:
            questions = st.session_state.questions
            for i, row in questions.iterrows():
                st.markdown(f"**Q{i+1}: {row['Question']}**")
                options = [row['Option_A'], row['Option_B'], row['Option_C'], row['Option_D']]
                selected = st.radio(
                    f"Select your answer for Q{i+1}",
                    options,
                    key=f"q_{i}"
                )
                st.session_state.answers[i] = selected

            if st.button("Submit Quiz"):
                st.session_state.quiz_submitted = True

        if st.session_state.get("quiz_submitted", False):
            questions = st.session_state.questions
            correct_count = 0
            wrong_count = 0
            analysis_data = []

            for i, row in questions.iterrows():
                correct_option_letter = row['Correct_Option']
                correct_answer = row[f'Option_{correct_option_letter}']
                user_answer = st.session_state.answers.get(i, "")

                is_correct = (user_answer == correct_answer)
                if is_correct:
                    correct_count += 1
                else:
                    wrong_count += 1

                analysis_data.append({
                    "Q#": i+1,
                    "Question": row['Question'],
                    "Your Answer": user_answer,
                    "Correct Answer": correct_answer,
                    "Result": "Correct" if is_correct else "Wrong"
                })

            st.success(f" {student_name}, you got {correct_count} correct and {wrong_count} wrong out of 10.")

            st.markdown("### Detailed Analysis")
            analysis_df = pd.DataFrame(analysis_data)
            st.dataframe(analysis_df, use_container_width=True)

            save_result(student_name, student_id, correct_count, len(questions))

            if st.button("Restart Quiz"):
                st.session_state.quiz_started = False
                st.session_state.quiz_submitted = False
                st.session_state.answers = {}
    else:
        st.info("Please enter your name and ID to start the quiz.")

def save_result(name, student_id, score, total_questions):
    """Append quiz result to CSV with date & time."""
    result_file = "data/quiz_results.csv"

    if not os.path.exists(result_file):
        with open(result_file, "w") as f:
            f.write("Name,Student_ID,DateTime,Score,Total_Questions\n")

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_entry = f"{name},{student_id},{current_time},{score},{total_questions}\n"

    with open(result_file, "a") as f:
        f.write(new_entry)
