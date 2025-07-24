import os
import time
import json
import random
from datetime import datetime
from itertools import cycle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
CONFIG_FILE = 'config.json'

# Create necessary directories and files
def create_directories_and_files():
    # Create directories
    os.makedirs('logs', exist_ok=True)
    os.makedirs('cookies', exist_ok=True)
    
    # Create files if they don't exist
    for file_path in ['logs/logs.log', 'logs/comment_stats.json', 'logs/errors.log']:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                if 'comment_stats.json' in file_path:
                    json.dump({}, f)
                else:
                    f.write('')

# Load configuration from JSON
def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("=" * 60)
        print("❌ ERROR: Configuration file not found!")
        print("=" * 60)
        print(f"The required file '{CONFIG_FILE}' is missing from the project root.")
        print()
        print("📋 To fix this issue:")
        print("1. Copy 'config-example.json' to 'config.json'")
        print("2. Edit 'config.json' with your Instagram accounts and settings")
        print("3. For more information, refer to the doc/CONFIG-README.md file")
        print()
        print("💡 The config.json file should contain:")
        print("   • accounts: Array of Instagram username/password objects")
        print("   • comments: Array of comments to post")
        print("   • hashtags: Array of hashtags to target")
        print("   • settings: Configuration for timing and behavior")
        print("   • paths: File and directory paths")
        print()
        print("Example structure:")
        print("""   {
     "accounts": [
       {"username": "your_username", "password": "your_password"}
     ],
     "comments": ["Great post!", "Love this! ❤️"],
     "hashtags": ["#example", "#hashtag"],
     "settings": {
       "daily_limit_per_account": 200,
       "comments_per_session_min": 2,
       "comments_per_session_max": 5,
       "delay_between_comments_min": 420,
       "delay_between_comments_max": 480,
       "delay_between_sessions": 5,
       "headless_mode": false,
       "scroll_count_for_posts": 2,
       "scroll_delay": 3,
       "login_delay": 8,
       "comment_box_retries": 5,
       "post_button_wait_attempts": 10
     },
     "paths": {
       "chromedriver_path": "chrome/chromedriver.exe",
       "log_file": "logs/logs.log",
       "stats_file": "logs/comment_stats.json",
       "error_log_file": "logs/errors.log",
       "cookies_dir": "cookies"
     }
   }""")
        print("=" * 60)
        exit(1)
    
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print("=" * 60)
        print("❌ ERROR: Invalid JSON in config.json!")
        print("=" * 60)
        print(f"JSON parsing error: {e}")
        print()
        print("📋 To fix this issue:")
        print("1. Check your config.json file for syntax errors")
        print("2. Use a JSON validator to verify the format")
        print("3. Ensure all strings are properly quoted")
        print("4. Check for missing commas or brackets")
        print("=" * 60)
        exit(1)
    
    # Validate required fields
    validation_errors = []
    
    if not config.get('accounts'):
        validation_errors.append("• Missing or empty 'accounts' array")
    elif not isinstance(config['accounts'], list):
        validation_errors.append("• 'accounts' must be an array")
    else:
        for i, account in enumerate(config['accounts']):
            if not isinstance(account, dict):
                validation_errors.append(f"• Account {i+1} must be an object")
            elif not account.get('username') or not account.get('password'):
                validation_errors.append(f"• Account {i+1} missing 'username' or 'password'")
    
    if not config.get('comments'):
        validation_errors.append("• Missing or empty 'comments' array")
    elif not isinstance(config['comments'], list):
        validation_errors.append("• 'comments' must be an array")
    
    if not config.get('hashtags'):
        validation_errors.append("• Missing or empty 'hashtags' array")
    elif not isinstance(config['hashtags'], list):
        validation_errors.append("• 'hashtags' must be an array")
    
    # Validate settings section
    if not config.get('settings'):
        validation_errors.append("• Missing 'settings' section")
    elif not isinstance(config['settings'], dict):
        validation_errors.append("• 'settings' must be an object")
    
    # Validate paths section
    if not config.get('paths'):
        validation_errors.append("• Missing 'paths' section")
    elif not isinstance(config['paths'], dict):
        validation_errors.append("• 'paths' must be an object")
    
    if validation_errors:
        print("=" * 60)
        print("❌ ERROR: Invalid config.json structure!")
        print("=" * 60)
        print("The following issues were found in your config.json:")
        print()
        for error in validation_errors:
            print(error)
        print()
        print("📋 To fix this issue:")
        print("1. Check the config-example.json file for the correct structure")
        print("2. Ensure all required fields are present and properly formatted")
        print("3. Verify that accounts have both 'username' and 'password' fields")
        print("4. Make sure 'settings' and 'paths' sections are included")
        print("5. Copy config-example.json to config.json if you're missing sections")
        print("=" * 60)
        exit(1)
    
    return config

# Initialize directories and files
create_directories_and_files()

CONFIG = load_config()
HASHTAGS = CONFIG.get('hashtags')

