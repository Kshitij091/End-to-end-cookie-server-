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

# Function to set the background from an image file
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

# Page configuration
st.set_page_config(
    page_title="E2E BY RAJVEER SINGH",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setting the specific background image
set_background("image_0.png")

#                                                 
#          RAJVEER / SINGH THEME CSS (Updated for Clarity and Boldness)
#                                                 
custom_css = """
<style>
    /* Importing fonts for a professional and bold look */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Cinzel+Decorative:wght@700&family=Great+Vibes&family=Courier+New:wght@700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap');

    body, p, span, div, input, textarea, button, label {
        font-family: 'Roboto', sans-serif !important;
    }

    .stApp {
        background: transparent;
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(15, 0, 30, 0.85); /* Slightly darker, less blur for clear content */
        backdrop-filter: blur(8px);
        border-radius: 22px;
        padding: 32px;
        border: 3px solid rgba(255, 215, 0, 0.6); /* Thicker, brighter border */
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.3),
                    inset 0 0 28px rgba(255, 215, 0, 0.2);
    }

    .main-header {
        background: linear-gradient(135deg, #100020, #3a0060, #1a0033); /* Darker gradient */
        border: 3px solid #ffea00; /* Richer gold border */
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85),
                    0 0 40px rgba(255, 215, 0, 0.4);
        position: relative;
        overflow: hidden;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffea00, #fff200, #ffea00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive !important;
        font-size: 3.8rem; /* Larger font */
        font-weight: 700 !important;
        margin: 0;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.9); /* More intense shadow */
        letter-spacing: 2px;
    }

    .main-header p {
        color: #FFFFFF; /* Pure white for contrast */
        font-family: 'Great Vibes', cursive !important;
        font-size: 2.4rem; /* Larger font */
        font-weight: 700 !important;
        margin-top: 0.7rem;
        letter-spacing: 2px;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
    }

    .Couple-logo, .prince-logo {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        margin-bottom: 22px;
        border: 5px solid #ffea00;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.9),
                    inset 0 0 20px rgba(255, 255, 255, 0.5);
    }

    .stButton>button {
        background: linear-gradient(45deg, #cc9900, #ffea00, #e6b800);
        color: #000000 !important; /* Black text for bold contrast */
        border: 3px solid #cc9900;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700 !important;
        font-size: 2.1rem; /* Larger font */
        transition: all 0.4s ease;
        box-shadow: 0 10px 30px rgba(255, 215, 0, 0.6);
        text-shadow: none; /* Removed shadow for cleaner look */
        width: 100%;
        text-transform: uppercase;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 18px 50px rgba(255, 215, 0, 0.9);
        background: linear-gradient(45deg, #ffea00, #fff200, #ffea00);
        color: #000000 !important;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(20, 10, 40, 0.9); /* Darker input background */
        border: 2px solid #cc9900;
        border-radius: 14px;
        color: #FFFFFF; /* White text */
        font-weight: 700;
        padding: 1rem;
        font-size: 1.3rem; /* Larger font */
    }

    .stTextInput>div>div>input::placeholder,
    .stTextArea>div>div>textarea::placeholder {
        color: #d4af37cc;
        font-weight: 700;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ffea00;
        box-shadow: 0 0 0 5px rgba(255, 215, 0, 0.5);
        background: rgba(30, 20, 50, 1);
    }

    label {
        color: #ffea00 !important; /* Brighter gold */
        font-weight: 700 !important;
        font-size: 1.4rem !important;
        text-shadow: 2px 2px 6px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(20, 5, 40, 0.85);
        border-radius: 16px;
        padding: 10px;
        border: 2px solid #cc9900;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(60, 0, 110, 0.7);
        color: #FFFFFF; /* White for tab text */
        border-radius: 12px;
        padding: 16px 30px;
        font-weight: 700;
        font-size: 1.2rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #cc9900, #ffea00);
        color: #000000 !important; /* Black for selected tab text */
    }

    [data-testid="stMetricValue"] {
        color: #ffea00;
        font-size: 3rem; /* Larger font */
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 215, 0, 0.9);
    }

    [data-testid="stMetricLabel"] {
        color: #FFFFFF; /* White for contrast */
        font-weight: 700;
        font-size: 1.2rem;
    }

    .console-section {
        background: rgba(10, 0, 30, 0.9);
        border: 3px solid #cc9900;
        border-radius: 16px;
        padding: 22px;
        margin-top: 28px;
    }

    .console-header {
        color: #ffea00;
        font-family: 'Cinzel Decorative', cursive !important;
        font-weight: 700;
        font-size: 1.6rem;
        text-shadow: 0 0 20px #ffea00cc;
        margin-bottom: 18px;
    }

    .console-output {
        background: #000000;
        border: 2px solid #3a0060;
        border-radius: 14px;
        padding: 18px;
        color: #fff200; /* Yellow for console text */
        font-family: 'Courier New', monospace !important;
        font-size: 15px; /* Larger font */
        font-weight: 700;
        max-height: 480px;
        overflow-y: auto;
    }

    .console-line {
        background: rgba(60, 0, 110, 0.4);
        border-left: 5px solid #ffea00;
        padding: 10px 16px;
        margin: 8px 0;
        color: #fff200;
    }

    .success-box {
        background: linear-gradient(135deg, #cc9900, #ffea00);
        color: #000000;
        font-weight: 700;
        border: 3px solid #000000;
    }

    .error-box {
        background: linear-gradient(135deg, #a00000, #e01585);
        color: #FFFFFF;
        font-weight: 700;
        border: 3px solid #ffea00;
    }

    .whatsapp-btn {
        display: inline-block;
        padding: 1.2rem 3rem;
        background: linear-gradient(45deg, #008000, #32cd32, #008000);
        border: 3px solid #ffea00;
        border-radius: 16px;
        color: #FFFFFF !important; /* White text */
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        font-size: 2rem;
        text-decoration: none;
        box-shadow: 0 10px 30px rgba(0, 128, 0, 0.7);
        text-transform: uppercase;
        transition: all 0.4s ease;
    }

    .whatsapp-btn:hover {
        background: linear-gradient(45deg, #32cd32, #7fff00, #32cd32);
        transform: translateY(-5px);
        box-shadow: 0 20px 50px rgba(50, 205, 50, 0.9);
        color: #000000 !important; /* Black text on hover */
    }

    .footer {
        background: rgba(20, 5, 40, 0.9);
        border-top: 4px solid #cc9900;
        color: #FFFFFF; /* White footer text */
        font-family: 'Great Vibes', cursive !important;
        font-size: 1.8rem;
        font-weight: 700;
        padding: 3.8rem;
        text-align: center;
        text-shadow: 2px 2px 6px #000;
    }
</style>
"""

# Rest of the script remains unchanged for functionality
st.markdown(custom_css, unsafe_allow_html=True)
ADMIN_PASSWORD = "RAJVEER_SINGH_09"
WHATSAPP_NUMBER = "7520745560"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"

# Key Generation
def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

# Approval File Handling
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

# WhatsApp Message Function
def send_whatsapp_message(user_name, approval_key):
    message = f"  HELLO RAJVEER SIR   \nMy name is {user_name}\nPlease approve my key:\n  {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

# Check if key is approved
def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# Session State Initialization
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

# Class to manage automation state across threads
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

# ADMIN CONFIG
ADMIN_UID = "RAJVEER_SINGH2.0"

# --- HELPER FUNCTIONS FOR AUTOMATION ---
def log_message(msg, automation_state=None):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
   
    if automation_state:
        # Add to the thread-safe state logs
        automation_state.logs.append(formatted_msg)
    else:
        # Add to session state logs (for non-automation functions)
        if 'logs' in st.session_state:
            st.session_state.logs.append(formatted_msg)

# Function to safely find the message input element
def find_message_input(driver, process_id, automation_state=None):
    log_message(f'{process_id}: Finding message input...', automation_state)
    time.sleep(10) # Give more time for chat to load
   
    # Try to scroll a bit to trigger rendering
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except Exception:
        pass
   
    # Debug current page
    try:
        page_title = driver.title
        page_url = driver.current_url
        log_message(f'{process_id}: Page Title: {page_title}', automation_state)
        log_message(f'{process_id}: Page URL: {page_url}', automation_state)
    except Exception as e:
        log_message(f'{process_id}: Could not get page info: {e}', automation_state)
   
    # Comprehensive selectors for FB message inputs
    message_input_selectors = [
        # Content-editable div (modern FB, standard and alternative)
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"][data-lexical-editor="true"]',
        # Aria labels (with case-insensitive matching in CSS)
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        'div[contenteditable="true"][spellcheck="true"]',
        # Other common attributes
        '[role="textbox"][contenteditable="true"]',
        'textarea[placeholder*="message" i]',
        # Fallbacks for nested structures
        'div[aria-placeholder*="message" i]',
        'div[data-placeholder*="message" i]',
        # Even simpler fallbacks
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
                    # Check if actually editable using JS to be sure
                    is_editable = driver.execute_script("""
                        return arguments[0].contentEditable === 'true' ||
                               arguments[0].tagName === 'TEXTAREA' ||
                               arguments[0].tagName === 'INPUT';
                    """, element)
                   
                    if is_editable:
                        log_message(f'{process_id}: Found editable element with selector #{idx+1}', automation_state)
                       
                        # Briefly click to ensure focus
                        try:
                            element.click()
                            time.sleep(0.5)
                        except:
                            pass
                       
                        # Inspect the element found (for debugging)
                        element_text = driver.execute_script("return arguments[0].placeholder || arguments[0].getAttribute('aria-label') || arguments[0].getAttribute('aria-placeholder') || '';", element).lower()
                       
                        # If it has relevant keywords or we're using reliable selectors, it's likely the right one
                        keywords = ['message', 'write', 'type', 'send', 'chat', 'msg', 'reply', 'text', 'aa']
                        if any(keyword in element_text for keyword in keywords):
                            log_message(f'{process_id}:   Found message input with text: {element_text[:50]}', automation_state)
                            return element
                        elif idx < 10:
                            # Trust primary selectors even without text match
                            log_message(f'{process_id}:   Using primary selector editable element (#{idx+1})', automation_state)
                            return element
                        elif selector == '[contenteditable="true"]' or selector == 'textarea' or selector == 'input[type="text"]':
                            log_message(f'{process_id}:   Using fallback editable element', automation_state)
                            return element
                except Exception as e:
                    log_message(f'{process_id}: Element check failed: {str(e)[:50]}', automation_state)
                    continue
        except Exception as e:
            # Selector error, skip
            continue
   
    # Dump some page source for extreme debugging if needed
    try:
        page_source = driver.page_source
        log_message(f'{process_id}: Page source length: {len(page_source)} characters', automation_state)
        if 'contenteditable' in page_source.lower():
            log_message(f'{process_id}: Page contains contenteditable elements', automation_state)
        else:
            log_message(f'{process_id}: No contenteditable elements found in page', automation_state)
    except Exception:
        pass
   
    return None

# Setup Chrome driver in headless mode for server compatibility
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
   
    # Try to find installed chromium if it exists (for linux servers)
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
   
    # Common chromedriver locations
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
   
    # Fallback to standard initialization if paths not explicitly found
    try:
        from selenium.webdriver.chrome.service import Service
       
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', automation_state)
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', automation_state)
       
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed successfully!', automation_state)
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

# --- AUTOMATION THREAD ---
def send_messages(config, automation_state, user_id, process_id='AUTO-1'):
    driver = None
    try:
        log_message(f'{process_id}: Starting automation...', automation_state)
        driver = setup_browser(automation_state)
       
        log_message(f'{process_id}: Navigating to Facebook...', automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8) # Longer wait for server
       
        # Set cookies for authentication
        if config['cookies'] and config['cookies'].strip():
            log_message(f'{process_id}: Adding cookies...', automation_state)
            # Cookies format expected: 'name1=value1; name2=value2; ...'
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
                            # Some cookies may fail to add, ignore them
                            pass
       
        # Open the chat conversation
        if config['chat_id']:
            chat_id = config['chat_id'].strip()
            log_message(f'{process_id}: Opening conversation {chat_id}...', automation_state)
            driver.get(f'https://www.facebook.com/messages/t/{chat_id}')
        else:
            # Fallback to general messages if chat ID is not set
            log_message(f'{process_id}: Opening messages...', automation_state)
            driver.get('https://www.facebook.com/messages')
       
        # Give ample time for conversation to load, including messages and inputs
        time.sleep(15)
       
        # Find the message input box
        message_input = find_message_input(driver, process_id, automation_state)
       
        if not message_input:
            log_message(f'{process_id}: Message input not found!', automation_state)
            automation_state.running = False
            db.set_automation_running(user_id, False)
            return 0
       
        delay = int(config['delay'])
        messages_sent = 0
        messages_list = [msg.strip() for msg in config['messages'].split('\n') if msg.strip()]
       
        if not messages_list:
            messages_list = ['Hello!']
       
        # Message sending loop
        while automation_state.running:
            # Prepare message
            base_message = get_next_message(messages_list, automation_state)
           
            if config['name_prefix']:
                message_to_send = f"{config['name_prefix']} {base_message}"
            else:
                message_to_send = base_message
           
            try:
                # FB uses divs, standard focus/send_keys don't always work.
                # Complex JS to focus and input text.
                driver.execute_script("""
                    const element = arguments[0];
                    const message = arguments[1];
                   
                    element.scrollIntoView({behavior: 'smooth', block: 'center'});
                    element.focus();
                    element.click();
                   
                    // Method for contenteditable div
                    if (element.tagName === 'DIV') {
                        element.textContent = message;
                        element.innerHTML = message;
                    } else {
                        // For inputs or textareas
                        element.value = message;
                    }
                   
                    // Dispatch events to simulate input
                    element.dispatchEvent(new Event('input', { bubbles: true }));
                    element.dispatchEvent(new Event('change', { bubbles: true }));
                    element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
                """, message_input, message_to_send)
               
                # Short wait between input and send
                time.sleep(1)
               
                # Complex JS to find the send button (they are dynamic)
                sent = driver.execute_script("""
                    const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
                   
                    for (let btn of sendButtons) {
                        // Check if visible
                        if (btn.offsetParent !== null) {
                            btn.click();
                            return 'button_clicked';
                        }
                    }
                    return 'button_not_found';
                """)
               
                # If button click fails, fallback to pressing Enter
                if sent == 'button_not_found':
                    log_message(f'{process_id}: Send button not found, using Enter key...', automation_state)
                    driver.execute_script("""
                        const element = arguments[0];
                        element.focus();
                       
                        // Simulate keydown event for Enter
                        const events = [
                            new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                            new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                        ];
                       
                        events.forEach(event => element.dispatchEvent(event));
                    """, message_input)
                    log_message(f'{process_id}:   Sent via Enter: "{message_to_send[:30]}..."', automation_state)
                else:
                    log_message(f'{process_id}:   Sent via button: "{message_to_send[:30]}..."', automation_state)
               
                # Update counters
                messages_sent += 1
                automation_state.message_count = messages_sent
               
                # Wait for specified delay
                log_message(f'{process_id}: Message #{messages_sent} sent. Waiting {delay}s...', automation_state)
                time.sleep(delay)
               
            except Exception as e:
                # Don't break loop on error, just log and wait a bit
                log_message(f'{process_id}: Send error: {str(e)[:100]}', automation_state)
                time.sleep(5) # Short wait on error
       
        log_message(f'{process_id}: Automation stopped. Total messages: {messages_sent}', automation_state)
        return messages_sent
       
    except Exception as e:
        log_message(f'{process_id}: Fatal error: {str(e)}', automation_state)
        # Mark as not running on fatal error
        automation_state.running = False
        db.set_automation_running(user_id, False)
        return 0
    finally:
        # Ensure browser quits even if error occurs
        if driver:
            try:
                driver.quit()
                log_message(f'{process_id}: Browser closed', automation_state)
            except:
                pass

# --- ADMIN NOTIFICATION THREAD ---
# NEW COMPLEX FUNCTION: Navigates and sends a message to the admin to notify they started
def send_admin_notification(user_config, username, automation_state, user_id):
    driver = None
    try:
        log_message(f"ADMIN-NOTIFY: Preparing admin notification...", automation_state)
       
        # Get saved thread ID if it exists
        admin_e2ee_thread_id = db.get_admin_e2ee_thread_id(user_id)
       
        if admin_e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Using saved admin thread: {admin_e2ee_thread_id}", automation_state)
       
        # Setup and authenticate driver
        driver = setup_browser(automation_state)
       
        log_message(f"ADMIN-NOTIFY: Navigating to Facebook...", automation_state)
        driver.get('https://www.facebook.com/')
        time.sleep(8)
       
        if user_config['cookies'] and user_config['cookies'].strip():
            log_message(f"ADMIN-NOTIFY: Adding cookies...", automation_state)
            cookie_array = user_config['cookies'].split(';')
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
       
        # STRATEGY: Try various ways to open the message conversation with the admin
        user_chat_id = user_config.get('chat_id', '')
        admin_found = False
        e2ee_thread_id = admin_e2ee_thread_id
        chat_type = 'REGULAR'
       
        # Strategy A: Use saved conversation ID
        if e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Opening saved admin conversation...", automation_state)
           
            if '/e2ee/' in str(e2ee_thread_id) or admin_e2ee_thread_id:
                conversation_url = f'https://www.facebook.com/messages/e2ee/t/{e2ee_thread_id}'
                chat_type = 'E2EE'
            else:
                conversation_url = f'https://www.facebook.com/messages/t/{e2ee_thread_id}'
                chat_type = 'REGULAR'
           
            log_message(f"ADMIN-NOTIFY: Opening {chat_type} conversation: {conversation_url}", automation_state)
            driver.get(conversation_url)
            time.sleep(8)
            admin_found = True
       
        # Strategy B: Use admin profile to find message button
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: Searching for admin UID: {ADMIN_UID}...", automation_state)
           
            try:
                profile_url = f'https://www.facebook.com/{ADMIN_UID}'
                log_message(f"ADMIN-NOTIFY: Opening admin profile: {profile_url}", automation_state)
                driver.get(profile_url)
                time.sleep(8)
               
                message_button_selectors = [
                    'div[aria-label*="Message" i]',
                    'a[aria-label*="Message" i]',
                    'div[role="button"]:has-text("Message")',
                    'a[role="button"]:has-text("Message")',
                    '[data-testid*="message"]'
                ]
               
                message_button = None
                for selector in message_button_selectors:
                    try:
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            # Double check text contents or other markers
                            for elem in elements:
                                text = elem.text.lower() if elem.text else ""
                                aria_label = elem.get_attribute('aria-label') or ""
                                if 'message' in text or 'message' in aria_label.lower():
                                    message_button = elem
                                    log_message(f"ADMIN-NOTIFY: Found message button: {selector}", automation_state)
                                    break
                            if message_button:
                                break
                    except:
                        continue
               
                if message_button:
                    log_message(f"ADMIN-NOTIFY: Clicking message button...", automation_state)
                    driver.execute_script("arguments[0].click();", message_button)
                    time.sleep(8)
                   
                    # Message button usually redirects to messages page, capturing the ID
                    current_url = driver.current_url
                    log_message(f"ADMIN-NOTIFY: Redirected to: {current_url}", automation_state)
                   
                    if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                        # Extract the actual ID from the URL
                        if '/e2ee/t/' in current_url:
                            e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'E2E'
                            log_message(f"ADMIN-NOTIFY: Found E2E conversation: {e2ee_thread_id}", automation_state)
                        else:
                            e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                            chat_type = 'REGULAR'
                            log_message(f"ADMIN-NOTIFY: Found REGULAR conversation: {e2ee_thread_id}", automation_state)
                       
                        # Check it's not the user's OWN chat ID by mistake
                        if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                            # Save it for future use so we don't need profile lookup every time
                            current_cookies = user_config.get('cookies', '')
                            db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                            admin_found = True
                    else:
                        log_message(f"ADMIN-NOTIFY: Message button didn't redirect to messages page", automation_state)
                else:
                    log_message(f"ADMIN-NOTIFY: Could not find message button on profile", automation_state)
           
            except Exception as e:
                log_message(f"ADMIN-NOTIFY: Profile approach failed: {str(e)[:100]}", automation_state)
           
            # Strategy C: Type UID in new message box
            if not admin_found or not e2ee_thread_id:
                log_message(f"ADMIN-NOTIFY:  Could not find admin via search, trying DIRECT MESSAGE approach...", automation_state)
               
                try:
                    profile_url = f'https://www.facebook.com/messages/new'
                    log_message(f"ADMIN-NOTIFY: Opening new message page...", automation_state)
                    driver.get(profile_url)
                    time.sleep(8)
                   
                    search_box = None
                    search_selectors = [
                        'input[aria-label*="To:" i]',
                        'input[placeholder*="Type a name" i]',
                        'input[type="text"]'
                    ]
                   
                    for selector in search_selectors:
                        try:
                            search_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                            if search_elements:
                                for elem in search_elements:
                                    if elem.is_displayed():
                                        search_box = elem
                                        log_message(f"ADMIN-NOTIFY: Found 'To:' box with: {selector}", automation_state)
                                        break
                                if search_box:
                                    break
                        except:
                            continue
                   
                    if search_box:
                        # Typing via JS is more reliable on server
                        log_message(f"ADMIN-NOTIFY: Typing admin UID in new message...", automation_state)
                        driver.execute_script("""
                            arguments[0].focus();
                            arguments[0].value = arguments[1];
                            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                        """, search_box, ADMIN_UID)
                        time.sleep(5)
                       
                        # Complex JS logic to select the first search result
                        result_elements = driver.find_elements(By.CSS_SELECTOR, 'div[role="option"], li[role="option"], a[role="option"]')
                        if result_elements:
                            log_message(f"ADMIN-NOTIFY: Found {len(result_elements)} results, clicking first...", automation_state)
                            driver.execute_script("arguments[0].click();", result_elements[0])
                            time.sleep(8)
                           
                            # Conversation should now be open, extract ID
                            current_url = driver.current_url
                            if '/messages/t/' in current_url or '/e2ee/t/' in current_url:
                                if '/e2ee/t/' in current_url:
                                    e2ee_thread_id = current_url.split('/e2ee/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'E2EE'
                                    log_message(f"ADMIN-NOTIFY:   Direct message opened E2EE: {e2ee_thread_id}", automation_state)
                                else:
                                    e2ee_thread_id = current_url.split('/messages/t/')[-1].split('?')[0].split('/')[0]
                                    chat_type = 'REGULAR'
                                    log_message(f"ADMIN-NOTIFY:   Direct message opened REGULAR chat: {e2ee_thread_id}", automation_state)
                               
                                # Save ID if not equal to user chat ID
                                if e2ee_thread_id and e2ee_thread_id != user_chat_id and user_id:
                                    current_cookies = user_config.get('cookies', '')
                                    db.set_admin_e2ee_thread_id(user_id, e2ee_thread_id, current_cookies, chat_type)
                                    admin_found = True
                except Exception as e:
                    log_message(f"ADMIN-NOTIFY: Direct message approach failed: {str(e)[:100]}", automation_state)
       
        # CRITICAL EXIT: All approaches failed
        if not admin_found or not e2ee_thread_id:
            log_message(f"ADMIN-NOTIFY: ALL APPROACHES FAILED - Could not find/open admin conversation", automation_state)
            return
       
        # Success opening conversation, now find input and send notification message
        conversation_type = "E2EE" if "e2ee" in driver.current_url else "REGULAR"
        log_message(f"ADMIN-NOTIFY: Successfully opened {conversation_type} conversation with admin", automation_state)
       
        # Find input using same complex helper
        message_input = find_message_input(driver, 'ADMIN-NOTIFY', automation_state)
       
        if message_input:
            # Prepare notification message contents
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conversation_type = "E2EE " if "e2ee" in driver.current_url.lower() else "Regular  "
            # Format message with Unicode characters
            notification_msg = f" New User Started Automation\n\n  Username: {username}\n  Time: {current_time}\n  Chat Type: {conversation_type}\n  Thread ID: {e2ee_thread_id if e2ee_thread_id else 'N/A'}"
           
            # Input and send using JS for server compatibility
            log_message(f"ADMIN-NOTIFY: Typing notification message...", automation_state)
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
                element.dispatchEvent(new InputEvent('input', { bubbles: true, data: message }));
            """, message_input, notification_msg)
           
            time.sleep(1)
           
            log_message(f"ADMIN-NOTIFY: Trying to send message...", automation_state)
            # Complex logic for send button
            send_result = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send" i]:not([aria-label*="like" i]), [data-testid="send-button"]');
               
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return 'button_clicked';
                    }
                }
                return 'button_not_found';
            """)
           
            if send_result == 'button_not_found':
                log_message(f"ADMIN-NOTIFY: Send button not found, using Enter key...", automation_state)
                # Failover to Enter key logic
                driver.execute_script("""
                    const element = arguments[0];
                    element.focus();
                   
                    const events = [
                        new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keypress', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }),
                        new KeyboardEvent('keyup', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true })
                    ];
                   
                    events.forEach(event => element.dispatchEvent(event));
                """, message_input)
                log_message(f"ADMIN-NOTIFY:  Sent via Enter key", automation_state)
            else:
                log_message(f"ADMIN-NOTIFY: Send button clicked", automation_state)
           
            time.sleep(2) # Give a little time for message send process
        else:
            log_message(f"ADMIN-NOTIFY: Failed to find message input", automation_state)
           
    except Exception as e:
        log_message(f"ADMIN-NOTIFY:  Error sending notification: {str(e)}", automation_state)
    finally:
        if driver:
            try:
                driver.quit()
                log_message(f"ADMIN-NOTIFY: Browser closed", automation_state)
            except:
                pass

# COMPOSITE FUNCTION FOR THREAD
def run_automation_with_notification(user_config, username, automation_state, user_id):
    # STEP 1: Notify admin, complex task but crucial
    send_admin_notification(user_config, username, automation_state, user_id)
    # STEP 2: Start main message sending loop
    send_messages(user_config, automation_state, user_id)

# Setup the thread for automation so it runs in background
def start_automation(user_config, user_id):
    # Using thread-safe automation state
    automation_state = st.session_state.automation_state
   
    if automation_state.running:
        return
   
    automation_state.running = True
    automation_state.message_count = 0
    automation_state.logs = [] # Clear logs on start
   
    # Update running status in DB for persistence
    db.set_automation_running(user_id, True)
   
    # Get username for notification
    username = db.get_username(user_id)
    # Create thread and start
    # PASS THE COMPOSITE FUNCTION
    thread = threading.Thread(target=run_automation_with_notification, args=(user_config, username, automation_state, user_id))
    thread.daemon = True # Thread terminates when main thread terminates
    thread.start()

# Stop the automation thread
def stop_automation(user_id):
    # Just set running flag to False, thread will stop itself
    st.session_state.automation_state.running = False
    # Update running status in DB
    db.set_automation_running(user_id, False)

# --- PAGES ---
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
   
    # Metrics
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
   
    # Handling Pending Approvals
    if pending:
        st.markdown("####   Pending Approval Requests")
       
        for key, info in pending.items():
            # Create columns for layout
            col1, col2, col3 = st.columns([2, 2, 1])
           
            with col1:
                st.text(f"  {info['name']}")
            with col2:
                st.text(f"  {key}")
            with col3:
                # Approve button
                if st.button(" ", key=f"approve_{key}"):
                    # Move from pending to approved
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    # Refresh page
                    st.rerun()
    else:
        st.info("No pending approvals")
   
    # Handling Approved Keys
    if approved_keys:
        st.markdown("####   Approved Keys")
        for key, info in approved_keys.items():
            st.text(f"  {info['name']} -   {key}")
   
    # Logout button
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
                # Add to pending list
                pending = load_pending_approvals()
                pending[user_key] = {
                    "name": username,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
               
                # Update status
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False # Reset WhatsApp flag
                st.rerun()
       
        with col2:
            # Login as Admin button
            if st.button("  Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
   
    elif st.session_state.approval_status == 'pending':
        st.warning("  Approval Pending...")
        st.info(f"**Your Key:** `{user_key}`")
       
        whatsapp_url = send_whatsapp_message(username, user_key)
       
        # Automatically open WhatsApp only ONCE using JS
        if not st.session_state.whatsapp_opened:
            whatsapp_js = f"""
            <script>
                // Short timeout to allow page to load, then open in new tab
                setTimeout(function() {{
                    window.open('{whatsapp_url}', '_blank');
                }}, 500);
            </script>
            """
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True # Mark as opened
       
        st.success(f"  WhatsApp opening automatically for: **{username}**")
        st.markdown(f"""
        <div style="text-align: center; margin: 20px 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                Click Here to Open WhatsApp
            </a>
        </div>
        """, unsafe_allow_html=True)
       
        # Show message preview
        st.markdown("###   Message Preview:")
        st.code(f"""  HELLO RAJVEER SIR PLEASE   
My name is {username}
Please approve my key:
  {user_key}""")
       
        st.markdown("---")
       
        col1, col2 = st.columns(2)
       
        with col1:
            # Refresh/Check status button
            if st.button("  Check Approval Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("  Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("  Not approved yet. Please wait!")
       
        with col2:
            # Go back button
            if st.button("  Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False # Reset WhatsApp flag
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
                else:
                    st.error("  Invalid password!")
       
        with col2:
            # Go back button
            if st.button("  Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
   
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

def login_page():
    # Header
    st.markdown("""
    <div class="main-header">
        <img src="https://ibb.co/2Y0kPPtN.jpg" class="couple-logo">
        <h1> RAJVEER SINGH OFFLINE E2E  </h1>
        <p>səvən bıllıon smılə's ın ʈhıs world buʈ ɣour's ıs mɣ fαvourıʈəs___  </p>
    </div>
    """, unsafe_allow_html=True)
   
    # Tabs for login and signup
    tab1, tab2 = st.tabs(["  Login", "  Sign Up"])
   
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
       
        if st.button("Login", key="login_btn", use_container_width=True):
            if username and password:
                # Verify user credentials
                user_id = db.verify_user(username, password)
                if user_id:
                    # Generate user key for approval check
                    user_key = generate_user_key(username, password)
                   
                    # Set session state
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.user_key = user_key
                   
                    # Check if key is already approved
                    if check_approval(user_key):
                        st.session_state.key_approved = True
                        st.session_state.approval_status = 'approved'
                       
                        # Auto-restart automation if it was running before
                        should_auto_start = db.get_automation_running(user_id)
                        if should_auto_start:
                            # Load config first
                            user_config = db.get_user_config(user_id)
                            if user_config and user_config['chat_id']:
                                start_automation(user_config, user_id)
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                   
                    # Welcome and redirect
                    st.success(f"  Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("  Invalid username or password!")
            else:
                st.warning("   Please enter both username and password")
   
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
       
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    # Create user in DB
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"  {message} Please login now!")
                    else:
                        st.error(f"  {message}")
                else:
                    st.error("  Passwords do not match!")
            else:
                st.warning("   Please fill all fields")

def main_app():
    st.markdown('<div class="main-header"><img src="https://ibb.co/2Y0kPPtN.jpg" class="couple-logo"><h1>RAJVEER SINGH E2E OFFLINE</h1><p>Dreamed about you all night... now I just want to live that dream today. ✨❤️  </p></div>', unsafe_allow_html=True)
   
    # Check if auto-restart was already checked this session, and user is logged in
    if not st.session_state.auto_start_checked and st.session_state.user_id:
        st.session_state.auto_start_checked = True # Mark as checked for this session
        should_auto_start = db.get_automation_running(st.session_state.user_id)
       
        # Only start if it should, and is NOT already running
        if should_auto_start and not st.session_state.automation_state.running:
            # Load config first
            user_config = db.get_user_config(st.session_state.user_id)
            if user_config and user_config['chat_id']:
                # Pass both config and user_id to helper
                start_automation(user_config, st.session_state.user_id)
   
    # Sidebar
    st.sidebar.markdown(f"###   {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("  Key Approved")
   
    if st.sidebar.button("  Logout", use_container_width=True):
        # Stop automation if running before logging out
        if st.session_state.automation_state.running:
            stop_automation(st.session_state.user_id)
       
        # Clear session state
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_key = None
        st.session_state.key_approved = False
        st.session_state.automation_running = False
        st.session_state.auto_start_checked = False
        st.session_state.approval_status = 'not_requested'
        st.rerun()
   
    # Load user's automation configuration
    user_config = db.get_user_config(st.session_state.user_id)
   
    # Main Content Area
    if user_config:
        # Create tabs for config and control
        tab1, tab2 = st.tabs(["   Configuration", "  Automation"])
       
        with tab1:
            st.markdown("### Your Configuration")
           
            chat_id = st.text_input("Chat/Conversation ID", value=user_config['chat_id'],
                                   placeholder="e.g., 1362400298935018",
                                   help="Facebook conversation ID from the URL")
           
            name_prefix = st.text_input("Hatersname", value=user_config['name_prefix'],
                                       placeholder="e.g., [END TO END]",
                                       help="Prefix to add before each message")
           
            delay = st.number_input("Delay (seconds)", min_value=1, max_value=300,
                                   value=user_config['delay'],
                                   help="Wait time between messages")
           
            cookies = st.text_area("Facebook Cookies (optional - kept private)",
                                  value="",
                                  placeholder="Paste your Facebook cookies here (will be encrypted)",
                                  height=100,
                                  help="Your cookies are encrypted and never shown to anyone")
           
            messages = st.text_area("Messages (one per line)",
                                   value=user_config['messages'],
                                   placeholder="NP file copy paste karo",
                                   height=150,
                                   help="Enter each message on a new line")
           
            if st.button("  Save Configuration", use_container_width=True):
                # Update config in database (using encryption for cookies if provided)
                final_cookies = cookies if cookies.strip() else user_config['cookies']
                db.update_user_config(
                    st.session_state.user_id,
                    chat_id,
                    name_prefix,
                    delay,
                    final_cookies,
                    messages
                )
                st.success("  Configuration saved successfully!")
                st.rerun() # Refresh to update view
       
        with tab2:
            st.markdown("### Automation Control")
           
            # Re-fetch user config in this tab
            user_config = db.get_user_config(st.session_state.user_id)
           
            # Status Metrics using background automation state
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Messages Sent", st.session_state.automation_state.message_count)
            with col2:
                status = "  Running" if st.session_state.automation_state.running else "  Stopped"
                st.metric("Status", status)
            with col3:
                st.metric("Chat ID", user_config['chat_id'][:10] + "..." if user_config['chat_id'] else "Not Set")
           
            st.markdown("---")
           
            # Control Buttons
            col1, col2 = st.columns(2)
           
            with col1:
                if st.button("Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                    # Validate configuration
                    if user_config['chat_id']:
                        # Call modified start automation
                        start_automation(user_config, st.session_state.user_id)
                        st.success("  Automation started!")
                        st.rerun() # Immediate state update
                    else:
                        st.error("  Please set Chat ID in Configuration first!")
           
            with col2:
                if st.button(" Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                    # Call stop automation with user_id
                    stop_automation(st.session_state.user_id)
                    st.warning("   Automation stopped!")
                    st.rerun() # Immediate state update
           
            # Logs Area
            if st.session_state.automation_state.logs:
                st.markdown("###   Live Console Output")
               
                # Display logs (only last 30 lines)
                logs_html = '<div class="console-output">'
                for log in st.session_state.automation_state.logs[-30:]:
                    logs_html += f'<div class="console-line">{log}</div>'
                logs_html += '</div>'
               
                st.markdown(logs_html, unsafe_allow_html=True)
               
                # Manual refresh for logs, otherwise use st.session_state change to re-trigger
                if st.button("  Refresh Logs"):
                    st.rerun()
    else:
        st.warning("No configuration found. Please refresh the page!")

# --- APP FLOW ---
if not st.session_state.logged_in:
    # Not logged in -> Login or Sign up
    login_page()
elif not st.session_state.key_approved:
    # Logged in but not approved -> Request or Admin
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    # Logged in and approved -> Main app
    main_app()

# Footer
st.markdown('<div class="footer">Made with  by Rajveer singh | � 2025</div>', unsafe_allow_html=True)

