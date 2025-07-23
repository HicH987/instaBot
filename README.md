# 🤖 Instagram Automation Bot

A sophisticated Instagram commenting bot that operates across multiple accounts with intelligent rotation, rate limiting, and natural behavior patterns. Built with Python and Selenium for reliable automation.

---

## 🎯 Purpose & Vision

This project was developed as a tool for **digital advocacy** and awareness campaigns. It enables consistent, automated engagement across Instagram hashtags to amplify important messages and causes.

> �️ **Ethical Use Only**: This tool is designed for peaceful digital activism, not spam or commercial abuse. Use responsibly and respect Instagram's community guidelines.

---

## ✨ Key Features

### 🔄 **Smart Account Management**
- **Multi-account rotation** with infinite cycling
- **Session-based commenting** (2-5 comments per login)
- **Daily limits per account** (default: 200 comments)
- **Cookie-based login** to skip repeated authentication

### 🧠 **Intelligent Behavior**
- **Human-like timing** with 7-8 minute delays between comments
- **Duplicate prevention** - never comments on the same post twice
- **Random comment selection** from your custom list
- **Randomized hashtag targeting** for natural engagement patterns

### 📊 **Comprehensive Tracking**
- **Detailed logging** with timestamps and activity records
- **Comment statistics** tracking per account and date
- **Error monitoring** with automatic retry mechanisms
- **Link archiving** to prevent duplicate comments

### ⚙️ **Fully Configurable**
- **JSON-based configuration** - no code editing required
- **Customizable timing and limits** for different use cases
- **Flexible file paths** and directory structure
- **Headless mode** support for server deployment

---

## � Quick Start

### 1. **Setup Configuration**
```bash
# Copy the example configuration
cp config-example.json config.json

# Edit with your settings
nano config.json
```

### 2. **Install Dependencies**
```bash
pip install selenium
```

### 3. **Download ChromeDriver**
- Download from [ChromeDriver](https://chromedriver.chromium.org/)
- Place in `chrome/chromedriver.exe`
- Ensure version matches your Chrome browser

### 4. **Run the Bot**
```bash
python main.py
```

---

## 📋 Configuration Guide

### **Basic Structure**
```json
{
  "accounts": [
    {"username": "account1", "password": "password1"},
    {"username": "account2", "password": "password2"}
  ],
  "comments": [
    "Great post!",
    "Love this content ❤️",
    "Amazing work!"
  ],
  "hashtags": [
    "#photography",
    "#art",
    "#inspiration"
  ],
  "settings": { ... },
  "paths": { ... }
}
```

### **Key Settings**
| Setting | Default | Description |
|---------|---------|-------------|
| `daily_limit_per_account` | 200 | Max comments per account per day |
| `comments_per_session_min/max` | 2-5 | Comments per login session |
| `delay_between_comments_min/max` | 420-480s | Wait time between comments (7-8 min) |
| `headless_mode` | false | Run browser in background |

📖 **For detailed configuration help, see [doc/CONFIG-README.md](doc/CONFIG-README.md)**

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

### **Safety Features**
- **Rate Limiting**: Built-in delays prevent Instagram detection
- **Duplicate Prevention**: Never comments on same post twice
- **Error Recovery**: Automatic retries with backoff strategies
- **Cookie Management**: Reduces login frequency to avoid suspicion

---

## 📁 Project Structure

```
instaBot/
├── main.py                 # Main bot script
├── config.json             # Your configuration (create from example)
├── config-example.json     # Configuration template
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── chrome/
│   ├── chromedriver.exe   # ChromeDriver executable
│   └── ChromeSetup.exe    # Chrome browser installer
├── doc/
│   └── CONFIG-README.md   # Detailed configuration guide
├── logs/                  # Auto-created directory
│   ├── log.log           # Activity logs (gitignored)
│   └── comment_stats.json # Comment statistics (gitignored)
└── cookies/               # Auto-created directory (gitignored)
    └── account1.json      # Saved login cookies (auto-generated)
```

### **Important Notes:**
- 📁 **Auto-created folders**: `logs/` and `cookies/` are created automatically
- 🚫 **Gitignored files**: Log files, stats, and cookies are excluded from version control
- 📝 **config.json**: Create from `config-example.json` (also gitignored for security)

### **Git Ignore Protection**
The `.gitignore` file protects sensitive data by excluding:
- 🔒 **config.json** - Your account credentials
- 📁 **logs/** - All activity logs and statistics  
- 🍪 **cookies/** - Saved login sessions
- 🐍 **Python cache** - \_\_pycache\_\_ and .pyc files
- 💻 **IDE files** - .vscode, .idea folders
- 🌐 **Virtual environments** - venv/, .env/ folders

---

## 🛡️ Safety & Best Practices

### **Rate Limiting**
- ✅ Keep daily limits under 300 comments per account
- ✅ Use 7-8 minute delays between comments minimum
- ✅ Don't run 24/7 - give accounts regular breaks
- ✅ Start with lower limits and gradually increase

### **Account Safety**
- ⚠️ Use dedicated accounts, not your main Instagram
- ⚠️ Avoid accounts with 2FA enabled (bot will skip them)
- ⚠️ Monitor error logs for login issues or blocks
- ⚠️ Have backup accounts ready

### **Content Strategy**
- 📝 Use 10-15 varied, meaningful comments
- 📝 Mix hashtag targets regularly
- 📝 Avoid repetitive or spammy language
- 📝 Keep comments relevant to your cause

---

## � Monitoring & Troubleshooting

### **Log Files**
- **`logs/log.log`**: Real-time activity and session info
- **`logs/comment_stats.json`**: Detailed comment history and counts

### **Common Issues**

| Problem | Solution |
|---------|----------|
| "ChromeDriver not found" | Download ChromeDriver matching your Chrome version |
| "Login failed" | Check credentials, disable 2FA, or account may be blocked |
| "No posts found" | Try more popular hashtags or check hashtag validity |
| Bot too slow/fast | Adjust delay settings in config.json |

---

## ⚖️ Legal & Ethical Disclaimer

This tool interacts with Instagram and may violate their [Terms of Service](https://help.instagram.com/581066165581870).

### **Important Notes:**
- 🚫 **Not for spam or commercial promotion**
- 🚫 **Not for harassment or abuse**
- ✅ **Intended for peaceful digital activism only**
- ⚠️ **Use at your own risk** - accounts may be suspended
- 📋 **You are responsible** for how you use this tool

### **Recommended Use:**
- Humanitarian awareness campaigns
- Social cause advocacy
- Educational content promotion
- Community engagement for positive causes

---

## 🤝 Contributing

This project is designed for ethical digital activism. If you have improvements or bug fixes that enhance safety and reliability, contributions are welcome.

---

## 📞 Support

For configuration help, see [doc/CONFIG-README.md](doc/CONFIG-README.md)

**Remember**: This tool is most effective when used responsibly and in moderation. Quality engagement beats quantity every time.
