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
import base64

def set_background(image_file):
    if os.path.exists(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

st.set_page_config(
    page_title="E2E BY RAJVEER SINGH",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

set_background("1000000802.png")

# =================================================================
#          RAJVEER / SINGH THEME CSS (UPDATED FOR MAXIMUM CLARITY)
# =================================================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Cinzel+Decorative:wght@700&family=Great+Vibes&display=swap');
    
    /* Overall Text Styling for Visibility */
    .stApp {
        background: transparent;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF !important;
    }

    .main .block-container {
        background: rgba(15, 5, 35, 0.85); /* Slightly darker for better text contrast */
        backdrop-filter: blur(15px);
        border-radius: 22px;
        padding: 32px;
        border: 2px solid rgba(255, 215, 0, 0.5);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.25);
    }

    /* Main Header */
    .main-header {
        background: linear-gradient(135deg, #120024, #310054, #1d003b);
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.8), 0 0 35px rgba(255, 215, 0, 0.4);
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
    }

    .main-header p {
        color: #FFFFFF !important;
        font-family: 'Great Vibes', cursive;
        font-size: 2.3rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
    }

    /* Input Fields (Fixed Purple Text Issue) */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(20, 10, 40, 0.95) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 14px;
        color: #FFFFFF !important; /* Changed from Purple to Crystal White */
        font-weight: 600 !important;
        font-size: 1.2rem !important;
        padding: 1rem;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #ffeb3b88 !important;
    }

    /* Labels & Headings */
    label, .stMarkdown h3, .stMarkdown h4 {
        color: #ffd700 !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        text-shadow: 2px 2px 4px #000000 !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520) !important;
        color: #000000 !important; /* Black text on Gold button for ultimate clarity */
        border: 2px solid #ffd700;
        border-radius: 16px;
        padding: 0.8rem 2rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 800;
        font-size: 1.5rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.45);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.75);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700) !important;
        color: #000000 !important;
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(20, 5, 40, 0.85);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #ffd700;
    }

    .stTabs [data-baseweb="tab"] {
        color: #ffd700 !important;
        font-size: 1.1rem;
        font-weight: bold;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700) !important;
        color: #000000 !important;
        border-radius: 12px;
    }

    /* Metrics display */
    [data-testid="stMetricValue"] {
        color: #ffeb3b !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        text-shadow: 0 0 15px rgba(255, 235, 59, 0.6);
    }
    
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600;
    }

    /* Live Console Logs */
    .console-output {
        background: #05000a !important;
        border: 2px solid #ffd700 !important;
        border-radius: 14px;
        padding: 18px;
        max-height: 480px;
        overflow-y: auto;
    }

    .console-line {
        background: rgba(255, 255, 255, 0.05);
        border-left: 4px solid #ffd700;
        padding: 9px 14px;
        margin: 7px 0;
        color: #FFEE55 !important; /* Bright Neon Yellow Log Text */
        font-family: 'Courier New', monospace;
        font-weight: 600;
    }

    /* WhatsApp Button styling */
    .whatsapp-btn {
        display: inline-block;
        background: linear-gradient(45deg, #008000, #2ea44f);
        color: #FFFFFF !important;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 50px;
        text-decoration: none;
        border: 2px solid #ffd700;
        box-shadow: 0 5px 15px rgba(0,128,0,0.4);
        font-size: 1.2rem;
    }

    /* Footer styling fixed */
    .footer {
        background: rgba(15, 5, 35, 0.9);
        border-top: 3px solid #ffd700;
        color: #FFFFFF !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.2rem;
        text-align: center;
        padding: 1.5rem;
        margin-top: 3rem;
    }
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
    message = f"  HELLO RAJVEER SIR   \nMy name is {user_name}\nPlease approve my key:\n  {approval_key}"
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

def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    if automation_state:
        automation_state.logs.append(formatted_msg)
    else:
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except:
        pass
   
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea'
    ]
   
    for selector in message_input_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                is_editable = driver.execute_script("return arguments[0].contentEditable === 'true' || arguments[0].tagName === 'TEXTAREA';", element)
                if is_editable:
                    return element
        except:
            continue
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
   
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages:
        return 'Hello!'
    if automation_state:
        message = messages[automation_state.message_rotation_index % len(messages)]
        automation_state.message_rotation_index += 1
    else:
        message = messages[0]
    return message

