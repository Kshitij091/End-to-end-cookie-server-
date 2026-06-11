import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import database as db
import requests

# Background image URL (your couple image)
BACKGROUND_IMAGE_URL = "https://i.ibb.co/2Y0kPPtN.jpg"

st.set_page_config(
    page_title="E2E BY RAJVEER SINGH",
    page_icon=" ",
    layout="wide",
    initial_sidebar_state="expanded"
)

#                                                 
#          RAJVEER / SINGH THEME CSS (UPDATED FOR IMAGE BACKGROUND)
#                                                 
custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * {{
        font-family: 'Playfair Display', serif;
    }}

    /* Full-screen background image */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.6)), 
                          url('{BACKGROUND_IMAGE_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Main container styling for readability over image */
    .main .block-container {{
        background: rgba(10, 0, 20, 0.75); /* Dark semi-transparent overlay */
        backdrop-filter: blur(8px);
        border-radius: 22px;
        padding: 32px;
        margin-top: 20px;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.1),
                    inset 0 0 28px rgba(255, 215, 0, 0.05);
    }}

    /* Redesigned main header with text only for better fit */
    .main-header {{
        background: linear-gradient(135deg, rgba(26, 0, 51, 0.9), rgba(75, 0, 130, 0.9), rgba(42, 0, 85, 0.9));
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.6),
                    0 0 35px rgba(255, 215, 0, 0.2);
        position: relative;
        overflow: hidden;
    }}

    .main-header::before {{
        content: " ";
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 6.5rem;
        opacity: 0.1;
        color: #ffd700;
    }}

    .main-header h1 {{
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }}

    .main-header p {{
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.6rem;
        margin-top: 0.5rem;
        letter-spacing: 1.5px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
    }}

    /* Adjust content images to be smaller and decorative, not background */
    .content-logo {{
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 15px;
        border: 3px solid #ffd700;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.6);
    }}

    .stButton>button {{
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 0.9rem 2.2rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 7px 20px rgba(255, 215, 0, 0.35);
        text-shadow: 1px 1px 2px rgba(0,0,0,0.4);
        width: 100%;
    }}

    .stButton>button:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(255, 215, 0, 0.65);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }}

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {{
        background: rgba(40, 20, 80, 0.6);
        border: 2px solid #b8860b;
        border-radius: 12px;
        color: #ffd700;
        padding: 0.9rem;
        font-size: 1.05rem;
    }}

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {{
        color: rgba(212, 175, 55, 0.6);
    }}

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: #ffd700;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.25);
        background: rgba(50, 30, 90, 0.7);
    }}

    label {{
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 3px #000;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(30, 10, 60, 0.5);
        border-radius: 14px;
        padding: 8px;
        border: 1px solid #b8860b;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: rgba(75, 0, 130, 0.4);
        color: #d4af37;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
    }}

    [data-testid="stMetricValue"] {{
        color: #ffd700;
        font-size: 2.4rem;
        font-weight: 700;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }}

    [data-testid="stMetricLabel"] {{
        color: #d4af37;
        font-weight: 500;
    }}

    .console-section {{
        background: rgba(20, 0, 40, 0.6);
        border: 2px solid #b8860b;
        border-radius: 14px;
        padding: 20px;
        margin-top: 25px;
    }}

    .console-header {{
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
        margin-bottom: 15px;
    }}

    .console-output {{
        background: rgba(15, 0, 26, 0.9);
        border: 2px solid #4b0082;
        border-radius: 12px;
        padding: 15px;
        color: #ffeb3b;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
    }}

    .console-line {{
        background: rgba(75, 0, 130, 0.2);
        border-left: 4px solid #ffd700;
        padding: 8px 12px;
        margin: 6px 0;
        color: #ffeb3b;
    }}

    .success-box {{
        background: linear-gradient(135deg, rgba(184, 134, 11, 0.9), rgba(255, 215, 0, 0.9));
        color: #1a0033;
        border: 2px solid #1a0033;
    }}

    .error-box {{
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.9), rgba(199, 21, 133, 0.9));
        border: 2px solid #ffd700;
    }}

    .whatsapp-btn {{
        background: linear-gradient(45deg, #006400, #228b22, #006400);
        border: 2px solid #ffd700;
        color: #ffd700;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        padding: 12px 24px;
        border-radius: 14px;
        text-decoration: none;
        display: inline-block;
        box-shadow: 0 7px 20px rgba(0, 100, 0, 0.45);
        transition: all 0.3s ease;
    }}

    .whatsapp-btn:hover {{
        background: linear-gradient(45deg, #228b22, #32cd32, #228b22);
        transform: translateY(-4px);
        box-shadow: 0 12px 35px rgba(50, 205, 50, 0.6);
        color: #1a0033;
    }}

    .footer {{
        background: rgba(30, 10, 60, 0.7);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.4rem;
        padding: 2.2rem;
        text-align: center;
        text-shadow: 1px 1px 4px #000;
        position: relative;
        bottom: 0;
        width: 100%;
        margin-top: 30px;
    }}
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {{
        .main-header h1 {{ font-size: 2.2rem; }}
        .main-header p {{ font-size: 1.3rem; }}
        .stTabs [data-baseweb="tab"] {{ padding: 10px 16px; font-size: 0.9rem; }}
    }}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

ADMIN_PASSWORD = "RAJVEER_SINGH_09"
WHATSAPP_NUMBER = "7520745560"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"HELLO RAJVEER SIR   \nMy name is {user_name}\nPlease approve my key:\n{approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'message_count' not in st.session_state:
    st.session_state.message_count = 0
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False

class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

if 'auto_start_checked' not in st.session_state:
    st.session_state.auto_start_checked = False

ADMIN_UID = "RAJVEER_SINGH2.0"

# ... [Automation functions find_message_input, setup_browser, etc. remain the same] ...

def admin_panel():
    st.markdown("""
    <div class="main-header">
        <h1>  ADMIN PANEL  </h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
   
    # Added defensive style for text inputs in admin panel if needed
    st.markdown('<style>.stTextInput label { color: #d4af37 !important; text-shadow: 1px 1px 2px #000; }</style>', unsafe_allow_html=True)

    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
   
    # Modified metric styling for admin view
    col1_m, col2_m = st.columns(2)
    with col1_m: st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    with col2_m: st.warning(f"**Pending Approvals:** {len(pending)}")
   
    if pending:
        st.markdown("####   Pending Approval Requests")
       
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
           
            with col1:
                st.text(f"{info['name']}")
            with col2:
                st.text(f"{key}")
            with col3:
                # Optimized button styling
                if st.button(" ", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("No pending approvals")
   
    if approved_keys:
        st.markdown("####   Approved Keys")
        # Optimization: scrollable area for long approved key list
        keys_html = '<div style="max-height: 300px; overflow-y: auto; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;">'
        for key, info in approved_keys.items():
            keys_html += f'<div style="color: #ffeb3b; font-family: monospace; padding: 5px; border-bottom: 1px solid rgba(255,215,0,0.1);">{info["name"]} - {key}</div>'
        keys_html += '</div>'
        st.markdown(keys_html, unsafe_allow_html=True)
   
    st.markdown("---")
    if st.button("Logout", key="admin_logout_btn", use_container_width=True):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    st.markdown(f"""
    <div class="main-header">
        <div style="text-align: center;">
            <img src="{BACKGROUND_IMAGE_URL}" class="content-logo" alt="logo">
        </div>
        <h1> PREMIUM KEY REQUIRED </h1>
        <p>ONE MONTH 500 RS PAID - Contact Rajveer</p>
    </div>
    """, unsafe_allow_html=True)
   
    # Style override for code display to improve readability over background
    st.markdown("""
        <style>
            code { 
                background: rgba(15, 0, 26, 0.8) !important;
                color: #ffeb3b !important;
                border: 1px solid #b8860b !important;
            }
        </style>
    """, unsafe_allow_html=True)

    if st.session_state.approval_status == 'not_requested':
        st.markdown("###   Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
       
        col1, col2 = st.columns([1, 1])
       
        with col1:
            if st.button("Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {
                    "name": username,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
               
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
       
        with col2:
            if st.button("Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
   
    elif st.session_state.approval_status == 'pending':
        st.warning("  Approval Pending...")
        st.info(f"**Your Key:** `{user_key}`")
       
        whatsapp_url = send_whatsapp_message(username, user_key)
       
        if not st.session_state.whatsapp_opened:
            whatsapp_js = f"""
            <script>
                setTimeout(function() {{
                    window.open('{whatsapp_url}', '_blank');
                }}, 500);
            </script>
            """
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True
       
        st.success(f"  WhatsApp opening automatically for: **{username}**")
        st.markdown(f"""
        <div style="text-align: center; margin: 25px 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                Click Here to Open WhatsApp manually
            </a>
        </div>
        """, unsafe_allow_html=True)
       
        st.markdown("###   Message Preview:")
        st.code(f"""HELLO RAJVEER SIR PLEASE   
My name is {username}
Please approve my key:
{user_key}""")
       
        st.markdown("---")
       
        col1, col2 = st.columns(2)
       
        with col1:
            if st.button("Check Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("  Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Not approved yet.")
       
        with col2:
            if st.button("Back to Login", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("###   Admin Login")
       
        # Defensive style for text input labels in admin view
        st.markdown('<style>.stTextInput label { color: #ffd700 !important; text-shadow: 1px 1px 2px #000; }</style>', unsafe_allow_html=True)
        admin_password = st.text_input("Enter Admin Password:", type="password", key="admin_password_input")
       
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("  Invalid password!")
       
        with col2:
            if st.button("Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

def login_page():
    st.markdown(f"""
    <div class="main-header">
        <div style="text-align: center;">
            <img src="{BACKGROUND_IMAGE_URL}" class="content-logo" alt="logo">
        </div>
        <h1> RAJVEER SINGH E2E </h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___</p>
    </div>
    """, unsafe_allow_html=True)
   
    tab1, tab2 = st.tabs(["  Login", "  Sign Up"])
   
    with tab1:
        st.markdown("### Welcome Back!")
        # Defensive style for labels over the background image
        st.markdown('<style>.stTextInput label { color: #ffd700 !important; text-shadow: 1px 1px 3px #000; }</style>', unsafe_allow_html=True)
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
       
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    user_key = generate_user_key(username, password)
                   
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.user_key = user_key
                   
                    if check_approval(user_key):
                        st.session_state.key_approved = True
                        st.session_state.approval_status = 'approved'
                       
                        # Auto-start logic removed for simplicity on login, triggered in main_app
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                   
                    st.success(f"  Welcome back, {username}!")
                    time.sleep(0.5) # small delay for feedback
                    st.rerun()
                else:
                    st.error("  Invalid username or password!")
            else:
                st.warning("   Please enter both username and password")
   
    with tab2:
        st.markdown("### Create New Account")
        # Same label style as Tab 1
        st.markdown('<style>.stTextInput label { color: #ffd700 !important; text-shadow: 1px 1px 3px #000; }</style>', unsafe_allow_html=True)
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
       
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"  {message} Please login now!")
                        time.sleep(1)
                        # Optional: Automatically switch to login tab logic if desired, but default rerun to sign up tab is fine
                    else:
                        st.error(f"  {message}")
                else:
                    st.error("  Passwords do not match!")
            else:
                st.warning("   Please fill all fields")

def main_app():
    # Defensive style to make metrics readable over the blurred background area if blur is not enough
    st.markdown('<style>[data-testid="stMetricValue"] { text-shadow: 0 0 10px #000; }</style>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="main-header"><div style="text-align: center;"><img src="{BACKGROUND_IMAGE_URL}" class="content-logo"></div><h1> RAJVEER SINGH OFFLINE E2E </h1><p>Dreamed about you all night... now I just want to live that dream today. ✨❤️</p></div>', unsafe_allow_html=True)
   
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        should_auto_start = db.get_automation_running(st.session_state.user_id)
        if should_auto_start and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                start_automation(user_config, st.session_state.user_id)
   
    st.sidebar.markdown(f"###   {st.session_state.username}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("  Key Approved")
   
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
       
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_key = None
        st.session_state.key_approved = False
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.session_state.approval_status = 'not_requested'
        st.rerun()
   
    user_config = db.get_user_config(st.session_state.user_id)
   
    if user_config:
        # Optimization: Add defensive style for all inputs in the main area within main_app
        st.markdown('<style>.stTextInput label, .stTextArea label, .stNumberInput label { color: #ffd700 !important; text-shadow: 1px 1px 3px #000; }</style>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([" Configuration", " Automation Control"])
       
        with tab1:
            st.markdown("### Your Configuration")
           
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018")
           
            name_prefix = st.text_input("Hatersname (Optional Prefix)", value=user_config['name_prefix'],
                                       placeholder="e.g., [OFFLINE E2E]")
           
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config['delay'])
           
            # Updated placeholder to hint how to provide cookies
            cookies = st.text_area("Facebook Cookies (Format: c_user=...; xs=...)",
                                  value="",
                                  placeholder="Paste complete cookie string here (will be encrypted)",
                                  height=100)
           
            messages = st.text_area("Messages (one per line)",
                                   value=user_config['messages'],
                                   placeholder="Paste your message file contents here",
                                   height=150)
           
            if st.button("Save Configuration", use_container_width=True):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("Configuration saved successfully!")
                time.sleep(1)
                st.rerun()
       
        with tab2:
            st.markdown("### Automation Dashboard")
           
            user_config = db.get_user_config(st.session_state.user_id)
           
            # Re-read metrics for tab 2
            m_count = st.session_state.automation_state.message_count
            m_status = "Running" if st.session_state.automation_state.running else "Stopped"
            m_chat = user_config['chat_id'][:10] + "..." if user_config['chat_id'] else "Not Set"

            st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-around; text-align: center;">
                        <div>
                            <div style="color: #d4af37; font-weight: 500;">Sent</div>
                            <div style="color: #ffd700; font-size: 2rem; font-weight: 700; text-shadow: 0 0 10px #000;">{m_count}</div>
                        </div>
                        <div>
                            <div style="color: #d4af37; font-weight: 500;">Status</div>
                            <div style="color: #ffd700; font-size: 2rem; font-weight: 700; text-shadow: 0 0 10px #000;">{m_status}</div>
                        </div>
                        <div>
                            <div style="color: #d4af37; font-weight: 500;">Chat ID</div>
                            <div style="color: #ffd700; font-size: 2rem; font-weight: 700; text-shadow: 0 0 10px #000;">{m_chat}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
           
            st.markdown("---")
           
            col1, col2 = st.columns(2)
           
            with col1:
                # Optimized button logic with disabled state
                st_button = st.button("Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True)
                if st_button:
                    if user_config['chat_id']:
                        start_automation(user_config, st.session_state.user_id)
                        st.success("Automation started!")
                        st.rerun()
                    else:
                        st.error("Please set Chat ID in Configuration first!")
           
            with col2:
                sp_button = st.button("Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True)
                if sp_button:
                    stop_automation(st.session_state.user_id)
                    st.warning("Automation stopped!")
                    st.rerun()
           
            if st.session_state.automation_state.logs:
                st.markdown("###   Live Console Output")
               
                logs_html = '<div class="console-output">'
                # Limit logs to last 30 lines for performance
                log_subset = st.session_state.automation_state.logs[-30:]
                for log in log_subset:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
               
                st.markdown(logs_html, unsafe_allow_html=True)
               
                st.markdown('<div style="margin-top: 10px; text-align: center;">', unsafe_allow_html=True)
                if st.button("Refresh Logs manually", key="refresh_logs_btn"):
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("No configuration found. Please refresh the page!")

# --- [Application execution logic remains the same] ---
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">Made with by Rajveer singh | © 2025 </div>'unsafe_allow_html=True)
