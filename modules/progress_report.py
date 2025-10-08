import streamlit as st
import pandas as pd
import os
import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from modules.pdf_generator import generate_pdf_report

DATA_DIR = "data"

def safe_load_csv(fname, parse_dates=None):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        return None
    return pd.read_csv(path, parse_dates=parse_dates)

def progress_report_tab():
    st.title("Student Progress Report")

    st.markdown("Enter your **Name** and **Student ID** to view your progress.")
    name = st.text_input("Student Name")
    student_id = st.text_input("Student ID")

    if not (name and student_id):
        st.info("Please enter your name and student ID.")
        return

    quiz_df = safe_load_csv("quiz_results.csv", parse_dates=["DateTime"])
    thoughts_df = safe_load_csv("student_thoughts.csv", parse_dates=["Date"])

    if quiz_df is None:
        st.error("Missing file: data/quiz_results.csv — please add it.")
        return

    qf = pd.DataFrame()
    if quiz_df is not None:
        qf = quiz_df[quiz_df['Student_ID'].astype(str) == student_id].copy()
        qf['DateTime'] = pd.to_datetime(qf['DateTime'], errors='coerce')
        qf = qf.sort_values('DateTime').reset_index(drop=True)

    tf = pd.DataFrame()
    if thoughts_df is not None:
        tf = thoughts_df[thoughts_df['Student_ID'].astype(str) == student_id].copy()
        tf['DateTime'] = pd.to_datetime(tf['Date'], errors='coerce')
        tf = tf.sort_values('DateTime').reset_index(drop=True)

    total_quizzes = len(qf)
    avg_score = round(qf['Score'].mean(), 2) if total_quizzes > 0 else 0
    total_thoughts = len(tf)

    st.markdown("### Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Quizzes Taken", total_quizzes)
    col2.metric("Average Score", f"{avg_score}")
    col3.metric("Thoughts Shared", total_thoughts)

    try:
        avg_by_student = quiz_df.groupby("Student_ID")['Score'].mean().reset_index()
        avg_by_student = avg_by_student.sort_values('Score', ascending=False).reset_index(drop=True)
        if student_id in avg_by_student['Student_ID'].astype(str).values:
            rank = int(avg_by_student[avg_by_student['Student_ID'].astype(str) == student_id].index[0]) + 1
            total_students = avg_by_student.shape[0]
            st.markdown(f"**🏆 Rank:** {rank} / {total_students}")
        else:
            st.markdown("**🏆 Rank:** Not ranked (no quizzes)")
    except Exception:
        st.markdown("**🏆 Rank:** Data not available")

    st.markdown("---")

    if total_quizzes > 0:
        st.markdown("### Quiz Performance Over Time")
        plt.figure(figsize=(8,5))
        plt.plot(qf['DateTime'], qf['Score'], marker='o', linestyle='-', color='green')
        plt.xlabel("Date")
        plt.ylabel("Score")
        plt.title("Quiz Scores Over Time")
        plt.xticks(rotation=20)
        plt.grid(True)
        st.pyplot(plt)
        buf_scores = io.BytesIO()
        plt.savefig(buf_scores, format="png", bbox_inches="tight")
        buf_scores.seek(0)
        plt.close()
    else:
        st.info("No quiz attempts yet — take some quizzes to see progress.")
        buf_scores = None

    st.markdown("### Correct vs Wrong (All Quizzes)")
    correct_total, wrong_total = 0, 0
    if total_quizzes > 0:
        if 'Total_Questions' in qf.columns:
            total_attempts = qf['Total_Questions'].astype(int).sum()
        else:
            total_attempts = total_quizzes * 10
        correct_total = int(qf['Score'].sum())
        wrong_total = int(total_attempts - correct_total)

        plt.figure(figsize=(6,6))
        plt.pie([correct_total, wrong_total],
                labels=['Correct', 'Wrong'],
                colors=['#4CAF50', '#FF5722'],
                autopct='%1.1f%%',
                startangle=90,
                explode=(0.05,0.05))
        plt.title("Correct vs Wrong Answers")
        st.pyplot(plt)
        buf_pie = io.BytesIO()
        plt.savefig(buf_pie, format="png", bbox_inches="tight")
        buf_pie.seek(0)
        plt.close()
    else:
        st.info("No quiz attempts to compute correct/wrong counts.")
        buf_pie = None

    st.markdown("---")

    st.markdown("### 🧾 Activity Timeline")
    timeline_rows = []

    for _, r in qf.iterrows():
        timeline_rows.append({
            "DateTime": r['DateTime'],
            "Type": "Quiz",
            "Detail": f"Score {r['Score']} / {r.get('Total_Questions', '')}"
        })
    for _, r in tf.iterrows():
        timeline_rows.append({
            "DateTime": r['DateTime'],
            "Type": "Thought",
            "Detail": r.get('Thought', '')
        })

    timeline_df = pd.DataFrame(timeline_rows)
    if not timeline_df.empty:
        timeline_df = timeline_df.sort_values("DateTime", ascending=False).reset_index(drop=True)
        st.dataframe(timeline_df, use_container_width=True)
    else:
        st.info("No timeline events yet.")

    st.markdown("---")

    st.markdown("### Export Report")
    if st.button("Generate & Download PDF Report"):
        summary = {
            "total_quizzes": total_quizzes,
            "avg_score": avg_score,
            "total_thoughts": total_thoughts,
            "correct_total": correct_total,
            "wrong_total": wrong_total
        }
        images = {}
        if buf_scores: images['scores_png'] = buf_scores
        if buf_pie: images['correct_wrong_png'] = buf_pie

        pdf_bytes = generate_pdf_report(name, student_id, summary, timeline_df, images)
        st.download_button("⬇Download PDF", data=pdf_bytes, file_name=f"{student_id}_progress_report.pdf", mime="application/pdf")
