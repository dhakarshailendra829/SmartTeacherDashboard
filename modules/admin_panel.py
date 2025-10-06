import streamlit as st
import pandas as pd
import os
import plotly.express as px
from datetime import datetime

def admin_panel(data_path="data/teacher_dataset_100.csv"):
    st.title("🧰 Admin Panel - Analytics & Management")
    st.markdown("Manage teacher datasets, view appointments, student feedback, and analyze trends!")

    # Section 1: Upload Teacher Dataset
    st.subheader("📤 Upload New Teacher Dataset")
    uploaded_file = st.file_uploader("Upload (.csv)", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if not df.empty:
            df.to_csv(data_path, index=False)
            st.success("Teacher dataset updated successfully!")
        else:
            st.error("Uploaded file is empty!")

    # Section 2: Download Teacher Dataset
    st.subheader("📥 Download Current Dataset")
    if os.path.exists(data_path):
        st.download_button(
            "⬇️ Download Teacher Dataset",
            data=open(data_path, "rb"),
            file_name="teacher_dataset_backup.csv",
            mime="text/csv"
        )

    # Section 3: Dataset Stats & Preview
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        st.markdown("### 📊 Teacher Dataset Stats")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Teachers", len(df))
        col2.metric("Unique Subjects", df['Subject'].nunique())
        col3.metric("Total Free Slots", df['Free_Start'].count())

        with st.expander("📋 Preview Teacher Dataset"):
            st.dataframe(df)

    # =========================
    # Section 4: Appointment Analytics
    # =========================
    st.subheader("📅 Appointment Data & Analytics")
    appointment_file = "data/appointments.csv"
    if os.path.exists(appointment_file):
        appt_df = pd.read_csv(appointment_file)

        if appt_df.empty:
            st.info("No appointments have been booked yet.")
        else:
            # Convert Date to datetime safely
            if 'Date' in appt_df.columns:
                appt_df['Date'] = pd.to_datetime(appt_df['Date'], errors='coerce')

            st.write(f"Total Appointments: {len(appt_df)}")
            st.dataframe(appt_df.tail(10))

            # --- Appointments Over Time ---
            if appt_df['Date'].notna().any():
                st.markdown("#### 📈 Appointments Over Time")
                appt_over_time = appt_df.groupby(appt_df['Date'].dt.date).size().reset_index(name='Count')
                fig1 = px.line(appt_over_time, x='Date', y='Count', markers=True,
                               title="Appointments Trend Over Time", labels={'Count': 'Number of Appointments'})
                st.plotly_chart(fig1, use_container_width=True)

            # --- Most Booked Teachers ---
            if 'Teacher_Name' in appt_df.columns and not appt_df['Teacher_Name'].isna().all():
                st.markdown("#### 🏆 Most Booked Teachers")
                teacher_counts = appt_df['Teacher_Name'].value_counts().reset_index()
                teacher_counts.columns = ['Teacher_Name', 'Bookings']
                fig2 = px.bar(teacher_counts, x='Teacher_Name', y='Bookings', color='Bookings',
                              title="Top Teachers by Appointments", text='Bookings')
                st.plotly_chart(fig2, use_container_width=True)

            # --- Subject Popularity ---
            if 'Teacher_ID' in appt_df.columns and not df.empty:
                st.markdown("#### 📚 Subject Popularity")
                subject_counts = appt_df.merge(df[['Teacher_ID', 'Subject']], on='Teacher_ID', how='left')
                subj_chart = subject_counts['Subject'].value_counts().reset_index()
                subj_chart.columns = ['Subject', 'Count']
                fig3 = px.pie(subj_chart, names='Subject', values='Count', title="Appointments per Subject")
                st.plotly_chart(fig3, use_container_width=True)

            # --- Clear Appointments ---
            if st.button("🗑 Clear All Appointments"):
                os.remove(appointment_file)
                st.warning("⚠ All appointment records deleted!")
    else:
        st.info("No appointments file found yet.")

    # Section 5: Student Thoughts
    st.subheader("💬 Student Thoughts & Feedback")
    thoughts_file = "data/student_thoughts.csv"
    if os.path.exists(thoughts_file):
        t_df = pd.read_csv(thoughts_file, parse_dates=['Date'])
        if t_df.empty:
            st.info("No thoughts submitted yet.")
        else:
            st.write(f"Total Thoughts: {len(t_df)}")
            st.dataframe(t_df.tail(10))

            if st.button("🗑 Clear All Thoughts"):
                os.remove(thoughts_file)
                st.warning("⚠ All student thoughts cleared!")
    else:
        st.info("No thoughts submitted yet.")


