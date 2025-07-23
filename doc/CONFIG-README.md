# Configuration Guide

This document explains all the settings in your `config.json` file.

## Setup Instructions
1. Copy `config-example.json` to `config.json`
2. Edit `config.json` with your settings
3. Run the bot with `python main.py`

---

## Configuration Sections

### **accounts**
Add your Instagram login credentials here.
```json
"accounts": [
  { "username": "your_username", "password": "your_password" },
  { "username": "another_account", "password": "another_password" }
]
```
- **What it does**: The bot will cycle through these accounts
- **Important**: Use strong, unique passwords for security

---

### **comments**
Random comments the bot will post.
```json
"comments": [
  "Great post!",
  "Love this content ❤️",
  "🔥🔥🔥"
]
```
- **What it does**: Bot randomly selects one comment for each post
- **Tip**: Add variety to look more natural
- **Tip**: Use emojis to make comments engaging

---

### **hashtags**
Hashtags the bot will search for posts to comment on.
```json
"hashtags": [
  "#photography",
  "#travel",
  "#lifestyle"
]
```
- **What it does**: Bot finds posts under these hashtags
- **Tip**: Choose relevant hashtags for your niche
- **Tip**: Mix popular and niche hashtags

---

## Settings Section

### **Daily Limits**
- **`daily_limit_per_account`**: `200`
  - Maximum comments each account can make per day
  - Resets every day at midnight
  - Helps avoid Instagram rate limits

### **Session Control**
- **`comments_per_session_min`**: `2`
  - Minimum comments when an account logs in
  
- **`comments_per_session_max`**: `5`
  - Maximum comments when an account logs in
  - Bot picks random number between min and max

### **Timing & Delays**
- **`delay_between_comments_min`**: `420` (7 minutes)
  - Minimum wait time between each comment
  
- **`delay_between_comments_max`**: `480` (8 minutes)
  - Maximum wait time between each comment
  - Random delay helps avoid detection
  
- **`delay_between_sessions`**: `5`
  - Wait time before switching to next account (seconds)

- **`login_delay`**: `8`
  - Wait time after entering login credentials (seconds)
  - Gives Instagram time to process login

### **Browser Settings**
- **`headless_mode`**: `false`
  - `true`: Browser runs in background (invisible)
  - `false`: Browser window is visible
  - Set to `true` for servers, `false` for testing

### **Post Discovery**
- **`scroll_count_for_posts`**: `2`
  - How many times to scroll down on hashtag pages
  - More scrolls = more posts found = more variety
  
- **`scroll_delay`**: `3`
  - Wait time between each scroll (seconds)
  - Gives page time to load new posts

### **Error Handling**
- **`comment_box_retries`**: `5`
  - How many times to try finding the comment box
  - Higher number = more persistent but slower
  
- **`post_button_wait_attempts`**: `10`
  - How many times to try clicking the Post button
  - Sometimes Instagram is slow to enable the button

---

## Paths Section

### **`chromedriver_path`**: `"chrome/chromedriver.exe"`
- Path to your Chrome WebDriver executable
- Download from: https://chromedriver.chromium.org/
- Must match your Chrome browser version

### **Log Files**
- **`log_file`**: `"logs/logs.log"`
  - Where daily activity is recorded
  
- **`stats_file`**: `"logs/comment_stats.json"`
  - Where comment history and statistics are saved
  
- **`error_log_file`**: `"logs/errors.log"`
  - Where error messages are saved

### **`cookies_dir`**: `"cookies"`
- Where login cookies are saved
- Keeps accounts logged in between sessions
- Each account gets its own cookie file

---

## Safety Tips

### **Rate Limiting**
- Keep `daily_limit_per_account` under 300
- Use long delays between comments (7-8 minutes minimum)
- Don't run 24/7 - give accounts breaks

### **Natural Behavior**
- Use varied comments (at least 10-15 different ones)
- Mix hashtag targets
- Don't use the same pattern every day

### **Account Safety**
- Use accounts you don't mind losing
- Don't use your main Instagram account
- Enable 2FA on important accounts (bot will skip them)

### **Technical**
- Keep Chrome browser updated
- Update ChromeDriver when Chrome updates
- Monitor error logs for issues

---

## Common Issues

**"ChromeDriver not found"**
- Download ChromeDriver and put in `chrome/` folder
- Make sure version matches your Chrome browser

**"Login failed"**
- Check username/password spelling
- Account might have 2FA enabled
- Account might be temporarily blocked

**"No posts found"**
- Hashtags might be too specific
- Try more popular hashtags
- Check if hashtags still exist

**Bot runs too fast/slow**
- Adjust delay settings in `settings` section
- Increase delays if getting rate limited
- Decrease delays if bot is too slow

---

## Example Good Configuration

```json
{
  "settings": {
    "daily_limit_per_account": 150,
    "comments_per_session_min": 3,
    "comments_per_session_max": 7,
    "delay_between_comments_min": 360,
    "delay_between_comments_max": 600,
    "headless_mode": true
  }
}
```

This configuration:
- Limits each account to 150 comments per day (safe)
- Makes 3-7 comments per session (natural)
- Waits 6-10 minutes between comments (very safe)
- Runs in background (good for servers)