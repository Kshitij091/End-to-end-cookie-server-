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
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aapki background image load karne ke liye (Aapne code me 1000000802.png rakha tha, zarurat ke hisab se rename kar lein)
try:
    set_background("1000000843.png")
except:
    try:
        set_background("1000000802.png")
    except:
        pass

# ====================================================================
#          RAJVEER / SINGH THEME CSS (UPDATED FOR TRANSPARENCY & CLARITY)
# ====================================================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Great+Vibes&family=Playfair+Display:wght@600;700&display=swap');
    
    html, body, [data-testid="stSidebar"] {
        font-family: 'Playfair Display', serif;
    }
   
    .stApp {
        background: transparent;
    }

    /* BACKGROUND IMAGE KO CLEAR DIKHANE KE LIYE IS BOX KO TRANSPARENT KIYA HAI */
    .main .block-container {
        background: rgba(0, 0, 0, 0.45) !important; /* Elegant Transparent Glass Effect */
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 22px;
        padding: 40px;
        border: 2px solid rgba(255, 215, 0, 0.6);
        box-shadow: 0 12px 45px rgba(0, 0, 0, 0.6),
                    inset 0 0 35px rgba(255, 215, 0, 0.15);
        margin-top: 20px;
        margin-bottom: 20px;
    }

    /* HEADER SECTION */
    .main-header {
        background: linear-gradient(135deg, rgba(26, 0, 51, 0.75), rgba(75, 0, 130, 0.75), rgba(42, 0, 85, 0.75));
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.8),
                    0 0 35px rgba(255, 215, 0, 0.4);
        position: relative;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffffff, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.6rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.9), 0 0 30px rgba(255, 215, 0, 0.8);
    }

    .main-header p {
        color: #FFFFFF !important; /* Pure White for high contrast */
        font-family: 'Great Vibes', cursive;
        font-size: 2.4rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
        text-shadow: 2px 2px 8px #000000;
    }

    .couple-logo, .Prince-logo, .Couple-logo {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        margin-bottom: 22px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.9);
        object-fit: cover;
    }

    /* BUTTONS STYLE */
    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520) !important;
        color: #000000 !important; /* Dark text on Gold Button makes it extremely clear */
        border: 2px solid #ffffff;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 900;
        font-size: 1.4rem !important;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.9);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700) !important;
        color: #000000 !important;
    }

    /* INPUT FIELDS - TEXT CLEARITY INSIDE TRANSPARENT BOX */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(20, 10, 40, 0.85) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 14px;
        color: #FFFFFF !important; /* Text color pure white kiya hai clarity ke liye */
        padding: 1rem;
        font-size: 1.2rem !important;
        font-weight: 600;
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: rgba(255, 235, 59, 0.6) !important;
    }

    /* ALL LABELS AND TEXT HEADINGS */
    label, .stMarkdown p, h3, h4 {
        color: #FFFFFF !important; /* Pure White text */
        font-weight: 700 !important;
        text-shadow: 2px 2px 6px #000000, 0 0 10px rgba(255, 215, 0, 0.5) !important;
    }
    
    label {
        font-size: 1.25rem !important;
    }

    /* TABS CONFIGURATION */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(0, 0, 0, 0.6);
        border-radius: 16px;
        padding: 10px;
        border: 2px solid #ffd700;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.4);
        color: #FFFFFF !important;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 700;
        text-shadow: 1px 1px 4px #000;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700) !important;
        color: #000000 !important;
    }

    /* METRICS CONTROL */
    [data-testid="stMetricValue"] {
        color: #ffd700 !important;
        font-size: 3rem !important;
        font-weight: bold !important;
        text-shadow: 2px 2px 8px #000000, 0 0 15px #ffd700;
    }

    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        text-shadow: 1px 1px 4px #000;
    }

    /* CONSOLE & LOGS */
    .console-section {
        background: rgba(0, 0, 0, 0.7);
        border: 2px solid #ffd700;
        border-radius: 16px;
        padding: 22px;
    }

    .console-output {
        background: rgba(15, 0, 26, 0.9) !important;
        border: 2px solid #4b0082;
        border-radius: 14px;
        padding: 18px;
        color: #ffeb3b !important;
        font-family: 'Courier New', monospace;
        font-weight: bold;
    }

    .whatsapp-btn {
        background: linear-gradient(45deg, #006400, #228b22, #006400) !important;
        border: 2px solid #ffd700 !important;
        color: #ffffff !important;
        padding: 12px 30px;
        font-size: 1.4rem;
        font-weight: bold;
        border-radius: 12px;
        display: inline-block;
        text-decoration: none;
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.4);
        text-shadow: 2px 2px 4px #000;
    }

    .footer {
        background: rgba(0, 0, 0, 0.6);
        border-top: 3px solid #ffd700;
        color: #ffffff !important;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        padding: 2rem;
        text-align: center;
        text-shadow: 2px 2px 5px #000;
        margin-top: 30px;
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
    except Exception:
        pass
   
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
   
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
   
    log_message(f'{process_id}: Trying {len(message_input_selectors)} selectors...', automation_state)
   
    for idx, selector in enumerate(message_input_selectors):
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            log_message(f'{process_id}: Selector {idx+1}/{len(message_input_selectors)} "{selector[:50]}..." found {len(elements)} elements', automation_state)
           
            for element in elements:
                try:
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                   
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                       
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                       
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                       
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}:   Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            log_message(f'{process_id}:   Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}:   Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            continue
   
    return None

def setup_browser(automation_state=None):
    log_message('Setting up Chrome browser...', automation_state)
   
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
   
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
   
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', automation_state)
            break
   
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
   
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', automation_state)
            break
   
    try:
        from selenium.webdriver.chrome.service import Service
       
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
       
        driver.set_window_size(1920, 1080)
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', automation_state)
        raise error

def get_next_message(messages, automation_state=None):
    if not messages or len(messages) == 0:
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
       
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if config['cookies'] and config['cookies'].strip():
            cookie_array = config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        name = cookie_trimmed[:first_equal_index].strip()
                        value = cookie_trimmed[first_equal_index + 1:].strip()
                        try:
                            driver.add_cookie({
                                'name': name,
                                'value': value,
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except Exception:
                            pass
       
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            driver.get('https://www.facebook.com/messages')
       
        time.sleep(15)
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
       
        if not messages_list:
            messages_list = ['Hello!']
       
        while automation_state.running:
            base_message = get_next_message(messages_list, automation_state)
            message_to_send = f"{config['name_prefix']} {base_message}" if config['name_prefix'] else base_message
           
            try:
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        element.value = message;
                    }
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                """, message_input, message_to_send)
               
                time.sleep(1)
               
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    for (let btn of sendButtons) {
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
               
                if sent == 'button_not_found':
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                        element.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
                    """, message_input)
               
                messages_sent += 1
                automation_state.message_count = messages_sent
                time.sleep(delay)
               
            except Exception as e:
                time.sleep(5)
       
        return messages_sent
    except Exception as e:
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
        driver = setup_browser(automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if user_config['cookies'] and user_config['cookies'].strip():
            cookie_array = user_config['cookies'].split(';')
            for cookie in cookie_array:
                cookie_trimmed = cookie.strip()
                if cookie_trimmed:
                    first_equal_index = cookie_trimmed.find('=')
                    if first_equal_index > 0:
                        try:
                            driver.add_cookie({
                                'name': cookie_trimmed[:first_equal_index].strip(),
                                'value': cookie_trimmed[first_equal_index + 1:].strip(),
                                'domain': '.facebook.com',
                                'path': '/'
                            })
                        except:
                            pass
       
        user_chat_id = user_config.get('chat_id', '')
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
       
        if e2ee_thread_id:
            conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}' if '/e2ee/' in str(e2ee_thread_id) or admin_e2ee_thread_id else f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
       
        if not admin_found or not e2ee_thread_id:
            try:
                driver.get(f'https://www.facebook.com/{ADMIN_UID}')
                time.sleep(8)
                elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label*="Message" i], a[aria-label*="Message" i]')
                if elements:
                    driver.execute_script("arguments[0].click();", elements[0])
                    time.sleep(8)
                    current_url = driver.current_url
                    if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                        e2ee_thread_id = current_url.split('/t/')[-1].split('?')[0].split('/')[0]
                        if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                            db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, user_config.get('cookies', ''), 'REGULAR')
                            admin_found = True
            except:
                pass
       
        if admin_found:
            message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
            if message_input:
                from datetime import datetime
                notification_msg = f" New User Started Automation\n\n  Username: {username}\n  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                driver.execute_script("""
                    arguments[0].textContent = arguments[1];
                    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                """, message_input, notification_msg)
                time.sleep(1)
                driver.execute_script("""
                    const btn = document.querySelector('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                    if(btn) btn.click();
                """)
                time.sleep(2)
    except:
        pass
    finally:
        if driver:
            try: driver.quit()
            except: pass

def run_automation_with_notification(user_config, username, automation_state, user_id):
    send_admin_notification(user_config, username, automation_state, user_id)
    send_messages(user_config, automation_state, user_id)

def start_automation(user_config, user_id):
    automation_state = st.session_state.automation_state
    if automation_state.running:
        return
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = []
    db.set_automation_running(user_id, True)
    username = db.get_username(user_id)
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True
    thread.start()

def stop_automation(user_id):
    st.session_state.automation_state.running = False
    db.set_automation_running(user_id, False)

def admin_panel():
    st.markdown("""
    <div class="main-header">
        <img src="https://ibb.co/2Y0kPPtN.jpg" class="Couple-logo">
        <h1>  ADMIN PANEL  </h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
   
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
   
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
   
    if pending:
        st.markdown("####   Pending Approval Requests")
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1: st.text(f"  {info['name']}")
            with col2: st.text(f"  {key}")
            with col3:
                if st.button("Approve", key=f"approve_{key}"):
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
        for key, info in approved_keys.items():
            st.text(f"  {info['name']} -   {key}")
   
    if st.button("  Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <img src="https://ibb.co/2Y0kPPtN.jpg" class="Couple-logo">
        <h1>PREMIUM KEY APPROVAL REQUIRED</h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
   
    if st.session_state.approval_status == 'not_requested':
        st.markdown("###   Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
       
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("  Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
        with col2:
            if st.button("  Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
   
    elif st.session_state.approval_status == 'pending':
        st.warning("  Approval Pending...")
        whatsapp_url = send_whatsapp_message(username, user_key)
       
        if not st.session_state.whatsapp_opened:
            components.html(f"<script>setTimeout(function() {{ window.open('{whatsapp_url}', '_blank'); }}, 500);</script>", height=0)
            st.session_state.whatsapp_opened = True
       
        st.markdown(f'<div style="text-align: center; margin: 20px 0;"><a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">Click Here to Open WhatsApp</a></div>', unsafe_allow_html=True)
       
        col1, col2 = st.columns(2)
        with col1:
            if st.button("  Check Approval Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("  Approved! Redirecting...")
                    st.rerun()
        with col2:
            if st.button("  Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("###   Admin Login")
        admin_password = st.text_input("Enter Admin Password:", type="password", key="admin_password_input")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("  Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else: st.error("Invalid password!")
        with col2:
            if st.button("  Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()

def login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://ibb.co/2Y0kPPtN.jpg" class="couple-logo">
        <h1> RAJVEER SINGH OFFLINE E2E  </h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___  </p>
    </div>
    """, unsafe_allow_html=True)
   
    tab1, tab2 = st.tabs(["  Login", "  Sign Up"])
    with tab1:
        st.markdown("### Welcome Back!")
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
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                    st.rerun()
                else: st.error("Invalid username or password!")

    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password == confirm_password:
                success, message = db.create_user(new_username, new_password)
                if success: st.success("Account created! Please login.")
                else: st.error(message)

def main_app():
    st.markdown('<div class="main-header"><img src="https://ibb.co/2Y0kPPtN.jpg" class="couple-logo"><h1>RAJVEER SINGH E2E OFFLINE</h1><p>Dreamed about you all night... now I just want to live that dream today. ✨❤️  </p></div>', unsafe_allow_html=True)
   
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True
        if db.get_automation_running(st.session_state.user_id) and not st.session_state.automation_state.running:
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']: start_automation(user_config, st.session_state.user_id)
   
    st.sidebar.markdown(f"###   {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.success("  Key Approved")
   
    if st.sidebar.button("Logout", use_container_width=True):
        if st.session_state.automation_state.running: stop_automation(st.session_state.user_id)
        st.session_state.logged_in = False
        st.rerun()
   
    user_config = db.get_user_config(st.session_state.user_id)
    if user_config:
        tab1, tab2 = st.tabs(["   Configuration", "  Automation"])
        with tab1:
            st.markdown("### Your Configuration")
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'])
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'])
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300, value=user_config['delay'])
            cookies = st.text_area("Facebook Cookies (optional)", value="", placeholder="Paste new cookies here...")
            messages = st.text_area("Messages (one per line)", value=user_config['messages'], height=150)
           
            if st.button("Save Configuration", use_container_width=True):
                db.update_user_config(st.session_state.user_id, chat_id, name_prefix, delay, cookies if cookies.strip() else user_config['cookies'], messages)
                st.success("Configuration saved!")
                st.rerun()
       
        with tab2:
            st.markdown("### Automation Control")
            col1, col2, col3 = st.columns(3)
            col1.metric("Messages Sent", st.session_state.automation_state.message_count)
            col2.metric("Status", "Running" if st.session_state.automation_state.running else "Stopped")
            col3.metric("Chat ID", user_config['chat_id'][:10] + "..." if user_config['chat_id'] else "Not Set")
           
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    if user_config['chat_id']:
                        start_automation(user_config, st.session_state.user_id)
                        st.rerun()
                    else: st.error("Please set Chat ID first!")
            with col2:
                if st.button("Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    stop_automation(st.session_state.user_id)
                    st.rerun()
           
            if st.session_state.automation_state.logs:
                st.markdown("### Live Console Output")
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-25:]:
                    logs_html += f'<div style="border-left: 4px solid #ffd700; padding: 5px; margin: 5px 0;">{log}</div>'
                logs_html += '</div>'
                st.markdown(logs_html, unsafe_allow_html=True)

if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">Made with ❤️ by Rajveer singh | © 2026</div>', unsafe_allow_html=True)
      
