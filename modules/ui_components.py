import streamlit as st
import random

def load_css():
    st.markdown("""
    <style>
    /* Dark Futuristic Theme */
    .stApp {
        background-color: #0e1117;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #00ffff;
        font-weight: 600;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0074D9;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 8px 15px;
        transition: background-color 0.3s, transform 0.2s;
    }
    .stButton>button:hover {
        background-color: #00ffff;
        color: #000;
        transform: scale(1.05);
    }

    /* Teacher Card Style */
    .teacher-card {
        background: linear-gradient(145deg, #1f2029, #252836);
        padding: 15px;
        margin: 10px 0;
        border-radius: 12px;
        box-shadow: 0 0 10px #00ffff33;
        transition: transform 0.2s ease;
    }
    .teacher-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 15px #00ffff55;
    }
    .teacher-card h3 {
        color: #00ffff;
        margin-bottom: 5px;
    }
    .teacher-card p {
        color: #ffffff;
        margin: 0;
    }

    /* Motivational Quote Card */
    .quote-card {
        background: #1f2029;
        padding: 12px;
        margin: 8px 0;
        border-radius: 10px;
        box-shadow: 0 0 8px #00ffff33;
    }
    .quote-card h4 {
        color: #00ffff;
        margin-bottom: 5px;
    }
    .quote-card p {
        color: #fff;
        font-style: italic;
    }

    /* Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-around;
        background: #1a1d24;
        padding: 10px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px #00ffff22;
    }
    .nav-link {
        color: #00ffff;
        text-decoration: none;
        font-weight: 500;
        transition: color 0.3s, transform 0.2s;
    }
    .nav-link:hover {
        color: #ffffff;
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)

def show_navigation(selected_page: str):
    nav_items = ["Home", "Appointment", "Admin", "About"]
    st.markdown('<div class="top-nav">', unsafe_allow_html=True)

    for item in nav_items:
        if item == selected_page:
            st.markdown(f'<a class="nav-link" style="color:white;font-weight:700;">{item}</a>', unsafe_allow_html=True)
        else:
            st.markdown(f'<a class="nav-link" href="?page={item}">{item}</a>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def show_motivational_cards():
    inventors = [
        {"name": "Elon Musk", "quote": "When something is important enough, you do it even if the odds are not in your favor."},
        {"name": "Bill Gates", "quote": "Don't compare yourself with anyone in this world... if you do so, you are insulting yourself."},
        {"name": "Mark Zuckerberg", "quote": "The biggest risk is not taking any risk."},
        {"name": "Ada Lovelace", "quote": "That brain of mine is something more than merely mortal, as time will show."},
        {"name": "Steve Jobs", "quote": "Innovation distinguishes between a leader and a follower."},
        {"name": "Albert Einstein", "quote": "Imagination is more important than knowledge."},
        {"name": "Thomas Edison", "quote": "Genius is one percent inspiration and ninety-nine percent perspiration."}
    ]
    selected = random.sample(inventors, k=3)
    for inv in selected:
        st.markdown(f"""
        <div class="quote-card">
            <h4>{inv['name']}</h4>
            <p>“{inv['quote']}”</p>
        </div>
        """, unsafe_allow_html=True)
