import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from modules.ui_components import load_css, show_motivational_cards
from modules.appointment import show_calendar, book_appointment, get_appointments_by_student, ensure_appointments_file
from modules.admin_panel import admin_panel
import os
from modules.quiz import quiz_tab
from modules.progress_report import progress_report_tab


st.set_page_config(page_title="AI Teacher Assistant", page_icon="🎓", layout="wide")
load_css()
ensure_appointments_file()

try:
    model = joblib.load("models/teacher_intent_model.pkl")
except Exception as e:
    st.error(f"Error loading model: {e}")
    model = None

teacher_df = pd.read_csv("data/teacher_dataset_100.csv")
required_columns = [
    'Teacher_ID','Teacher_Name','Subject','Block','Room_Number',
    'Cabin_Number','Lecture_Start','Lecture_End','Free_Start',
    'Free_End','Available_Days'
]
if not all(col in teacher_df.columns for col in required_columns):
    st.error("Teacher CSV missing required columns!")
    st.stop()

THOUGHTS_FILE = "data/student_thoughts.csv"
if not os.path.exists(THOUGHTS_FILE) or os.stat(THOUGHTS_FILE).st_size == 0:
    with open(THOUGHTS_FILE, "w") as f:
        f.write("Student_Name,Student_ID,Teacher_Name,Thought,Date\n")

