# Free Services Setup Guide

This guide shows you how to set up **free** data logging and alerting services for your prototype.

## Table of Contents
1. [ThingSpeak (Data Logging)](#thingspeak-data-logging)
2. [Discord Webhooks (Alerts)](#discord-webhooks-alerts)
3. [Telegram Bots (Alerts)](#telegram-bots-alerts)
4. [Gmail SMTP (Email Alerts)](#gmail-smtp-email-alerts)
5. [Configuration](#configuration)

---

## ThingSpeak (Data Logging)

**Free Tier:** 3 messages per 15 seconds, 8,200 messages/day, 4 million/year

### Setup Steps:

1. **Create Account**
   - Go to https://thingspeak.com
   - Click "Sign Up" (free)
   - Verify your email

2. **Create a Channel**
   - Click "New Channel"
   - Name: "Elderly Monitoring"
   - Check boxes for Field 1-5:
     - Field 1: Motion Detected (0 or 1)
     - Field 2: Motion Level (0.0 to 1.0)
     - Field 3: Person Detected (0 or 1)
     - Field 4: Person Confidence (0.0 to 1.0)
     - Field 5: Time Since Movement (minutes, -1 if unknown)
   - Click "Save Channel"

3. **Get Write API Key**
   - Go to "API Keys" tab
   - Copy the "Write API Key"
   - Keep this secret!

4. **Configure in config.yaml**
   ```yaml
   data_logging:
     thingspeak:
       enabled: true
       write_api_key: "YOUR_WRITE_API_KEY_HERE"
       channel_id: "YOUR_CHANNEL_ID"  # Optional, for reference
   ```

5. **View Your Data**
   - Go to "Private View" tab to see real-time charts
   - Data updates every 15 seconds (due to rate limit)

---

## Discord Webhooks (Alerts)

**Free:** Unlimited webhooks, perfect for prototypes!

### Setup Steps:

1. **Create Discord Server** (if you don't have one)
   - Open Discord
   - Click "+" to create a server
   - Name it "Elderly Monitoring Alerts"

2. **Create Webhook**
   - Go to Server Settings (right-click server name)
   - Click "Integrations" → "Webhooks"
   - Click "New Webhook"
   - Name: "Monitoring Alerts"
   - Choose a channel (or create one)
   - Click "Copy Webhook URL"
   - Click "Save Changes"

3. **Configure in config.yaml**
   ```yaml
   alerts:
     webhook:
       enabled: true
       type: "discord"
       webhook_urls:
         - "https://discord.com/api/webhooks/YOUR_WEBHOOK_URL_HERE"
       timeout: 5
       retry_attempts: 2
   ```

4. **Test**
   - Run your monitoring system
   - When an alert triggers, you'll see a formatted message in Discord!

---

## Telegram Bots (Alerts)

**Free:** Unlimited messages, great for mobile notifications!

### Setup Steps:

1. **Create Bot**
   - Open Telegram
   - Search for "@BotFather"
   - Send: `/newbot`
   - Follow prompts to name your bot
   - Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

2. **Get Chat ID**
   - Create a group or use a private chat
   - Add your bot to the group
   - Send a message in the group
   - Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
   - Find `"chat":{"id":123456789}` - that's your chat ID

3. **Configure in config.yaml**
   ```yaml
   alerts:
     webhook:
       enabled: true
       type: "telegram"
       webhook_urls:
         - "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_CHAT_ID>"
       timeout: 5
       retry_attempts: 2
   ```

   **Note:** Replace `<YOUR_TOKEN>` and `<YOUR_CHAT_ID>` with actual values.

4. **Test**
   - Send a test message to your bot
   - Alerts will appear in your Telegram chat!

---

## Gmail SMTP (Email Alerts)

**Free:** Gmail allows sending emails via SMTP (with app password)

### Setup Steps:

1. **Enable 2-Factor Authentication**
   - Go to https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Create App Password**
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "Raspberry Pi Monitoring"
   - Copy the 16-character password

3. **Configure in config.yaml**
   ```yaml
   alerts:
     email:
       enabled: true
       smtp_server: "smtp.gmail.com"
       smtp_port: 587
       use_tls: true
       from_email: "your.email@gmail.com"
       to_emails:
         - "social.worker1@example.com"
         - "social.worker2@example.com"
   ```

4. **Set Environment Variable**
   - Create `.env` file in `non_movement/` directory:
   ```
   EMAIL_PASSWORD=your_16_character_app_password
   ```

5. **Test**
   - Run your monitoring system
   - Alerts will be sent as emails!

---

## Configuration

### Complete Example config.yaml:

```yaml
# Data Logging
data_logging:
  thingspeak:
    enabled: true
    write_api_key: "YOUR_THINGSPEAK_WRITE_API_KEY"
    channel_id: "1234567"

# Alerts
alerts:
  # Email (Gmail)
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    use_tls: true
    from_email: "your.email@gmail.com"
    to_emails: ["worker@example.com"]
  
  # Webhook (Discord or Telegram)
  webhook:
    enabled: true
    type: "discord"  # or "telegram"
    webhook_urls:
      - "https://discord.com/api/webhooks/YOUR_URL"
    timeout: 5
    retry_attempts: 2
  
  # API (if you have custom endpoint)
  api:
    enabled: false
    endpoint: "http://localhost:5000/api/alerts"
```

### Environment Variables (.env file):

Create `non_movement/.env`:
```
EMAIL_PASSWORD=your_gmail_app_password
```

---

## Quick Start Recommendations

**For Prototype Demo:**

1. **ThingSpeak** - Best for data visualization
   - Shows charts of movement over time
   - Free and easy to set up
   - Great for demos!

2. **Discord Webhook** - Best for alerts
   - Instant notifications
   - Formatted messages with colors
   - Free and unlimited

**Combination:**
- Use **ThingSpeak** for continuous data logging
- Use **Discord** for immediate alerts
- Both are free and perfect for prototypes!

---

## Troubleshooting

### ThingSpeak
- **"Rate limit exceeded"**: You're sending too fast (max 3 per 15 seconds)
- **"Invalid API key"**: Check your Write API Key
- **No data showing**: Wait 15 seconds, data updates in batches

### Discord Webhook
- **"404 Not Found"**: Webhook URL is incorrect or deleted
- **"401 Unauthorized"**: Webhook was deleted, create a new one
- **No messages**: Check webhook URL and channel permissions

### Telegram
- **"Unauthorized"**: Bot token is wrong
- **"Chat not found"**: Chat ID is wrong, or bot not added to group
- **No messages**: Check token and chat ID

### Gmail
- **"Authentication failed"**: App password is wrong
- **"Connection refused"**: Check SMTP server and port
- **"Login failed"**: Use app password, not regular password

---

## Security Notes

⚠️ **Important:**
- Never commit API keys or passwords to git
- Use `.env` file for sensitive data (already in `.gitignore`)
- Keep webhook URLs private
- Rotate keys if exposed

---

## Next Steps

1. Choose your services (ThingSpeak + Discord recommended)
2. Follow setup steps above
3. Update `config.yaml` with your credentials
4. Test with your monitoring system
5. Demo ready! 🎉