# Load settings with defaults
SETTINGS = CONFIG.get('settings', {})
DAILY_LIMIT_PER_ACCOUNT = SETTINGS.get('daily_limit_per_account', 200)
COMMENTS_PER_SESSION_MIN = SETTINGS.get('comments_per_session_min', 2)
COMMENTS_PER_SESSION_MAX = SETTINGS.get('comments_per_session_max', 5)
DELAY_BETWEEN_COMMENTS_MIN = SETTINGS.get('delay_between_comments_min', 420)
DELAY_BETWEEN_COMMENTS_MAX = SETTINGS.get('delay_between_comments_max', 480)
DELAY_BETWEEN_SESSIONS = SETTINGS.get('delay_between_sessions', 5)
HEADLESS_MODE = SETTINGS.get('headless_mode', False)
SCROLL_COUNT_FOR_POSTS = SETTINGS.get('scroll_count_for_posts', 2)
SCROLL_DELAY = SETTINGS.get('scroll_delay', 3)
LOGIN_DELAY = SETTINGS.get('login_delay', 8)
COMMENT_BOX_RETRIES = SETTINGS.get('comment_box_retries', 5)
POST_BUTTON_WAIT_ATTEMPTS = SETTINGS.get('post_button_wait_attempts', 10)

# Load paths with defaults
PATHS = CONFIG.get('paths', {})
CHROMEDRIVER_PATH = PATHS.get('chromedriver_path', 'chrome/chromedriver.exe')
LOG_FILE = PATHS.get('log_file', 'logs/logs.log')
STATS_FILE = PATHS.get('stats_file', 'logs/comment_stats.json')
ERROR_LOG_FILE = PATHS.get('error_log_file', 'logs/errors.log')
COOKIES_DIR = PATHS.get('cookies_dir', 'cookies')

# === Helper Functions ===
def strip_non_bmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def today():
    return datetime.now().strftime("%Y-%m-%d")

def log_error_to_file(message):
    with open(ERROR_LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{datetime.now()}] {message}\n")

def save_links_for_account(stats, username, tag, url, comment):
    entry = stats.setdefault(username, {}).setdefault(today(), {})
    entry.setdefault("count", 0)
    entry.setdefault("hashtags", {})
    entry["hashtags"].setdefault(tag, [])
    entry["hashtags"][tag].append({"url": url, "comment": comment})

def is_duplicate_link(stats, username, url):
    account_stats = stats.get(username, {}).get(today(), {}).get("hashtags", {})
    for links in account_stats.values():
        for item in links:
            if item["url"] == url:
                return True
    return False

def save_cookies(driver, username):
    os.makedirs(COOKIES_DIR, exist_ok=True)
    with open(os.path.join(COOKIES_DIR, f"{username}.json"), 'w', encoding='utf-8') as f:
        json.dump(driver.get_cookies(), f)