st.markdown("""
<style>
.navbar {
    display: flex;
    justify-content: space-around;
    background: linear-gradient(90deg, #001f3f, #0074D9);
    padding: 14px 0;
    font-size: 18px;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0px 2px 10px #00ffff44;
}
.navbar button {
    background: none;
    color: white;
    border: none;
    font-size: 16px;
    padding: 8px 20px;
    cursor: pointer;
    border-radius: 6px;
    transition: 0.3s;
}
.navbar button:hover {
    background-color: #00ffff;
    color: #000;
    transform: scale(1.05);
}
.active-nav {
    background-color: #00ffff;
    color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state['page'] = "Home"

pages = ["Home", "Book Appointment", "Student Thoughts", "Admin Panel", "About", "Quiz", "Progress Report"]
st.markdown('<div class="navbar">', unsafe_allow_html=True)
cols = st.columns(len(pages))
for idx, name in enumerate(pages):
    if cols[idx].button(name, key=f"nav_{name}"):
        st.session_state['page'] = name
st.markdown('</div>', unsafe_allow_html=True)

page = st.session_state['page']

def load_appointments():
    try:
        return pd.read_csv("data/appointments.csv")
    except:
        return pd.DataFrame(columns=['Student_Name','Student_ID','Teacher_ID','Teacher_Name','Slot','Date'])

def load_thoughts():
    try:
        return pd.read_csv(THOUGHTS_FILE)
    except:
        return pd.DataFrame(columns=['Student_Name','Student_ID','Teacher_Name','Thought','Date'])

appointments_df = load_appointments()
thoughts_df = load_thoughts()

if page == "Home":
    st.markdown("<h1 style='text-align:center; color:#00ffff;'>🎓 AI Teacher Assistant</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center; font-size:18px;'>Search teachers, view appointments, and get inspired by top tech innovators!</p>", unsafe_allow_html=True)

    st.markdown("### 📊 Quick Stats")
    total_teachers = len(teacher_df)
    total_appointments = len(appointments_df)
    most_booked_teacher = appointments_df['Teacher_Name'].value_counts().idxmax() if not appointments_df.empty else "N/A"

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Teachers", total_teachers)
    c2.metric("Total Appointments", total_appointments)
    c3.metric("Most Booked Teacher", most_booked_teacher)

    st.markdown("### 🌟 Top 3 Teachers")
    if not appointments_df.empty:
        top3 = appointments_df['Teacher_Name'].value_counts().head(3)
        for t in top3.index:
            st.success(f"⭐ {t} — {top3[t]} Appointments")
    else:
        st.info("No appointments booked yet.")

    st.markdown("### 📝 Recent Appointments")
    recent = appointments_df.tail(5)
    if not recent.empty:
        st.dataframe(recent, use_container_width=True)
    else:
        st.info("No recent appointments.")

    show_motivational_cards()

    st.markdown("### 🔎 Search Teacher")
    query = st.text_input("Search by Name or ID:")
    if query:
        if query.isnumeric():
            result = teacher_df[teacher_df['Teacher_ID'].astype(str).str.contains(query)]
        else:
            result = teacher_df[teacher_df['Teacher_Name'].str.contains(query, case=False)]

        if not result.empty:
            st.success(f"Found {len(result)} teacher(s)")
            for _, t in result.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="teacher-card">
                        <h3>{t['Teacher_Name']} ({t['Teacher_ID']})</h3>
                        <p><b>Subject:</b> {t['Subject']} | <b>Block:</b> {t['Block']} | <b>Room:</b> {t['Room_Number']}</p>
                        <p><b>Free Slots:</b> {t['Free_Start']} - {t['Free_End']} | <b>Days:</b> {t['Available_Days']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Teacher not found!")

elif page == "Book Appointment":
    st.title("📅 Book Appointment")
    student_name = st.text_input("👨‍🎓 Student Name")
    student_id = st.text_input("🆔 Student ID")
    teacher_query = st.text_input("🔍 Search Teacher by Name or ID")

    selected_teacher = None
    if teacher_query:
        if teacher_query.isnumeric():
            selected_teacher = teacher_df[teacher_df['Teacher_ID'].astype(str) == teacher_query]
        else:
            selected_teacher = teacher_df[teacher_df['Teacher_Name'].str.contains(teacher_query, case=False)]

    if selected_teacher is not None and not selected_teacher.empty:
        teacher_row = selected_teacher.iloc[0]
        st.markdown(f"""
        <div class="teacher-card">
            <h3>{teacher_row['Teacher_Name']} ({teacher_row['Teacher_ID']})</h3>
            <p><b>Subject:</b> {teacher_row['Subject']} | <b>Block:</b> {teacher_row['Block']} | <b>Room:</b> {teacher_row['Room_Number']}</p>
            <p><b>Free Slots:</b> {teacher_row['Free_Start']} - {teacher_row['Free_End']} | <b>Days:</b> {teacher_row['Available_Days']}</p>
        </div>
        """, unsafe_allow_html=True)

        appointments_file = "data/appointments.csv"
        if os.path.exists(appointments_file):
            appt_df = pd.read_csv(appointments_file)

            top_teachers = appt_df['Teacher_Name'].value_counts().head(3)
            st.info("💡 Popular Teachers based on past appointments:")
            for t, count in top_teachers.items():
                st.write(f"- {t} — {count} bookings")

            if student_id:
                student_history = appt_df[appt_df['Student_ID'] == student_id]
                if not student_history.empty:
                    last_teacher = student_history.iloc[-1]['Teacher_Name']
                    last_slot = student_history.iloc[-1]['Slot']
                    st.info(f"Recommended next slot: Try with {last_teacher} at {last_slot} again if available")
                else:
                    st.info("No past appointments, pick any free slot shown below.")
        else:
            st.info("No past appointment data yet. Suggestions will appear here once students book appointments.")

        available_slots = show_calendar(teacher_row)
        if available_slots:
            st.markdown("### 🕒 Select Slot")
            for slot in available_slots:
                if st.button(f"Book: {slot}"):
                    if not student_name or not student_id:
                        st.error("Please enter Student Name and ID")
                    else:
                        book_appointment(student_name, student_id, teacher_row, slot)
                        st.success(f"Appointment booked with {teacher_row['Teacher_Name']} at {slot}")

    if student_id:
        st.markdown("### 🎫 Your Appointments")
        df_student = get_appointments_by_student(student_id)
        if not df_student.empty:
            st.dataframe(df_student, use_container_width=True)
        else:
            st.info("No appointments found for this Student ID.")

elif page == "Student Thoughts":
    st.title("💬 Share Your Thoughts")
    student_name = st.text_input("👨‍🎓 Student Name")
    student_id = st.text_input("🆔 Student ID")
    teacher_name = st.text_input("👩‍🏫 Teacher Name")
    thought = st.text_area("✍️ Share your thoughts about the teacher")

    if st.button("Submit Thought"):
        if not student_name or not student_id or not teacher_name or not thought:
            st.error("Please fill all fields!")
        else:
            new_row = pd.DataFrame([{
                'Student_Name': student_name,
                'Student_ID': student_id,
                'Teacher_Name': teacher_name,
                'Thought': thought,
                'Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }])
            new_row.to_csv(THOUGHTS_FILE, mode='a', index=False, header=False)
            st.success("Thought shared successfully!")

    st.markdown("### 📝 Recent Thoughts")
    updated_thoughts = load_thoughts()
    if not updated_thoughts.empty:
        st.dataframe(updated_thoughts.tail(10), use_container_width=True)
    else:
        st.info("No thoughts shared yet.")

elif page == "Admin Panel":
    admin_panel()

elif page == "Quiz":
    quiz_tab()

elif page == "Progress Report":
    progress_report_tab()

elif page == "About":
    st.markdown("""
    <h2 style='color:#00ffff'>About this Project</h2>
    <p>Advanced <b>Teacher Assistant</b> with interactive booking, analytics, and AI-driven features.</p>
    <h3>👤 Project Maker</h3>
    <p><b>Shailendra Dhakad</b> – Artificial Intelligence/Machine Learning Student</p>

    <h3>🌟 Features</h3>
    <ul>
        <li>Teacher Search & Availability</li>
        <li>Interactive Appointment Booking</li>
        <li>Student Dashboard & History</li>
        <li>Admin Panel for Management</li>
        <li>Motivational & Inventor Cards</li>
        <li>Quick Stats & Top Teachers</li>
        <li>Dark Neon Theme</li>
        <li>Student Thoughts Sharing</li>
    </ul>

    <h3>🔮 Future Roadmap</h3>
    <ul>
        <li>AI-based Teacher & Slot Suggestions</li>
        <li>Email & PDF Notifications</li>
        <li>Dark/Light Mode Toggle</li>
        <li>Advanced Analytics & Graphs</li>
        <li>Gamified Badges for Students</li>
    </ul>
    """, unsafe_allow_html=True)

