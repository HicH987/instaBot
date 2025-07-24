Here's the **fully updated and cleaned-up `README.md`** with better structure, clearer guidance, reduced redundancy, and the **ChromeDriver download step removed**, since it's already included in the repo:

---

# 🤖 Instagram Automation Bot

Automate Instagram commenting across multiple accounts with human-like behavior, delays, and smart limits. Built with Python + Selenium.

---

## 🎯 Purpose

Designed for **digital activism** and **awareness campaigns** — not for spam or commercial use. Use responsibly and ethically.

---

## ✨ Features

### 🔄 Account Rotation

* Rotate unlimited accounts in a loop
* 2–5 comments per session, up to 200/day (default)
* Cookie-based login (fewer repeated logins)

### 🧠 Human-Like Behavior

* Delays of 7–8 minutes between comments
* Random comments and hashtags
* Never comments on the same post twice

### 📊 Tracking & Logs

* Logs with timestamps
* Comment statistics per account and per day
* Post archive to avoid repeats
* Retry system on errors

### ⚙️ Easy Configuration

* JSON-based config — no coding required
* Adjustable limits, delays, and file paths
* Headless mode supported (for servers)

---

## 🚀 Quick Start

1. **Set Up Configuration**

   ```bash
   cp config-example.json config.json
   nano config.json
   ```
   use the example (config-example.json) file to set your accounts, comments, hashtags, and settings.

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Bot**

   ```bash
   python main.py
   ```

---

## ⚙️ Config Overview

Example `config.json`:

```json
{
  "accounts": [
    {"username": "user1", "password": "pass1"}
  ],
  "comments": [
    "Great post!",
    "Amazing work!"
  ],
  "hashtags": [
    "#photography",
    "#art"
  ],
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
}
```

📘 Full config guide: [`doc/CONFIG-README.md`](doc/CONFIG-README.md)

---

## 🔧 How It Works

### **Account Rotation Cycle**
```
Account A → Login → 2-5 Comments → Logout
    ↓
Account B → Login → 3-4 Comments → Logout  
    ↓
Account C → Login → 2-5 Comments → Logout
    ↓ (cycles back to Account A)
```

### **Daily Flow**
1. **Load Configuration** and validate settings
2. **Create Infinite Account Cycle** from your account list
3. **For Each Account:**
   - Check daily comment limit (skip if reached)
   - Login using cookies or credentials
   - Find posts from random hashtags
   - Comment on 2-5 posts (session limit)
   - Wait 7-8 minutes between each comment
   - Logout and move to next account
4. **Repeat Forever** until manually stopped

---

## 🛡️ Safety Guidelines

### ✅ Best Practices

* Limit to \~300 comments/day/account
* Keep 7–8 min delay between comments
* Avoid running non-stop — allow rest breaks
* Start slow and increase gradually

### ⚠️ Account Tips

* Use alternate (not main) accounts
* Disable 2FA (bot will skip 2FA accounts)
* Monitor logs for errors or blocks
* Keep backups ready

### 📝 Comment Strategy

* Use 10–15 meaningful, varied comments
* Rotate hashtags frequently
* Avoid spammy or repetitive phrases

---

## 🧾 Logs & Troubleshooting

* `logs/log.log` — Activity log
* `logs/comment_stats.json` — Daily comment stats

| Problem            | Solution                                    |
| ------------------ | ------------------------------------------- |
| ChromeDriver error | Already included in repo — no action needed |
| Login failed       | Check credentials or disable 2FA            |
| No posts found     | Use more popular hashtags                   |
| Bot too fast/slow  | Adjust delay in config                      |

---

## 📁 Project Structure

```
instaBot/
├── chrome/
│   ├── chromedriver.exe    # ChromeDriver included
│   └── ChromeSetup.exe     # Chrome browser installer
├── doc/
│   └── CONFIG-README.md    # Full config guide
├── logs/                   # Logs (auto-generated)
├── cookies/                # Saved cookies (auto-generated)
├── main.py                 # Main bot script
├── config.json             # Your configuration
├── config-example.json     # Template config
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## ⚖️ Legal Disclaimer

This tool interacts with Instagram and **may violate their [Terms of Service](https://help.instagram.com/581066165581870)**.

### You must:

* 🚫 Not use it for spam, abuse, or promotion
* ✅ Use it only for ethical, peaceful campaigns
* ⚠️ Accept risk — account suspension is possible
* 📋 Be responsible for your usage

**Recommended Use:**

* Advocacy and awareness
* Nonprofit campaigns
* Community engagement for good causes

---

## 🤝 Contributing

Want to help? PRs that improve safety, reliability, or usability are welcome.

---

## 📞 Need Help?

See [`doc/CONFIG-README.md`](doc/CONFIG-README.md) for setup tips.

**Reminder:** This tool is most effective when used responsibly and in moderation.