def load_cookies(driver, username):
    path = os.path.join(COOKIES_DIR, f"{username}.json")
    if not os.path.exists(path):
        return False
    driver.get("https://www.instagram.com")
    with open(path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.get("https://www.instagram.com")
    return True

# === Instagram Bot Class ===
class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.visited = set()
        self.comments = self.load_comments()
        self.driver = self.start_browser()

    def log(self, msg):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        line = f"{timestamp} [{self.username}] {msg}"
        print(line)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    def load_comments(self):
        comments = CONFIG.get('comments', [])
        if not comments:
            print("[X] No comments found in config.json")
            exit()
        return [strip_non_bmp(comment) for comment in comments]

    def start_browser(self):
        options = Options()
        if HEADLESS_MODE:
            options.add_argument("--headless=new")
        
        # Force English language
        options.add_argument("--lang=en-US")
        options.add_argument("--accept-lang=en-US,en")
        options.add_experimental_option('prefs', {
            'intl.accept_languages': 'en,en_US'
        })
        
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        options.set_capability("pageLoadStrategy", "normal")

        try:
            driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                    window.navigator.chrome = { runtime: {} };
                    Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
                    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                """
            })
            return driver
        except WebDriverException as e:
            log_error_to_file(f"[X] Failed to start browser: {e}")
            exit()

    def login(self):
        cookies_loaded = False
        cookie_path = os.path.join(COOKIES_DIR, f"{self.username}.json")
        if os.path.exists(cookie_path):
            self.driver.get("https://www.instagram.com/")
            with open(cookie_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            self.driver.get("https://www.instagram.com/")
            cookies_loaded = True
            time.sleep(3)

        if cookies_loaded and "login" not in self.driver.current_url:
            self.log("✅ Session active, already logged in via cookies.")
            return

        self.log("🔐 Logging in manually...")
        self.driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(4)

        try:
            self.driver.find_element(By.NAME, 'username').send_keys(self.username)
            self.driver.find_element(By.NAME, 'password').send_keys(self.password + Keys.RETURN)
            time.sleep(LOGIN_DELAY)

            if "challenge" in self.driver.current_url:
                self.log("⚠️ Challenge or 2FA detected. Exiting...")
                self.driver.quit()
                exit()

            if "accounts/login" in self.driver.current_url:
                self.log("❌ Login failed. Check credentials.")
                self.driver.quit()
                exit()

            save_cookies(self.driver, self.username)
            self.log("✅ Logged in and cookies saved.")

        except Exception as e:
            self.log(f"Login exception: {e}")
            self.driver.quit()
            exit()


    def get_post_links(self, tag):
        try:
            self.driver.get(f'https://www.instagram.com/explore/tags/{tag[1:]}/')
            time.sleep(5)
            for _ in range(SCROLL_COUNT_FOR_POSTS):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_DELAY)
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            return list({l.get_attribute('href') for l in links if '/p/' in l.get_attribute('href')})
        except Exception as e:
            self.log(f"Failed to get post links for {tag}: {e}")
            return []

    def comment_on(self, url):
        if url in self.visited:
            return False
        try:
            self.driver.get(url)
            time.sleep(3)

            try:
                icon = self.driver.find_element(By.XPATH, "//svg[@aria-label='Comment']")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", icon)
                icon.click()
                time.sleep(2)
            except NoSuchElementException:
                self.log("No comment icon found. Possibly already open.")
            except Exception as e:
                self.log(f"Error clicking comment icon: {e}")

            comment_box = None
            for attempt in range(COMMENT_BOX_RETRIES):
                try:
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", comment_box)
                    self.driver.execute_script("arguments[0].focus();", comment_box)
                    comment_box.click()
                    time.sleep(1)
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@aria-label='Add a comment…']")
                    if comment_box.is_displayed() and comment_box.is_enabled():
                        break
                except StaleElementReferenceException as e:
                    self.log(f"[Try {attempt+1}/{COMMENT_BOX_RETRIES}] Stale element: retrying...")
                    time.sleep(1)
                except Exception as e:
                    self.log(f"[Try {attempt+1}/{COMMENT_BOX_RETRIES}] Failed to locate/focus comment box: {e}")
                    time.sleep(1)

            if not comment_box:
                self.log("❌ Unable to locate comment box after retries.")
                return False

            comment = strip_non_bmp(random.choice(self.comments))

            try:
                comment_box.send_keys(comment)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", comment_box)
            except Exception as e:
                self.log(f"❌ Error typing comment: {e}")
                return False

            time.sleep(1)

            for _ in range(POST_BUTTON_WAIT_ATTEMPTS):
                try:
                    post_btn = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Post']")
                    if post_btn.is_enabled():
                        post_btn.click()
                        break
                except Exception:
                    time.sleep(0.5)

            time.sleep(2)
            self.visited.add(url)
            self.log(f"✅ Commented on {url} with: {comment}")
            return url, comment

        except TimeoutException:
            self.log("⏱️ Timeout while waiting for comment box.")
            return False
        except Exception as e:
            self.log(f"❌ Failed at {url}: {e}")
            return False


    def close(self):
        self.driver.quit()

# === JSON Utilities ===
def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_stats(stats):
    with open(STATS_FILE, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)

def load_accounts():
    accounts = CONFIG.get('accounts', [])
    if not accounts:
        print("[X] No accounts found in config.json")
        exit()
    account_tuples = [(acc['username'], acc['password']) for acc in accounts]
    random.shuffle(account_tuples)
    return account_tuples

# === Main Execution Loop ===
if __name__ == "__main__":
    stats = load_stats()
    accounts = cycle(load_accounts())

    while True:
        username, password = next(accounts)
        used = stats.get(username, {}).get(today(), {}).get("count", 0)
        if used >= DAILY_LIMIT_PER_ACCOUNT:
            print(f"[~] {username} reached daily limit. Skipping...")
            time.sleep(2)
            continue

        limit_this_session = min(
            random.randint(COMMENTS_PER_SESSION_MIN, COMMENTS_PER_SESSION_MAX), 
            DAILY_LIMIT_PER_ACCOUNT - used
        )
        print(f"[>] Starting session for {username} (target: {limit_this_session} comments)")

        try:
            bot = InstagramBot(username, password)
            # load_cookies(bot.driver, username)
            bot.login()
            comments_done = 0

            for tag in random.sample(HASHTAGS, len(HASHTAGS)):
                links = bot.get_post_links(tag)
                random.shuffle(links)
                for link in links:
                    if comments_done >= limit_this_session:
                        break
                    if is_duplicate_link(stats, username, link):
                        continue
                    result = bot.comment_on(link)
                    if result:
                        url, comment = result
                        comments_done += 1
                        save_links_for_account(stats, username, tag, url, comment)
                        stats[username][today()]["count"] += 1
                        save_stats(stats)
                        delay = random.randint(DELAY_BETWEEN_COMMENTS_MIN, DELAY_BETWEEN_COMMENTS_MAX)
                        bot.log(f"Waiting {delay} sec...")
                        time.sleep(delay)

            bot.log(f"Finished session. Comments this session: {comments_done}.")
            bot.close()
        except Exception as e:
            print(f"[X] Fatal error with account {username}: {e}")
            log_error_to_file(f"{username}: {e}")
            continue

        time.sleep(DELAY_BETWEEN_SESSIONS)