def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config['cookies'] and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    try:
                        driver.add_cookie({'name': name, 'value': value, 'domain': '.facebook.com', 'path': '/'})
                    except:
                        pass
       
        chat_id = config['chat_id'].strip() if config['chat_id'] else ""
        if chat_id:
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            driver.get('https://www.facebook.com/messages')
       
        time.sleep(15)
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
       
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            message_to_send = f"{config['name_prefix']} {base_message}" if config['name_prefix'] else base_message
           
            try:
                driver.execute_script("""
                    arguments[0].focus();
                    if (arguments[0].tagName === 'DIV') {
                        arguments[0].innerText = arguments[1];
                    } else {
                        arguments[0].value = arguments[1];
                    }
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """, message_input, message_to_send)
               
                time.sleep(1)
                driver.execute_script("""
                    const btn = document.querySelector('[aria-label*="Send" i], [data-testid="send-button"]');
                    if(btn) btn.click();
                """)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
                log_message(f'{process_id}: Message #{messages_sent} sent.', automation_state)
                time.sleep(delay)
            except Exception as e:
                log_message(f'{process_id}: Send error: {str(e)[:50]}', automation_state)
                time.sleep(5)
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
    finally:
        if driver:
            driver.quit()

def admin_panel():
    st.markdown("""
    <div class="main-header">
        <h1>  ADMIN PANEL  </h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
   
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
   
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
   
    if pending:
        st.markdown("### Pending Approval Requests")
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1: st.text(info['name'])
            with col2: st.text(key)
            with col3:
                if st.button("Approve", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success("Approved!")
                    st.rerun()
   
    if st.button("Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <h1>PREMIUM KEY APPROVAL REQUIRED</h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
   
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Request Approval", use_container_width=True):
                pending = load_pending_approvals()
                pending[user_key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.rerun()
        with col2:
            if st.button("Admin Panel", use_container_width=True):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
               
    elif st.session_state.approval_status == 'pending':
        st.warning("Approval Pending...")
        whatsapp_url = send_whatsapp_message(username, user_key)
        if not st.session_state.whatsapp_opened:
            components.html(f"<script>window.open('{whatsapp_url}', '_blank');</script>", height=0)
            st.session_state.whatsapp_opened = True
           
        st.markdown(f'<div style="text-align: center;"><a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Click Here to Open WhatsApp</a></div>', unsafe_allow_html=True)
       
        if st.button("Check Approval Status", use_container_width=True):
            if check_approval(user_key):
                st.session_state.key_approved = True
                st.success("Approved!")
                st.rerun()
               
    elif st.session_state.approval_status == 'admin_login':
        admin_password = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login"):
            if admin_password == ADMIN_PASSWORD:
                st.session_state.approval_status = 'admin_panel'
                st.rerun()

def login_page():
    st.markdown("""
    <div class="main-header">
        <h1> RAJVEER SINGH OFFLINE E2E  </h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___</p>
    </div>
    """, unsafe_allow_html=True)
   
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        username = st.text_input("Username", key="l_user")
        password = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login", key="l_btn", use_container_width=True):
            user_id = db.verify_user(username, password)
            if user_id:
                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username
                st.session_state.user_key = generate_user_key(username, password)
                st.session_state.key_approved = check_approval(st.session_state.user_key)
                st.rerun()
    with tab2:
        new_user = st.text_input("Choose Username", key="s_user")
        new_pass = st.text_input("Choose Password", type="password", key="s_pass")
        if st.button("Create Account", use_container_width=True):
            db.create_user(new_user, new_pass)
            st.success("Account Created! Please Login.")

def main_app():
    st.markdown('<div class="main-header"><h1>RAJVEER SINGH E2E OFFLINE</h1><p>Dreamed about you all night... ❤️</p></div>', unsafe_allow_html=True)
   
    st.sidebar.markdown(f"### User: {st.session_state.username}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
       
    user_config = db.get_user_config(st.session_state.user_id)
    if user_config:
        tab1, tab2 = st.tabs(["Configuration", "Automation Control"])
        with tab1:
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'])
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'])
            delay = st.number_input("Delay (seconds)", min_value=1, value=user_config['delay'])
            cookies = st.text_area("Facebook Cookies", value="")
            messages = st.text_area("Messages (One per line)", value=user_config['messages'])
           
            if st.button("Save Configuration"):
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, final_cookies, messages)
                st.success("Saved!")
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start Automation", use_container_width=True):
                    st.session_state.automation_state.running = True
                    threading.Thread(target=send_messages, args=(user_config, st.session_state.automation_state, st.session_state.user_id)).start()
                    st.rerun()
            with col2:
                if st.button("Stop Automation", use_container_width=True):
                    st.session_state.automation_state.running = False
                    st.rerun()
                   
            if st.session_state.automation_state.logs:
                st.markdown("### Live Console Output")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-15:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">Made with ❤️ by Rajveer singh | © 2026</div>', unsafe_allow_html=True)
