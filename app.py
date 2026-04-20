import streamlit as st
import sqlite3
import hashlib
import random
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="TYBCA AI Syllabus Master App", layout="wide", page_icon="🎓")

# ==========================================
# 🛑 SMTP EMAIL CONFIGURATION
# Instructions:
# 1. Below, enter your Gmail Address.
# 2. Enter your 16-character Google App Password (NOT your normal password).
# 3. Save the file. The Registration Portal will now email real OTPs!
# ==========================================
SMTP_EMAIL = st.secrets["SMTP_EMAIL"]
SMTP_PASSWORD = st.secrets["SMTP_PASSWORD"]
# ==========================================

# --- Database & Auth Setup ---
def init_auth_db():
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT UNIQUE,
            theme_color TEXT DEFAULT '#2563eb'
        )
    ''')
    # Migration: Add theme_color if not exists
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN theme_color TEXT DEFAULT '#2563eb'")
    except sqlite3.OperationalError:
        pass

    # Default admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        hashed_pw = hashlib.sha256("admin".encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, password, role, email, theme_color) VALUES (?, ?, ?, ?, ?)", ("admin", hashed_pw, "admin", "admin@localhost.com", "#2563eb"))
    conn.commit()
    conn.close()

init_auth_db()

def authenticate(identifier, password):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT username, role, theme_color FROM users WHERE (username=? OR email=?) AND password=?", (identifier, identifier, hashed_pw))
    user = cursor.fetchone()
    conn.close()
    return user if user else None

def check_username_exists(username):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def check_email_exists(email):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    res = cursor.fetchone()
    conn.close()
    return res is not None

def register_user(username, password, email):
    conn = sqlite3.connect("auth.db")
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    success = False
    try:
        cursor.execute("INSERT INTO users (username, password, role, email, theme_color) VALUES (?, ?, ?, ?, ?)", (username, hashed_pw, "student", email, "#2563eb"))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return success

def send_otp_email(recipient_email, otp_code):
    if SMTP_EMAIL == "your_email@gmail.com":
         return False, "SMTP completely unconfigured. Please open app.py and insert your email/password."
         
    msg = MIMEText(f"Hello Future CA Student,\n\nYour TYBCA AI Syllabus Authentication OTP is: {otp_code}\n\nDo not share this code. Input it into the Streamlit Portal to officially verify your student account!")
    msg['Subject'] = 'TYBCA AI Syllabus - Registration OTP'
    msg['From'] = SMTP_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(msg)
        return True, "Email sent successfully!"
    except smtplib.SMTPAuthenticationError:
        return False, "SMTP Authentication Failed. Ensure you are using a 16-character Google App Password."
    except Exception as e:
        return False, f"Email transmission error: {e}"

if "role" not in st.session_state:
    st.session_state["role"] = None

if "theme_color" not in st.session_state:
    st.session_state["theme_color"] = "#2563eb"

# --- Global UI Cleanup ---
if st.session_state.get("role") in [None, "student"]:
    st.markdown("""
        <style>
        /* Hide Unwanted UI Elements */
        [data-testid="stCloudAppDeployButton"], 
        [data-testid="stToolbar"], 
        .stAppToolbar,
        footer,
        #MainMenu {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            opacity: 0 !important;
        }

        /* Keep header container but make it transparent for the toggle */
        header[data-testid="stHeader"] {
            background-color: rgba(0, 0, 0, 0) !important;
            border-bottom: none !important;
            box-shadow: none !important;
        }

        /* Ensure Sidebar Toggle is visible and clean */
        [data-testid="stSidebarCollapseButton"] {
            color: #1e293b !important;
            margin-top: 5px !important;
        }

        /* Fine-tune block container padding */
        .block-container {
            padding-top: 1.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

if "otp_state" not in st.session_state:
    st.session_state.otp_state = {
        "step": 1,
        "username": "",
        "password": "",
        "email": "",
        "generated_otp": ""
    }

# --- UI Components ---
def login():
    theme_c = st.session_state.get("theme_color", "#2563eb")
    st.markdown(
        f"""
        <style>
        /* Elegant Off-White Light Gradient Background */
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, #f8fafc 0%, {theme_c}15 50%, #f1f5f9 100%);
            color: #0f172a;
        }}
        
        /* Restrict overall container max-width for perfect centering (bypasses mobile stacking) */
        [data-testid="block-container"],
        [data-testid="stMainBlockContainer"],
        .st-emotion-cache-1jicfl2,
        .stMainBlockContainer {{
            max-width: 100% !important;
            padding-top: 5rem;
            padding-bottom: 5rem;
        }}

        /* Unified Glassmorphism Card for Auth */
        div[data-testid="stVerticalBlock"] > div:has(.st-key-auth_card) > div,
        .st-key-auth_card {{
            display: flex;
            align-items: center;
            max-width: 500px !important;
            margin: 0 auto !important;
            background: rgba(255, 255, 255, 0.45) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1) !important;
            border-radius: 20px !important;
            padding: 2.5rem !important;
            animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        /* Make the inner form and radio transparent since the parent card has the glass effect */
        [data-testid="stForm"], [data-testid="stRadio"] {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
            box-shadow: none !important;
            max-width: 100% !important;
        }}
        
        /* Premium iOS-style Segmented Toggle wrapper */
        [data-testid="stRadio"] {{
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
            margin: 0 auto 1.5rem auto !important;
        }}

        /* Inner container formatting */
        [data-testid="stRadio"] > div {{
            display: flex !important;
            flex-direction: row;
            justify-content: center !important;
            background: rgba(0, 0, 0, 0.04);
            padding: 8px;
            border-radius: 50px;
            gap: 15px;
            width: fit-content !important;
            margin: 0 auto !important;
            margin-bottom: -15px !important; /* pulls the toggle tighter down towards the form */
            position: relative;
            z-index: 10;
        }}

        /* Target individual navigation option boundaries */
        [data-baseweb="radio"] {{
            background: rgba(255, 255, 255, 0.7) !important;
            padding: 10px 40px !important;
            border-radius: 40px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); /* subtle pill shadow */
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            margin: 0 !important;
        }}

        [data-baseweb="radio"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px {theme_c}33;
            background: #ffffff !important;
        }}

        /* Exterminate native Streamlit/Browser radio-selection circles! */
        [data-baseweb="radio"] > div:first-child {{
            display: none !important;
        }}

        /* Enforce bold typography inside the pills */
        [data-baseweb="radio"] p, [data-baseweb="radio"] div {{
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            color: #1e293b !important;
            margin: 0 !important;
            padding: 0 !important;
        }}

        /* Force all Text Elements to Dark Slate over the Light Background */
        [data-testid="block-container"] p,
        [data-testid="block-container"] span,
        [data-testid="block-container"] label {{
            color: #1e293b !important;
        }}

         /* Fix Streamlit Input boxes under Light Theme */
        input[type="password"], input[type="text"] {{
            background-color: rgba(255, 255, 255, 0.8) !important;
            color: #0f172a !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
        }}

        /* Animate Header */
        h1, h2, h3 {{
            width: 100% !important;
            text-align: center !important;
            color: #0f172a !important;
            animation: fadeUp 0.6s ease-out forwards;
        }}

        /* Premium Button Hover Effects */
        .stButton>button {{
            transition: all 0.3s ease;
            background: {theme_c} !important;
            background-color: {theme_c} !important;
            border: none !important;
            box-shadow: 0 4px 15px {theme_c}66;
            border-radius: 8px;
        }}

        .stButton>button p {{
            color: white !important;
            font-weight: 600;
        }}

        .stButton>button:hover {{
            transform: translateY(-2px);
            opacity: 0.9;
            box-shadow: 0 6px 20px {theme_c}88;
        }}

        /* Keyframes */
        @keyframes fadeUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Sidebar Color Tweaks */
        [data-testid="stSidebar"] {{
             background-color: #f8fafc !important;
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
            color: #1e293b !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center;'>Welcome to Applied Artificial Intelligence Model Development and Deployment</h1>", unsafe_allow_html=True)
    st.write("") # small spacer
    
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "Login"
        
    mode_idx = 0 if st.session_state.auth_mode == "Login" else 1
    
    # Unified Container Card
    with st.container(key="auth_card"):
        # Centering the toggle
        selected_mode = st.radio("Mode", ["Login", "Register"], horizontal=True, label_visibility="collapsed", index=mode_idx)
        
        if selected_mode != st.session_state.auth_mode:
            st.session_state.auth_mode = selected_mode
            st.rerun()
            
        if st.session_state.auth_mode == "Login":
            with st.form("login_form"):
                st.subheader("Login to Portal")
                identifier = st.text_input("Username or Email Address")
                password = st.text_input("Password", type="password")
                
                # Constrain Submit Button
                _, btn_col, _ = st.columns([1, 3, 1])
                with btn_col:
                    submit = st.form_submit_button("Enter", use_container_width=True)
                
                if submit:
                    user_data = authenticate(identifier, password)
                    if user_data:
                        uname, urole, utheme = user_data
                        st.session_state["username"] = uname
                        st.session_state["role"] = urole
                        st.session_state["theme_color"] = utheme
                        st.rerun()
                    else:
                        st.error("Invalid credentials.")

        elif st.session_state.auth_mode == "Register":
            if st.session_state.otp_state["step"] == 1:
                with st.form("register_form", clear_on_submit=False):
                    st.subheader("Secure Student Registration")
                    new_user = st.text_input("Username")
                    email = st.text_input("Email Address")
                    new_pass = st.text_input("Password", type="password")
                    confirm_pass = st.text_input("Confirm Password", type="password")
                    
                    _, btn_col, _ = st.columns([1, 3, 1])
                    with btn_col:
                        submit_reg = st.form_submit_button("Send Email OTP", use_container_width=True)
                    
                    if submit_reg:
                        if not new_user or not new_pass or not email:
                            st.error("Fields cannot be empty!")
                        elif "@" not in email:
                            st.error("Please enter a valid email address.")
                        elif new_pass != confirm_pass:
                            st.error("Passwords do not match!")
                        elif check_username_exists(new_user):
                            st.error("Username already exists. Pick another one.")
                        elif check_email_exists(email):
                            st.error("Email Address is already registered.")
                        else:
                            gen_otp = str(random.randint(1000, 9999))
                            success, message = send_otp_email(email, gen_otp)
                            
                            if success:
                                st.session_state.otp_state["step"] = 2
                                st.session_state.otp_state["username"] = new_user
                                st.session_state.otp_state["password"] = new_pass
                                st.session_state.otp_state["email"] = email
                                st.session_state.otp_state["generated_otp"] = gen_otp
                                st.rerun()
                            else:
                                st.error(message)
                            
            elif st.session_state.otp_state["step"] == 2:
                st.info(f"📧 An email containing a 4-digit token has been securely dispatched to **{st.session_state.otp_state['email']}**.")
                
                with st.form("otp_form", clear_on_submit=False):
                    st.subheader("Secure Student Registration")
                    entered_otp = st.text_input("Enter 4-digit Verification Token", max_chars=4)
                    
                    _, btn_col, _ = st.columns([1, 3, 1])
                    with btn_col:
                        submit_otp = st.form_submit_button("Verify & Finalize", use_container_width=True)
                    
                    if submit_otp:
                        if entered_otp == st.session_state.otp_state["generated_otp"]:
                            reg_user = st.session_state.otp_state["username"]
                            reg_pass = st.session_state.otp_state["password"]
                            reg_mail = st.session_state.otp_state["email"] 
                            
                            if register_user(reg_user, reg_pass, reg_mail):
                                st.session_state.otp_state["step"] = 1 # Reset state
                                st.session_state.auth_mode = "Login" # Jump back!
                                st.rerun()
                            else:
                                st.error("Database conflict. Try again.")
                        else:
                            st.error("Incorrect verification token. Please try again.")

                if st.button("Cancel Registration"):
                    st.session_state.otp_state["step"] = 1
                    st.rerun()

login_page = st.Page(login, title="Login / Register", icon="🔒")

# --- Routing ---
if st.session_state["role"] is None:
    pg = st.navigation([login_page])
else:
    # Sidebar logout & dynamic track selection
    st.sidebar.title(f"Welcome, {st.session_state['role'].capitalize()}!")
    if st.sidebar.button("Logout"):
        st.session_state["role"] = None
        st.rerun()
        
    st.sidebar.divider()
    
    track = "Beginner Track (CMS)"
    if st.session_state["role"] in ["admin", "faculty"]:
        st.sidebar.title("Curriculum Tracks")
        track = st.sidebar.radio(
            "Choose Track:",
            ["Beginner Track (CMS)", "Learning Track (Advanced)"],
            index=0
        )
    else:
        st.sidebar.info("Logged in as Student. Showing Beginner Track only.")

    if track == "Learning Track (Advanced)":
        pages = {
            "Overview": [
                st.Page("home.py", title="Home", icon="🏠")
            ],
            "Unit 1: Streamlit Fundamentals": [
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_1_basics.py", title="1.1 Streamlit Basics", icon="1️⃣"),
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_2_interactive_ui.py", title="1.2 Interactive UI", icon="🎛️"),
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_3_data_viz.py", title="1.3 Data Visualization", icon="📊"),
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_4_mini_dashboard.py", title="1.4 Analytics Dashboard", icon="📈"),
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_5_sqlite_connect.py", title="1.5 SQLite Integration", icon="💾"),
                st.Page("learning/Unit_1_Streamlit_Fundamentals/1_6_persistence.py", title="1.6 Data Persistence", icon="🕰️")
            ],
            "Unit 2: Learning Algorithms": [
                st.Page("learning/Unit_2_Learning_Algorithms/2_1_unsupervised.py", title="2.1 Unsupervised Algorithms", icon="🔍"),
                st.Page("learning/Unit_2_Learning_Algorithms/2_2_reinforcement_overview.py", title="2.2 Reinforcement Learning", icon="🤖"),
                st.Page("learning/Unit_2_Learning_Algorithms/2_3_ensemble_learning.py", title="2.3 Ensemble Learning", icon="🌲"),
                st.Page("learning/Unit_2_Learning_Algorithms/2_4_2_5_evaluation_tuning.py", title="2.4 & 2.5 Tuning & Eval", icon="⚙️")
            ],
            "Unit 3: Model Deployment": [
                st.Page("learning/Unit_3_Model_Deployment/streamlit_client.py", title="3.4 Flask API Client", icon="🌐")
            ],
            "Unit 4: End-to-End Workflow": [
                st.Page("learning/Unit_4_End_to_End_Workflow/frontend/app.py", title="🎓 Student Marks System", icon="🚀")
            ]
        }
    else:
        pages = {
            "Overview": [
                st.Page("home.py", title="Home", icon="🏠")
            ],
            "Unit 1: Streamlit Fundamentals": [
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_1_basics.py", title="1.1 Portal Basics", icon="1️⃣"),
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_2_interactive_ui.py", title="1.2 Student Form", icon="📝"),
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_3_data_viz.py", title="1.3 Enrollments Viz", icon="📊"),
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_4_mini_dashboard.py", title="1.4 Admin Dashboard", icon="🏫"),
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_5_sqlite_connect.py", title="1.5 Setup DB", icon="💾"),
                st.Page("beginner/Unit_1_Streamlit_Fundamentals/1_6_persistence.py", title="1.6 Manage Records", icon="🗄️")
            ],
            "Unit 2: Learning Algorithms": [
                st.Page("beginner/Unit_2_Learning_Algorithms/2_1_unsupervised.py", title="2.1 Study Groups Clustering", icon="🎯"),
                st.Page("beginner/Unit_2_Learning_Algorithms/2_2_reinforcement_overview.py", title="2.2 RL Timetables", icon="🤖"),
                st.Page("beginner/Unit_2_Learning_Algorithms/2_3_ensemble_learning.py", title="2.3 Predict Pass/Fail", icon="🌳"),
                st.Page("beginner/Unit_2_Learning_Algorithms/2_4_2_5_evaluation_tuning.py", title="2.4 Model Eval", icon="📏")
            ],
            "Unit 3: Model Deployment": [
                st.Page("beginner/Unit_3_Model_Deployment/streamlit_client.py", title="3.0 Admissions Client", icon="🎓")
            ],
            "Unit 4: End-to-End Workflow": [
                st.Page("beginner/Unit_4_End_to_End_Workflow/frontend/student_app.py", title="4.0 Student CMS App", icon="🚀")
            ]
        }
        
    # Management Section (Restricted to Admin/Faculty)
    if st.session_state["role"] in ["admin", "faculty"]:
        manage_page = {"Manage App": [st.Page("admin_dashboard.py", title="App Settings", icon="⚙️")]}
        pages = {**manage_page, **pages}
        
    pg = st.navigation(pages)

pg.run()

