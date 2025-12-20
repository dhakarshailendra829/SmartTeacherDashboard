<h1 align="center">Smart Teacher Dashboard</h1>
<p align="center">
  <b>AI-Powered Teacher Assistant & Appointment Management System</b><br/>
  <i>
    Artificial Intelligence • Machine Learning • Streamlit •
    Real-Time Dashboards • Academic Workflow Automation
  </i>
</p>
<p align="center">
  <img src="https://img.shields.io/badge/AI-Teacher%20Assistant-blueviolet" />
  <img src="https://img.shields.io/badge/Machine%20Learning-Intent%20Model-brightgreen" />
  <img src="https://img.shields.io/badge/Streamlit-Interactive%20UI-orange" />
  <img src="https://img.shields.io/badge/Real--Time-Analytics-blue" />
  <img src="https://img.shields.io/badge/Education-Smart%20Campus-success" />
</p>

---
## Project Overview
**Smart Teacher Dashboard** is an **AI-driven academic assistant platform** designed to streamline **teacher discovery, appointment scheduling, student interaction, and academic progress tracking** through a single unified dashboard.
The system combines:
- **Interactive Streamlit UI**
- **Machine Learning intent model**
- **Real-time analytics**
- **Role-based access (Student / Admin)**
It simulates a **smart college/school digital assistant** that improves communication efficiency between students and faculty.
---

## Purpose & Motivation
Traditional academic systems suffer from:
- Manual appointment handling
- Poor visibility of teacher availability
- No centralized student-teacher interaction history
- Limited data-driven insights

This project solves those problems by providing:
- Automated appointment booking
- AI-assisted teacher interaction
- Real-time dashboards & insights
- Scalable foundation for future AI features
---

## Key Features

### Authentication System
- User registration & login
- Session-based authentication
- Secure CSV-based user storage

### Teacher Search & Discovery
- Search by **Teacher Name or ID**
- View subject, block, room, and availability
- Real-time filtering

### Appointment Booking System
- View free slots dynamically
- Book appointments with one click
- Student-wise appointment history
- Popular teacher recommendations
- Past-booking-based suggestions

### AI & Smart Logic
- Pre-trained **teacher intent ML model**
- Intelligent slot & teacher suggestions
- Future-ready AI architecture

### Student Thoughts Module
- Students can share feedback/thoughts
- Stored with timestamp
- View recent submissions in real time

### Dashboard Analytics
- Total teachers count
- Total appointments
- Most booked teacher
- Top 3 teachers
- Recent appointment tracking

### Quiz Module
- Interactive quiz tab for students
- Supports academic engagement

### Progress Report
- Student-wise progress visualization
- Extendable for academic analytics

### Admin Panel
- Centralized system management
- Monitoring appointments & activities
- Designed for scalability

### UI & UX
- Custom CSS styling
- Neon dark theme
- Sticky navigation bar
- Responsive layout
---

## Project Structure
SmartTeacherDashboard/
│
├── app.py # Main Streamlit frontend
├── models/
│ └── teacher_intent_model.pkl
│
├── modules/
│ ├── ui_components.py # CSS & UI helpers
│ ├── appointment.py # Booking logic
│ ├── admin_panel.py # Admin controls
│ ├── quiz.py # Quiz module
│ └── progress_report.py # Progress analytics
│
├── data/
│ ├── users.csv
│ ├── teacher_dataset_100.csv
│ ├── appointments.csv
│ └── student_thoughts.csv
│
├── images/
│ └── (UI assets if any)
│
└── README.md
---

## Tech Stack
- **Frontend:** Streamlit
- **Backend Logic:** Python
- **Machine Learning:** Scikit-learn, Joblib
- **Data Handling:** Pandas
- **Storage:** CSV-based persistence
- **UI Styling:** Custom CSS + HTML
- **Deployment Ready:** Streamlit Cloud / Local
---

## How to Run the Project
### Clone Repository
    git clone https://github.com/dhakarshailendra829/SmartTeacherDashboard.git
    cd SmartTeacherDashboard
    
### Install Dependencies
    pip install -r requirements.txt
    
### Run Application
    streamlit run app.py
---

## Dataset Details
### Teacher Dataset
Includes:
- Teacher ID  
- Teacher Name  
- Subject  
- Block  
- Room Number  
- Lecture Timings  
- Free Slots  
- Available Days  

### Appointments Data
- Stores student–teacher booking history  
- Includes selected slot and appointment date  

### User Data
- Stores user login credentials  
- Lightweight CSV-based storage  
---

## Future Enhancements
- AI-based teacher & slot recommendation engine  
- Email & PDF appointment confirmations  
- Advanced analytics & visual charts  
- Dark / Light theme toggle  
- NLP-based student queries  
- Gamification & student achievement badges  
- Database migration (SQL / NoSQL)  
---

## Project Author
**Shailendra Dhakad**  
*Artificial Intelligence & Machine Learning Enthusiast*
> Passionate about building intelligent systems that solve real-world problems in education, automation, and analytics.

