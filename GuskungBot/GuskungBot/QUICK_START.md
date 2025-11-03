# 🚀 Quick Start Guide

Quick start guide for Windows

### Option 1: Using BAT files (Easiest)

1. **First time setup:**
   ```cmd
   setup.bat
   ```

2. **Edit `.env` file:**
   - Open `.env` file
   - Add your `DISCORD_TOKEN=your_token_here`

3. **Run the bot:**
   ```cmd
   run.bat
   ```

### Option 2: Using Command Line

```cmd
pip install -r requirements.txt
# Edit .env file and add DISCORD_TOKEN
python main.py
```

## 🔧 Requirements

- **Python:** 3.8 or higher
- **Discord Bot Token:** Get from [Discord Developer Portal](https://discord.com/developers/applications)
- **Permissions:** Bot needs "Kick Members" permission for kick features

## 📝 Environment Variables

Create `.env` file:

```env
DISCORD_TOKEN=your_discord_bot_token_here
```

## ⚙️ Configuration

Edit `main.py` to customize:
- Command prefix
- Rate limiting settings
- Spam detection thresholds
- Auto-kick settings

## 🆘 Troubleshooting

### Python not found
- **Windows:** Install Python from [python.org](https://www.python.org/)

### Dependencies install fails
```cmd
# Upgrade pip first
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Bot doesn't connect
- Check if DISCORD_TOKEN is correct in `.env`
- Verify token hasn't expired
- Check bot has required intents in Discord Developer Portal

## 🌐 Platform Support

| Platform | Supported | Scripts |
|----------|-----------|---------|
| Windows | ✅ | `.bat` files |

## 📚 More Information

See `README.md` for detailed documentation.

