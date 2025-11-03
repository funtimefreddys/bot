# 🌐 Language Support Guide

GuskungBot supports **2 languages**: Thai (ไทย) and English

## 📝 Setting Default Language

### Method 1: Environment Variable (`.env`)

Add to your `.env` file:
```env
DISCORD_TOKEN=your_token_here
BOT_LANGUAGE=th    # or 'en' for English
```

### Method 2: Using Discord Command

Use the `/language` command in Discord:
```
/language lang:th    # Set to Thai
/language lang:en   # Set to English
```

**Note:** Requires `Manage Server` permission

## 🎯 Language Per Server

Each Discord server can have its own language setting:
- Server A: Thai
- Server B: English
- Server C: Thai

The language is set per server using `/language` command.

## 📋 Supported Languages

| Code | Language | Status |
|------|----------|--------|
| `th` | ไทย (Thai) | ✅ Full Support |
| `en` | English | ✅ Full Support |

## 🔧 Available Translations

All bot messages support both languages:
- ✅ Command responses
- ✅ Error messages
- ✅ Help messages
- ✅ Spam warnings
- ✅ Profile checks
- ✅ Auto-kick messages

## 💡 Usage Example

### Change Server Language

1. Open Discord
2. Go to your server
3. Type: `/language lang:en` (for English)
4. Or: `/language lang:th` (for Thai)

### Default Behavior

- If no language is set, bot uses language from `.env` file
- If `.env` doesn't specify, defaults to **Thai (th)**

## 🌍 Adding More Languages

To add more languages, edit `i18n.py`:

1. Add language code to `LANGUAGES` dictionary
2. Add all translation keys
3. The bot will automatically support it!

Example:
```python
LANGUAGES = {
    'th': {...},
    'en': {...},
    'ja': {...},  # Japanese (example)
}
```

## 📚 Current Translations

### Command Descriptions
- `/hello` - "ทักทายบอท / Greet the bot"
- `/ping` - "ตรวจสอบ latency / Check bot latency"
- `/language` - "Change bot language / เปลี่ยนภาษา"

### Common Messages
- Rate limit warnings
- Permission errors
- Spam detection warnings
- Profile check results
- Auto-kick notifications

## 🆘 Troubleshooting

### Language doesn't change
- Make sure you have `Manage Server` permission
- Use lowercase: `th` or `en` (not `TH` or `EN`)
- Restart the bot if needed

### Mixed languages
- Each server has its own language setting
- Different servers can have different languages

