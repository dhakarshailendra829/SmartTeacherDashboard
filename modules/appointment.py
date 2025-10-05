import streamlit as st
import pandas as pd
import os

APPOINTMENTS_FILE = "data/appointments.csv"

# Ensure appointments file exists with correct headers
def ensure_appointments_file():
    headers = ["Student_Name", "Student_ID", "Teacher_ID", "Teacher_Name", "Slot", "Date"]
    if not os.path.exists(APPOINTMENTS_FILE) or os.stat(APPOINTMENTS_FILE).st_size == 0:
        with open(APPOINTMENTS_FILE, "w") as f:
            f.write(",".join(headers) + "\n")


def show_calendar(teacher_row):
    """
    Returns list of clickable slots for a teacher.
    """
    free_start = teacher_row['Free_Start']
    free_end = teacher_row['Free_End']
    days = teacher_row['Available_Days'].split(",")
    slots = [f"{day} {free_start}-{free_end}" for day in days]
    return slots


def book_appointment(student_name, student_id, teacher_row, slot):
    """
    Appends a new appointment entry into the CSV file.
    Automatically writes headers if file is empty.
    """
    ensure_appointments_file() 

    data = {
        "Student_Name": student_name,
        "Student_ID": student_id,
        "Teacher_ID": teacher_row['Teacher_ID'],
        "Teacher_Name": teacher_row['Teacher_Name'],
        "Slot": slot,
        "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    df = pd.DataFrame([data])

    # Append to CSV
    df.to_csv(APPOINTMENTS_FILE, mode='a', index=False, header=False)

    st.success(f"Appointment booked for {teacher_row['Teacher_Name']} at {slot}")
    st.balloons()


def get_appointments_by_student(student_id):
    """
    Returns all appointments for a specific student ID.
    If the file is empty, returns an empty DataFrame safely.
    """
    ensure_appointments_file()
    try:
        df = pd.read_csv(APPOINTMENTS_FILE)
        if "Student_ID" not in df.columns:
            return pd.DataFrame()
        return df[df['Student_ID'].astype(str) == str(student_id)]
    except pd.errors.EmptyDataError:
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading appointments file: {e}")
        return pd.DataFrame()
