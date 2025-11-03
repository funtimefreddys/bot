# main.py
import os
import time
from datetime import datetime
from collections import defaultdict
from dotenv import load_dotenv
import discord
from discord import app_commands
from discord.ext import commands

# Import i18n support
from i18n import get_text, set_language, get_language, DEFAULT_LANGUAGE

# Import bad words filter
from bad_words import check_bad_words, add_bad_word, remove_bad_word, get_bad_words, BAD_WORDS_TH, BAD_WORDS_EN

# --- การจัดการความปลอดภัย (Security Management) ---

# 1. โหลดตัวแปรสภาพแวดล้อมจากไฟล์ .env (เพื่อโหลด DISCORD_TOKEN)
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # แก้ไข: ใช้ชื่อตัวแปรที่ถูกต้อง

# ตั้งค่าภาษาเริ่มต้นจาก .env
bot_lang = os.getenv('BOT_LANGUAGE', 'th').lower()
if bot_lang in ['th', 'en']:
    set_language(bot_lang)

# เก็บภาษาของแต่ละ guild (สามารถตั้งค่าได้ใน guild)
guild_languages = defaultdict(lambda: DEFAULT_LANGUAGE)  # {guild_id: 'th' or 'en'}
# เก็บภาษาของแต่ละ user (ผู้ใช้สามารถเลือกภาษาได้เอง)
user_languages = defaultdict(lambda: None)  # {user_id: 'th' or 'en' or None}

def get_guild_language(guild_id: int = None) -> str:
    """Get language for a guild"""
    if guild_id and guild_id in guild_languages:
        return guild_languages[guild_id]
    return DEFAULT_LANGUAGE

def get_user_language(user_id: int = None) -> str:
    """Get language for a user"""
    if user_id and user_id in user_languages and user_languages[user_id]:
        return user_languages[user_id]
    return None

def get_language_for_context(guild_id: int = None, user_id: int = None) -> str:
    """Get language - priority: user > guild > default"""
    # 1. Check user language first
    if user_id:
        user_lang = get_user_language(user_id)
        if user_lang:
            return user_lang
    
    # 2. Check guild language
    if guild_id:
        return get_guild_language(guild_id)
    
    # 3. Default language
    return DEFAULT_LANGUAGE

def t(key: str, guild_id: int = None, user_id: int = None, lang: str = None, **kwargs) -> str:
    """Get translated text for a guild/user context"""
    if lang is None:
        lang = get_language_for_context(guild_id, user_id)
    return get_text(key, lang, **kwargs)

# 2. กำหนด Intent ที่บอทต้องการ
# หมายเหตุ: message_content เป็น Privileged Intent 
# ถ้าไม่ได้เปิดใน Developer Portal บอทยังรันได้ แต่ bad words filter จะไม่ทำงาน
intents = discord.Intents.default()
# ลด intents ที่ไม่จำเป็นออก - ปิด members และ presences
# intents.members = False  # Privileged Intent - ไม่จำเป็น
# intents.presences = False  # Privileged Intent - ไม่จำเป็น

# message_content จำเป็นสำหรับ bad words filter และ spam detection
# ถ้าต้องการ bad words filter ให้เปิด MESSAGE CONTENT INTENT ใน Developer Portal
# ถ้าไม่ต้องการ bad words filter สามารถปิดได้โดยตั้ง ENABLE_MESSAGE_CONTENT=false ใน .env
MESSAGE_CONTENT_ENABLED = os.getenv('ENABLE_MESSAGE_CONTENT', 'true').lower() == 'true'
if MESSAGE_CONTENT_ENABLED:
    intents.message_content = True  # Privileged Intent - ต้องเปิดใน Developer Portal
else:
    print("ℹ️  INFO: Message Content Intent is disabled")
    print("   Bad words filter and spam detection will NOT work")
    print("   Bot commands will still work")
    intents.message_content = False

# 3. สร้าง Bot (ใช้ commands.Bot เพื่อรองรับทั้ง slash commands)
# commands.Bot มี tree attribute อยู่แล้ว ไม่ต้องสร้างใหม่
bot = commands.Bot(
    command_prefix='!',  # ยังรองรับ prefix commands (สำรอง)
    intents=intents,
    help_command=None
)

# --- ระบบ Rate Limiting (ป้องกัน Spam) ---
class RateLimiter:
    """ระบบจำกัดจำนวนคำสั่งต่อช่วงเวลา"""
    def __init__(self, max_calls: int = 5, time_window: int = 60):
        """
        max_calls: จำนวนคำสั่งสูงสุด
        time_window: ช่วงเวลาเป็นวินาที
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.user_calls = defaultdict(list)  # เก็บประวัติคำสั่งของแต่ละ user
    
    def is_allowed(self, user_id: int) -> bool:
        """ตรวจสอบว่าผู้ใช้สามารถใช้คำสั่งได้หรือไม่"""
        now = time.time()
        # ลบคำสั่งเก่าที่เกิน time_window
        self.user_calls[user_id] = [
            call_time for call_time in self.user_calls[user_id]
            if now - call_time < self.time_window
        ]
        
        # ตรวจสอบว่ามีคำสั่งเกิน limit หรือไม่
        if len(self.user_calls[user_id]) >= self.max_calls:
            return False
        
        # บันทึกคำสั่งใหม่
        self.user_calls[user_id].append(now)
        return True
    
    def get_remaining_time(self, user_id: int) -> int:
        """คืนเวลาที่เหลือก่อนจะสามารถใช้คำสั่งได้อีก"""
        if user_id not in self.user_calls or not self.user_calls[user_id]:
            return 0
        
        oldest_call = min(self.user_calls[user_id])
        remaining = self.time_window - (time.time() - oldest_call)
        return max(0, int(remaining))

# สร้าง Rate Limiter สำหรับคำสั่งทั่วไป
command_limiter = RateLimiter(max_calls=10, time_window=60)

# --- ระบบตรวจจับ Spam ที่ดีขึ้น ---
class SpamDetector:
    """ระบบตรวจจับ spam แบบหลายมิติ"""
    def __init__(self):
        self.message_history = defaultdict(list)  # เก็บประวัติข้อความของแต่ละ user
        self.user_message_times = defaultdict(list)  # เก็บเวลาของข้อความ
        
    def check_duplicate_messages(self, user_id: int, content: str, threshold: int = 3) -> bool:
        """ตรวจสอบว่ามีข้อความซ้ำกันหรือไม่"""
        user_messages = self.message_history[user_id]
        
        # ลบข้อความเก่าที่เกิน 10 นาที
        current_time = time.time()
        self.message_history[user_id] = [
            msg for msg in user_messages if current_time - msg['time'] < 600
        ]
        
        # ตรวจสอบข้อความซ้ำ
        duplicate_count = sum(1 for msg in self.message_history[user_id] if msg['content'] == content)
        
        # บันทึกข้อความใหม่
        self.message_history[user_id].append({
            'content': content,
            'time': current_time
        })
        
        return duplicate_count >= threshold
    
    def check_rapid_messages(self, user_id: int, max_messages: int = 5, time_window: int = 10) -> bool:
        """ตรวจสอบว่าส่งข้อความเร็วเกินไปหรือไม่"""
        current_time = time.time()
        
        # ลบข้อความเก่าที่เกิน time_window
        self.user_message_times[user_id] = [
            msg_time for msg_time in self.user_message_times[user_id]
            if current_time - msg_time < time_window
        ]
        
        # ตรวจสอบจำนวนข้อความ
        if len(self.user_message_times[user_id]) >= max_messages:
            return True
        
        # บันทึกเวลาข้อความใหม่
        self.user_message_times[user_id].append(current_time)
        return False
    
    def check_emoji_spam(self, content: str, threshold: int = 10) -> bool:
        """ตรวจสอบ emoji spam"""
        emoji_count = sum(1 for char in content if ord(char) > 127 and char in '😀😃😄😁😆😅😂🤣😊😍😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠😈👿👹👺🤡💩👻💀☠️👽👾🤖🎃😺😸😹😻😼😽🙀😿😾')
        return emoji_count >= threshold
    
    def check_character_spam(self, content: str, threshold: int = 10) -> bool:
        """ตรวจสอบ character spam (ตัวอักษรซ้ำต่อเนื่อง)"""
        if len(content) < threshold:
            return False
        
        max_repeat = 1
        current_char = ''
        current_count = 0
        
        for char in content:
            if char == current_char:
                current_count += 1
                max_repeat = max(max_repeat, current_count)
            else:
                current_char = char
                current_count = 1
        
        return max_repeat >= threshold
    
    def check_link_spam(self, content: str, threshold: int = 3) -> bool:
        """ตรวจสอบ link spam"""
        import re
        links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        return len(links) >= threshold
    
    def check_mention_spam(self, message, threshold: int = 5) -> bool:
        """ตรวจสอบ mention spam"""
        total_mentions = len(message.mentions) + len(message.role_mentions)
        return total_mentions >= threshold

# สร้าง Spam Detector
spam_detector = SpamDetector()

# --- ระบบตั้งค่าการเตะอัตโนมัติ ---
# เก็บสถานะการเตะอัตโนมัติของแต่ละเซิร์ฟเวอร์
auto_kick_settings = defaultdict(dict)  # {guild_id: {'enabled': bool, 'min_account_age': int, 'require_avatar': bool}}

# --- ระบบกรองคำหยาบคาย ---
# เก็บสถานะการกรองคำหยาบคายของแต่ละเซิร์ฟเวอร์
bad_words_settings = defaultdict(dict)  # {guild_id: {'enabled': bool, 'action': str, 'warn_channel_id': int}}

# --- ฟังก์ชันตรวจสอบโปรไฟล์ (Global) ---
def has_default_profile(member: discord.Member, guild_id: int = None, kick_mode: bool = False, lang: str = None) -> tuple[bool, list[str]]:
    """ตรวจสอบว่าผู้ใช้มีโปรไฟล์ default หรือไม่"""
    issues = []
    settings = auto_kick_settings.get(guild_id, {}) if guild_id else {}
    
    # ใช้ language ที่ระบุ หรือ default
    if lang is None:
        lang = get_guild_language(guild_id)
    
    # 1. ตรวจสอบ username ที่ดูเหมือน default
    username = member.name.lower()
    if len(username) < 3:
        issues.append(t('profile_issue_short_name', guild_id=guild_id, user_id=None, lang=lang))
    
    # 2. ตรวจสอบ avatar default (ใช้ค่า settings ถ้าเปิด)
    require_avatar = settings.get('require_avatar', True) if kick_mode else True
    if require_avatar and member.avatar is None:
        issues.append(t('profile_issue_no_avatar', guild_id=guild_id, user_id=None, lang=lang))
    
    # 3. ตรวจสอบ account age (ใช้ค่า settings ถ้าเปิด)
    account_age_days = (datetime.now() - member.created_at.replace(tzinfo=None)).days
    min_age = settings.get('min_account_age', 7) if kick_mode else 7
    if account_age_days < min_age:
        issues.append(t('profile_issue_new_account', guild_id=guild_id, user_id=None, lang=lang, days=account_age_days))
    
    # 4. ตรวจสอบว่ามี roles หรือไม่ (อาจเป็น bot หรือ alt account)
    if isinstance(member, discord.Member) and len(member.roles) <= 1:  # มีแค่ @everyone
        issues.append(t('profile_issue_no_roles', guild_id=guild_id, user_id=None, lang=lang))
    
    return len(issues) > 0, issues

# --- ระบบ Input Validation ---
def sanitize_input(text: str, max_length: int = 2000) -> str:
    """ทำความสะอาดข้อความก่อนประมวลผล"""
    if not text:
        return ""
    
    # ตัดข้อความที่ยาวเกินไป
    text = text[:max_length]
    
    # ลบอักขระพิเศษที่อาจเป็นอันตราย (ปรับแต่งตามความต้องการ)
    # ในที่นี้เราจะเก็บอักขระพื้นฐานไว้ก่อน
    
    return text.strip()

def validate_command(command: str) -> bool:
    """ตรวจสอบความถูกต้องของคำสั่ง"""
    # ตรวจสอบว่าคำสั่งไม่ว่างเปล่า
    if not command or len(command) < 1:
        return False
    
    # ตรวจสอบความยาวคำสั่ง
    if len(command) > 100:
        return False
    
    # ตรวจสอบว่าคำสั่งมีอักขระแปลก ๆ หรือไม่
    # (เพิ่มเติมตามความต้องการ)
    
    return True

# --- ระบบ Permission Checks ---
def has_permission(member: discord.Member, permission: str = "administrator") -> bool:
    """ตรวจสอบว่าผู้ใช้มีสิทธิ์หรือไม่"""
    if not member:
        return False
    
    # ตรวจสอบสิทธิ์ตามชื่อ
    if permission == "administrator":
        return member.guild_permissions.administrator
    elif permission == "manage_messages":
        return member.guild_permissions.manage_messages
    elif permission == "ban_members":
        return member.guild_permissions.ban_members
    elif permission == "kick_members":
        return member.guild_permissions.kick_members
    
    return False

# --- ระบบ Logging ---
def log_action(action: str, user: discord.User = None, details: str = ""):
    """บันทึกการกระทำที่สำคัญ"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] {action}"
    
    if user:
        log_message += f" | User: {user.name}#{user.discriminator} ({user.id})"
    
    if details:
        log_message += f" | {details}"
    
    print(log_message)

# --- Event Handlers ---
@bot.event
async def on_ready():
    """Bot ready event - runs when bot connects to Discord"""
    print('=' * 50)
    print(f'🤖 Bot connected successfully!')
    print(f'Name: {bot.user.name}#{bot.user.discriminator}')
    print(f'ID: {bot.user.id}')
    print(f'Connected to {len(bot.guilds)} server(s)')
    if len(bot.guilds) > 0:
        print(f'\n📋 Connected servers:')
        for guild in bot.guilds:
            print(f'   - {guild.name} (ID: {guild.id})')
    print('=' * 50)
    
    # Sync Slash Commands
    print('🔄 Syncing slash commands...')
    
    # Sync commands both global and guild-specific
    synced_global = []
    synced_guilds = {}
    
    try:
        # Sync global commands (takes longer, up to 1 hour to appear)
        print('   📡 Syncing global commands...')
        synced_global = await bot.tree.sync()
        print(f'   ✅ Global commands: {len(synced_global)} commands')
        
        # Sync guild-specific commands (faster - takes about 1-5 minutes)
        if len(bot.guilds) > 0:
            print(f'   📡 Syncing guild commands ({len(bot.guilds)} server(s))...')
            for guild in bot.guilds:
                try:
                    bot.tree.copy_global_to(guild=guild)
                    synced_guild = await bot.tree.sync(guild=guild)
                    synced_guilds[guild.name] = len(synced_guild)
                    print(f'      ✅ {guild.name}: {len(synced_guild)} commands')
                except Exception as e:
                    print(f'      ⚠️ {guild.name}: Error occurred - {e}')
                    synced_guilds[guild.name] = 0
        else:
            print('   ⚠️ Bot is not in any servers yet')
            
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')
        import traceback
        traceback.print_exc()
    
    print('=' * 50)
    total_commands = len(synced_global)
    print(f'✅ Slash commands synced successfully!')
    print(f'   Global commands: {total_commands} commands')
    if synced_guilds:
        total_guild_commands = sum(synced_guilds.values())
        print(f'   Guild commands: {total_guild_commands} commands')
    
    print('\n💡 Notes:')
    print('   - Guild commands will appear in Discord within 1-5 minutes')
    print('   - Global commands may take up to 1 hour')
    print('   - Try typing / in Discord to see commands')
    print('   - If not visible, try reloading Discord (Ctrl+R)')
    print('=' * 50)
    
    log_action("Bot started", bot.user)

# Error handler สำหรับ Slash Commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """จัดการกับ Error ที่เกิดขึ้นจาก Slash Commands"""
    guild_id = interaction.guild.id if interaction.guild else None
    user_id = interaction.user.id if interaction.user else None
    
    if isinstance(error, app_commands.CommandOnCooldown):
        remaining = error.retry_after
        await interaction.response.send_message(
            t('rate_limit_cooldown', guild_id=guild_id, user_id=user_id, seconds=int(remaining)),
            ephemeral=True
        )
        log_action("Rate limit hit", interaction.user, f"Command: {interaction.command.name}")
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message(
            t('permission_denied', guild_id=guild_id, user_id=user_id),
            ephemeral=True
        )
        log_action("Permission denied", interaction.user, f"Command: {interaction.command.name}")
    else:
        # Log error อื่น ๆ
        log_action("Error occurred", interaction.user if interaction.user else None, f"Error: {str(error)}")
        try:
            await interaction.response.send_message(
                t('command_error', guild_id=guild_id, user_id=user_id),
                ephemeral=True
            )
        except:
            # ถ้า interaction.response ถูกใช้ไปแล้ว
            await interaction.followup.send(
                t('command_error', guild_id=guild_id, user_id=user_id),
                ephemeral=True
            )

# --- Slash Commands ---
@bot.tree.command(name="hello", description="ทักทายบอท / Greet the bot")
@app_commands.describe(name="ชื่อของคุณ / Your name (optional)")
async def hello_command(interaction: discord.Interaction, name: str = None):
    """คำสั่งทักทายแบบ Slash Command"""
    guild_id = interaction.guild.id if interaction.guild else None
    
    # ตรวจสอบ Rate Limit
    if not command_limiter.is_allowed(interaction.user.id):
        remaining = command_limiter.get_remaining_time(interaction.user.id)
        await interaction.response.send_message(
            t('rate_limit', guild_id, seconds=remaining),
            ephemeral=True
        )
        return
    
    # สร้าง response
    if name:
        response = sanitize_input(t('hello_response', guild_id, name=name, mention=interaction.user.mention))
    else:
        response = sanitize_input(t('hello_response_no_name', guild_id, mention=interaction.user.mention))
    
    await interaction.response.send_message(response)
    log_action("Command executed", interaction.user, "hello")

@bot.tree.command(name="ping", description="ตรวจสอบ latency / Check bot latency")
async def ping_command(interaction: discord.Interaction):
    """ตรวจสอบ latency ของบอท"""
    guild_id = interaction.guild.id if interaction.guild else None
    
    if not command_limiter.is_allowed(interaction.user.id):
        remaining = command_limiter.get_remaining_time(interaction.user.id)
        await interaction.response.send_message(
            t('rate_limit', guild_id, seconds=remaining),
            ephemeral=True
        )
        return
    
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(t('ping_response', guild_id, latency=latency))
    log_action("Command executed", interaction.user, "ping")

@bot.tree.command(name="clear", description="ลบข้อความ (ต้องมีสิทธิ์จัดการข้อความ)")
@app_commands.describe(amount="จำนวนข้อความที่ต้องการลบ (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear_command(interaction: discord.Interaction, amount: int = 5):
    """ลบข้อความ (ต้องมีสิทธิ์ manage_messages)"""
    guild_id = interaction.guild.id if interaction.guild else None
    user_id = interaction.user.id
    
    # ตรวจสอบจำนวนที่ต้องการลบ
    if amount < 1 or amount > 100:
        await interaction.response.send_message(
            t('clear_amount', guild_id=guild_id, user_id=user_id),
            ephemeral=True
        )
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        # ลบข้อความ
        deleted = await interaction.channel.purge(limit=amount)
        await interaction.followup.send(
            t('clear_success', guild_id=guild_id, user_id=user_id, count=len(deleted)),
            ephemeral=True
        )
        log_action("Messages cleared", interaction.user, f"Amount: {amount}")
    except discord.Forbidden:
        await interaction.followup.send(
            t('clear_permission', guild_id=guild_id, user_id=user_id),
            ephemeral=True
        )
        log_action("Permission error", interaction.user, "clear command")
    except Exception as e:
        await interaction.followup.send(
            t('clear_error', guild_id=guild_id, user_id=user_id),
            ephemeral=True
        )
        log_action("Error", interaction.user, f"clear: {str(e)}")

@bot.tree.command(name="sync", description="Sync slash commands อีกครั้ง (สำหรับผู้ดูแลระบบ)")
@app_commands.describe(force="Force sync (ลบคำสั่งเก่าก่อน sync)")
@app_commands.checks.has_permissions(administrator=True)
async def sync_command(interaction: discord.Interaction, force: bool = False):
    """Sync slash commands อีกครั้ง"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild = interaction.guild
        synced = []
        
        if force:
            # ลบคำสั่งเก่าก่อน
            bot.tree.clear_commands(guild=guild)
            await interaction.followup.send("🗑️ ลบคำสั่งเก่าแล้ว กำลัง sync ใหม่...", ephemeral=True)
        
        # Copy global commands ไปยัง guild
        if guild:
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
        else:
            synced = await bot.tree.sync()
        
        await interaction.followup.send(
            f"✅ Sync commands สำเร็จ! ({len(synced)} คำสั่ง)\n"
            f"คำสั่งจะปรากฏใน Discord ภายใน 1-5 นาที",
            ephemeral=True
        )
        log_action("Commands synced", interaction.user, f"Guild: {guild.name if guild else 'Global'}, Force: {force}")
        
    except Exception as e:
        await interaction.followup.send(
            f"❌ เกิดข้อผิดพลาด: {str(e)}",
            ephemeral=True
        )
        log_action("Sync error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="autokick", description="ตั้งค่าระบบเตะอัตโนมัติ (สำหรับผู้ดูแลระบบ)")
@app_commands.describe(
    enabled="เปิด/ปิดการเตะอัตโนมัติ",
    min_account_age="อายุบัญชีขั้นต่ำ (วัน)",
    require_avatar="ต้องมี avatar หรือไม่",
    log_channel="Channel สำหรับ log (ไม่ระบุ = ปิด)"
)
@app_commands.checks.has_permissions(administrator=True)
async def autokick_command(
    interaction: discord.Interaction,
    enabled: bool = None,
    min_account_age: int = 7,
    require_avatar: bool = True,
    log_channel: discord.TextChannel = None
):
    """ตั้งค่าระบบเตะอัตโนมัติ"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild = interaction.guild
        guild_id = guild.id if guild else None
        user_id = interaction.user.id
        if not guild:
            await interaction.followup.send(t('command_server_only', guild_id=guild_id, user_id=user_id), ephemeral=True)
            return
        
        # ตั้งค่า
        if guild.id not in auto_kick_settings:
            auto_kick_settings[guild.id] = {
                'enabled': False,
                'min_account_age': 7,
                'require_avatar': True,
                'log_channel_id': None
            }
        
        settings = auto_kick_settings[guild.id]
        
        # อัพเดทค่าตามที่ระบุ
        if enabled is not None:
            settings['enabled'] = enabled
        if min_account_age > 0:
            settings['min_account_age'] = min_account_age
        if require_avatar is not None:
            settings['require_avatar'] = require_avatar
        if log_channel:
            settings['log_channel_id'] = log_channel.id
        elif log_channel is None and enabled is False:
            # ถ้าปิดการเตะอัตโนมัติ ไม่ต้องตั้ง log channel
            pass
        
        # สร้าง embed แสดงสถานะ
        embed = discord.Embed(
            title="⚙️ ตั้งค่าระบบเตะอัตโนมัติ",
            color=discord.Color.green() if settings['enabled'] else discord.Color.red()
        )
        embed.add_field(
            name="สถานะ",
            value="✅ เปิดใช้งาน" if settings['enabled'] else "❌ ปิดใช้งาน",
            inline=False
        )
        embed.add_field(
            name="ตั้งค่า",
            value=f"**อายุบัญชีขั้นต่ำ:** {settings['min_account_age']} วัน\n"
                  f"**ต้องมี avatar:** {'ใช่' if settings['require_avatar'] else 'ไม่ใช่'}",
            inline=False
        )
        if settings.get('log_channel_id'):
            channel = guild.get_channel(settings['log_channel_id'])
            if channel:
                embed.add_field(
                    name="Log Channel",
                    value=channel.mention,
                    inline=False
                )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        log_action("Auto-kick settings updated", interaction.user, f"Guild: {guild.name}, Enabled: {settings['enabled']}")
    
    except Exception as e:
        await interaction.followup.send(
            f"❌ เกิดข้อผิดพลาด: {str(e)}",
            ephemeral=True
        )
        log_action("Auto-kick settings error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="kickprofile", description="เตะผู้ใช้ที่ไม่ตั้งโปรไฟล์ทันที (สำหรับผู้ดูแลระบบ)")
@app_commands.describe(user="ผู้ใช้ที่ต้องการเตะ")
@app_commands.checks.has_permissions(administrator=True)
async def kick_profile_command(interaction: discord.Interaction, user: discord.Member):
    """เตะผู้ใช้ที่ไม่ตั้งโปรไฟล์ทันที"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild = interaction.guild
        guild_id = guild.id if guild else None
        user_id = interaction.user.id
        if not guild:
            await interaction.followup.send(t('command_server_only', guild_id=guild_id, user_id=user_id), ephemeral=True)
            return
        
        guild_id = guild.id
        user_id = interaction.user.id
        lang = get_language_for_context(guild_id, user_id)
        
        # ตรวจสอบว่าผู้ใช้เป็น bot หรือไม่
        if user.bot:
            await interaction.followup.send(t('kick_cannot_bot', guild_id=guild_id, user_id=user_id, lang=lang), ephemeral=True)
            return
        
        # ตรวจสอบว่าผู้ใช้เป็นเจ้าของเซิร์ฟเวอร์หรือไม่
        if user == guild.owner:
            await interaction.followup.send(t('kick_cannot_owner', guild_id=guild_id, user_id=user_id, lang=lang), ephemeral=True)
            return
        
        # ตรวจสอบว่าเป็น admin หรือไม่
        if user.guild_permissions.administrator:
            await interaction.followup.send(t('kick_cannot_admin', guild_id=guild_id, user_id=user_id, lang=lang), ephemeral=True)
            return
        
        # ตรวจสอบโปรไฟล์
        guild_id = guild.id
        user_id = user.id
        lang = get_language_for_context(guild_id, user_id)
        has_issues, issues = has_default_profile(user, guild_id, kick_mode=False, lang=lang)
        
        if has_issues:
            # ลองส่งข้อความเตือนใน DMs
            try:
                # ใช้ภาษาของผู้ใช้ที่ถูกเตะ
                user_lang = get_language_for_context(guild_id, user_id)
                dm_embed = discord.Embed(
                    title=t('kick_dm_title', guild_id=guild_id, user_id=user_id, lang=user_lang),
                    description=f"{t('kick_dm_server', guild_id=guild_id, user_id=user_id, lang=user_lang)}: **{guild.name}**",
                    color=discord.Color.red()
                )
                dm_embed.add_field(
                    name=t('kick_dm_reason', guild_id=guild_id, user_id=user_id, lang=user_lang),
                    value="\n".join(f"• {issue}" for issue in issues),
                    inline=False
                )
                suggestions_value = f"• {t('kick_suggestion_avatar', guild_id=guild_id, user_id=user_id, lang=user_lang)}\n"
                suggestions_value += f"• {t('kick_suggestion_age', guild_id=guild_id, user_id=user_id, lang=user_lang)}\n"
                suggestions_value += f"• {t('kick_suggestion_name', guild_id=guild_id, user_id=user_id, lang=user_lang)}"
                dm_embed.add_field(
                    name=t('kick_dm_suggestions', guild_id=guild_id, user_id=user_id, lang=user_lang),
                    value=suggestions_value,
                    inline=False
                )
                await user.send(embed=dm_embed)
            except:
                pass
            
            # เตะผู้ใช้ออก
            kick_reason = t('kick_reason_prefix', guild_id=guild_id, user_id=user_id, lang=lang, user=interaction.user.name, reasons=', '.join(issues[:3]))
            await user.kick(reason=kick_reason)
            
            embed = discord.Embed(
                title=t('kick_success', guild_id=guild_id, user_id=interaction.user.id, lang=lang),
                description=f"User: {user.mention} ({user.name})",
                color=discord.Color.red()
            )
            embed.add_field(
                name=t('kick_dm_reason', guild_id=guild_id, user_id=interaction.user.id, lang=lang),
                value="\n".join(f"• {issue}" for issue in issues),
                inline=False
            )
            embed.set_footer(text=f"By {interaction.user.name}")
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            log_action("Manual kick", interaction.user, f"Kicked: {user.name}, Issues: {', '.join(issues)}")
        else:
            await interaction.followup.send(
                t('kick_profile_normal', guild_id=guild_id, user_id=interaction.user.id, lang=lang, mention=user.mention),
                ephemeral=True
            )
    
    except discord.Forbidden:
        guild_id = interaction.guild.id if interaction.guild else None
        user_id = interaction.user.id
        await interaction.followup.send(
            t('kick_permission', guild_id=guild_id, user_id=user_id),
            ephemeral=True
        )
        log_action("Kick permission error", interaction.user, f"User: {user.name}")
    except Exception as e:
        guild_id = interaction.guild.id if interaction.guild else None
        user_id = interaction.user.id
        await interaction.followup.send(
            t('error_occurred', guild_id=guild_id, user_id=user_id, error=str(e)),
            ephemeral=True
        )
        log_action("Kick error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="checkprofile", description="ตรวจสอบผู้ใช้ที่ไม่ตั้งโปรไฟล์ (สำหรับผู้ดูแลระบบ)")
@app_commands.describe(user="ผู้ใช้ที่ต้องการตรวจสอบ (ไม่ระบุ = ตรวจสอบทั้งหมด)")
@app_commands.checks.has_permissions(manage_guild=True)
async def check_profile_command(interaction: discord.Interaction, user: discord.Member = None):
    """ตรวจสอบผู้ใช้ที่ไม่ตั้งโปรไฟล์"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild = interaction.guild
        guild_id = guild.id if guild else None
        user_id = interaction.user.id
        if not guild:
            await interaction.followup.send(t('command_server_only', guild_id=guild_id, user_id=user_id), ephemeral=True)
            return
        
        # ตรวจสอบผู้ใช้
        if user:
            # ตรวจสอบผู้ใช้คนเดียว
            has_issues, issues = has_default_profile(user, guild.id, kick_mode=False)
            
            if has_issues:
                embed = discord.Embed(
                    title=f"⚠️ ตรวจพบปัญหาโปรไฟล์",
                    description=f"ผู้ใช้: {user.mention}",
                    color=discord.Color.orange()
                )
                embed.add_field(
                    name="ปัญหา",
                    value="\n".join(f"• {issue}" for issue in issues),
                    inline=False
                )
                embed.add_field(
                    name="ข้อมูล",
                    value=f"**ชื่อ:** {user.name}\n**ID:** {user.id}\n**สร้างเมื่อ:** {user.created_at.strftime('%Y-%m-%d')}",
                    inline=False
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(
                    f"✅ {user.mention} มีโปรไฟล์ปกติ",
                    ephemeral=True
                )
            
            log_action("Profile checked", interaction.user, f"User: {user.name}, Issues: {len(issues)}")
        else:
            # ตรวจสอบทั้งหมด
            members_with_issues = []
            
            for member in guild.members:
                if member.bot:
                    continue
                
                has_issues, issues = has_default_profile(member, guild.id, kick_mode=False)
                if has_issues:
                    members_with_issues.append((member, issues))
            
            if members_with_issues:
                # สร้าง embed แสดงผล
                embed = discord.Embed(
                    title=f"📋 รายงานผู้ใช้ที่ไม่ตั้งโปรไฟล์",
                    description=f"พบ {len(members_with_issues)} คน",
                    color=discord.Color.red()
                )
                
                # แสดง 10 คนแรก
                for i, (member, issues) in enumerate(members_with_issues[:10], 1):
                    issues_text = ", ".join(issues[:3])  # แสดง 3 ปัญหาหลัก
                    embed.add_field(
                        name=f"{i}. {member.name}",
                        value=f"{member.mention}\n**ปัญหา:** {issues_text}",
                        inline=False
                    )
                
                if len(members_with_issues) > 10:
                    embed.set_footer(text=f"แสดง 10 คนแรกจากทั้งหมด {len(members_with_issues)} คน")
                
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(
                    "✅ ไม่พบผู้ใช้ที่มีปัญหาโปรไฟล์",
                    ephemeral=True
                )
            
            log_action("All profiles checked", interaction.user, f"Found: {len(members_with_issues)} issues")
    
    except Exception as e:
        await interaction.followup.send(
            f"❌ เกิดข้อผิดพลาด: {str(e)}",
            ephemeral=True
        )
        log_action("Profile check error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="language", description="Change bot language / เปลี่ยนภาษา")
@app_commands.describe(
    lang="Language: th (Thai) or en (English)",
    scope="Scope: server (requires Manage Server) or user (personal)"
)
async def language_command(interaction: discord.Interaction, lang: str, scope: str = "user"):
    """Change bot language for server or user"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    lang = lang.lower()
    if lang not in ['th', 'en']:
        await interaction.followup.send(
            "❌ Invalid language! Use 'th' for Thai or 'en' for English\n"
            "❌ ภาษาไม่ถูกต้อง! ใช้ 'th' สำหรับไทย หรือ 'en' สำหรับอังกฤษ",
            ephemeral=True
        )
        return
    
    scope = scope.lower()
    lang_name = "ไทย" if lang == 'th' else "English"
    
    if scope == "server":
        # Change server language (requires Manage Server permission)
        guild = interaction.guild
        if not guild:
            await interaction.followup.send(
                "❌ This command can only be used in a server",
                ephemeral=True
            )
            return
        
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.followup.send(
                "❌ You need 'Manage Server' permission to change server language!\n"
                "❌ คุณต้องมีสิทธิ์ 'จัดการเซิร์ฟเวอร์' เพื่อเปลี่ยนภาษาของเซิร์ฟเวอร์!",
                ephemeral=True
            )
            return
        
        guild_languages[guild.id] = lang
        await interaction.followup.send(
            f"✅ Server language changed to {lang_name} / เปลี่ยนภาษาของเซิร์ฟเวอร์เป็น {lang_name} แล้ว!\n"
            f"🌐 All users in this server will see {lang_name} by default",
            ephemeral=True
        )
        log_action("Server language changed", interaction.user, f"Guild: {guild.name}, Language: {lang}")
    
    elif scope == "user":
        # Change user's personal language
        user_languages[interaction.user.id] = lang
        await interaction.followup.send(
            f"✅ Your personal language changed to {lang_name} / เปลี่ยนภาษาส่วนตัวของคุณเป็น {lang_name} แล้ว!\n"
            f"🌐 You will see bot messages in {lang_name} (unless server has different language)",
            ephemeral=True
        )
        log_action("User language changed", interaction.user, f"Language: {lang}")
    
    else:
        await interaction.followup.send(
            "❌ Invalid scope! Use 'server' or 'user'\n"
            "❌ ขอบเขตไม่ถูกต้อง! ใช้ 'server' หรือ 'user'",
            ephemeral=True
        )

@bot.tree.command(name="badwords", description="จัดการระบบกรองคำหยาบคาย / Manage bad words filter")
@app_commands.describe(
    enabled="เปิด/ปิดการกรองคำหยาบคาย / Enable/disable bad words filter",
    action="การดำเนินการเมื่อพบคำหยาบคาย (delete/warn) / Action when bad words found",
    add_word="เพิ่มคำหยาบคาย / Add bad word",
    remove_word="ลบคำหยาบคาย / Remove bad word",
    list_words="แสดงรายการคำหยาบคาย / Show bad words list",
    language="ภาษาที่ต้องการจัดการ (th/en) / Language to manage (th/en)"
)
@app_commands.checks.has_permissions(manage_guild=True)
async def badwords_command(
    interaction: discord.Interaction,
    enabled: bool = None,
    action: str = None,
    add_word: str = None,
    remove_word: str = None,
    list_words: bool = False,
    language: str = "en"
):
    """จัดการระบบกรองคำหยาบคาย"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild = interaction.guild
        if not guild:
            await interaction.followup.send(
                t('command_server_only', guild_id=None, user_id=interaction.user.id),
                ephemeral=True
            )
            return
        
        guild_id = guild.id
        user_id = interaction.user.id
        lang = get_language_for_context(guild_id, user_id)
        
        # Initialize settings
        if guild_id not in bad_words_settings:
            bad_words_settings[guild_id] = {
                'enabled': False,
                'action': 'delete',
                'warn_channel_id': None
            }
        
        settings = bad_words_settings[guild_id]
        
        # Handle different actions
        if add_word:
            # Add bad word
            word_lang = language.lower() if language else lang
            if add_bad_word(add_word, word_lang):
                await interaction.followup.send(
                    t('badwords_added', guild_id=guild_id, user_id=user_id, lang=lang, word=add_word),
                    ephemeral=True
                )
                log_action("Bad word added", interaction.user, f"Word: {add_word}, Language: {word_lang}")
            else:
                await interaction.followup.send(
                    t('badwords_already_exists', guild_id=guild_id, user_id=user_id, lang=lang),
                    ephemeral=True
                )
            return
        
        if remove_word:
            # Remove bad word
            word_lang = language.lower() if language else lang
            if remove_bad_word(remove_word, word_lang):
                await interaction.followup.send(
                    t('badwords_removed', guild_id=guild_id, user_id=user_id, lang=lang, word=remove_word),
                    ephemeral=True
                )
                log_action("Bad word removed", interaction.user, f"Word: {remove_word}, Language: {word_lang}")
            else:
                await interaction.followup.send(
                    t('badwords_not_found', guild_id=guild_id, user_id=user_id, lang=lang),
                    ephemeral=True
                )
            return
        
        if list_words:
            # List bad words
            word_lang = language.lower() if language else lang
            bad_words_list = get_bad_words(word_lang)
            
            embed = discord.Embed(
                title=t('badwords_list', guild_id=guild_id, user_id=user_id, lang=lang, count=len(bad_words_list)),
                color=discord.Color.orange()
            )
            
            if bad_words_list:
                # Show first 20 words
                words_text = ', '.join(bad_words_list[:20])
                if len(bad_words_list) > 20:
                    words_text += f" ... (+{len(bad_words_list) - 20} more)"
                embed.description = words_text
            else:
                embed.description = t('badwords_check_clean', guild_id=guild_id, user_id=user_id, lang=lang)
            
            embed.add_field(
                name=t('badwords_action', guild_id=guild_id, user_id=user_id, lang=lang),
                value=f"Language: {word_lang.upper()}",
                inline=False
            )
            
            await interaction.followup.send(embed=embed, ephemeral=True)
            return
        
        # Update settings
        if enabled is not None:
            settings['enabled'] = enabled
        
        if action:
            action = action.lower()
            if action in ['delete', 'warn']:
                settings['action'] = action
        
        # Create embed showing current settings
        embed = discord.Embed(
            title=t('badwords_title', guild_id=guild_id, user_id=user_id, lang=lang),
            color=discord.Color.green() if settings['enabled'] else discord.Color.red()
        )
        
        embed.add_field(
            name=t('badwords_status', guild_id=guild_id, user_id=user_id, lang=lang),
            value=t('badwords_enabled', guild_id=guild_id, user_id=user_id, lang=lang) if settings['enabled'] else t('badwords_disabled', guild_id=guild_id, user_id=user_id, lang=lang),
            inline=False
        )
        
        if settings['enabled']:
            embed.add_field(
                name=t('badwords_action', guild_id=guild_id, user_id=user_id, lang=lang),
                value=f"**{settings['action'].upper()}** - {'Delete message' if settings['action'] == 'delete' else 'Warn user'}",
                inline=False
            )
            
            # Show word counts
            th_count = len(BAD_WORDS_TH)
            en_count = len(BAD_WORDS_EN)
            embed.add_field(
                name=t('badwords_count', guild_id=guild_id, user_id=user_id, lang=lang),
                value=f"Thai: {th_count} words\nEnglish: {en_count} words",
                inline=False
            )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        log_action("Bad words settings updated", interaction.user, f"Guild: {guild.name}, Enabled: {settings['enabled']}")
    
    except Exception as e:
        guild_id = interaction.guild.id if interaction.guild else None
        await interaction.followup.send(
            t('error_occurred', guild_id=guild_id, user_id=interaction.user.id, error=str(e)),
            ephemeral=True
        )
        log_action("Bad words command error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="checkbadwords", description="ตรวจสอบคำหยาบคายในข้อความ / Check bad words in text")
@app_commands.describe(
    text="ข้อความที่ต้องการตรวจสอบ / Text to check",
    language="ภาษาที่ต้องการตรวจสอบ (th/en) / Language to check (th/en)"
)
async def checkbadwords_command(
    interaction: discord.Interaction,
    text: str,
    language: str = None
):
    """ตรวจสอบคำหยาบคายในข้อความ"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    await interaction.response.defer(ephemeral=True)
    
    try:
        guild_id = interaction.guild.id if interaction.guild else None
        user_id = interaction.user.id
        lang = get_language_for_context(guild_id, user_id)
        
        check_lang = language.lower() if language else lang
        has_bad_words, found_words = check_bad_words(text, check_lang)
        
        embed = discord.Embed(
            title=t('badwords_check_result', guild_id=guild_id, user_id=user_id, lang=lang, result=t('badwords_check_found', guild_id=guild_id, user_id=user_id, lang=lang, words=', '.join(found_words)) if has_bad_words else t('badwords_check_clean', guild_id=guild_id, user_id=user_id, lang=lang)),
            color=discord.Color.red() if has_bad_words else discord.Color.green()
        )
        
        if has_bad_words:
            embed.description = f"**{t('badwords_detected_words', guild_id=guild_id, user_id=user_id, lang=lang, words=', '.join(found_words))}**"
            embed.add_field(
                name=t('badwords_word', guild_id=guild_id, user_id=user_id, lang=lang),
                value=', '.join(found_words),
                inline=False
            )
        else:
            embed.description = t('badwords_check_clean', guild_id=guild_id, user_id=user_id, lang=lang)
        
        embed.add_field(
            name="Language",
            value=check_lang.upper(),
            inline=False
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        log_action("Bad words check", interaction.user, f"Found: {len(found_words)} words")
    
    except Exception as e:
        guild_id = interaction.guild.id if interaction.guild else None
        await interaction.followup.send(
            t('error_occurred', guild_id=guild_id, user_id=interaction.user.id, error=str(e)),
            ephemeral=True
        )
        log_action("Check bad words error", interaction.user, f"Error: {str(e)}")

@bot.tree.command(name="help", description="แสดงคำสั่งที่ใช้ได้ / Show available commands")
async def help_command(interaction: discord.Interaction):
    """แสดงคำสั่งที่ใช้ได้"""
    if not command_limiter.is_allowed(interaction.user.id):
        return
    
    guild_id = interaction.guild.id if interaction.guild else None
    
    help_embed = discord.Embed(
        title=t('help_title', guild_id),
        description=t('help_description', guild_id),
        color=discord.Color.blue()
    )
    
    help_embed.add_field(
        name="/hello",
        value="ทักทายบอท / Greet the bot",
        inline=False
    )
    help_embed.add_field(
        name="/ping",
        value="ตรวจสอบความเร็วของบอท / Check bot latency",
        inline=False
    )
    help_embed.add_field(
        name="/clear",
        value="ลบข้อความ (ต้องมีสิทธิ์จัดการข้อความ)",
        inline=False
    )
    help_embed.add_field(
        name="/help",
        value="แสดงคำสั่งนี้",
        inline=False
    )
    
    help_embed.add_field(
        name="/sync",
        value="Sync slash commands อีกครั้ง (สำหรับผู้ดูแลระบบเท่านั้น)",
        inline=False
    )
    
    help_embed.add_field(
        name="/checkprofile",
        value="ตรวจสอบผู้ใช้ที่ไม่ตั้งโปรไฟล์ (ต้องมีสิทธิ์จัดการสมาชิก)",
        inline=False
    )
    
    help_embed.add_field(
        name="/autokick",
        value="ตั้งค่าระบบเตะอัตโนมัติ (ต้องมีสิทธิ์ผู้ดูแลระบบ)",
        inline=False
    )
    
    help_embed.add_field(
        name="/kickprofile",
        value="เตะผู้ใช้ที่ไม่ตั้งโปรไฟล์ทันที (ต้องมีสิทธิ์ผู้ดูแลระบบ)",
        inline=False
    )
    
    help_embed.add_field(
        name="/badwords",
        value="จัดการระบบกรองคำหยาบคาย (ต้องมีสิทธิ์จัดการเซิร์ฟเวอร์)",
        inline=False
    )
    
    help_embed.add_field(
        name="/checkbadwords",
        value="ตรวจสอบคำหยาบคายในข้อความ",
        inline=False
    )
    
    help_embed.add_field(
        name="🔒 ระบบความปลอดภัย",
        value="• จำกัดจำนวนคำสั่งต่อเวลา\n• ตรวจสอบสิทธิ์ผู้ใช้\n• ป้องกัน spam และ abuse\n• ตรวจจับ spam แบบอัตโนมัติ\n• ระบบกรองคำหยาบคาย",
        inline=False
    )
    
    help_embed.set_footer(text="พิมพ์ / เพื่อดูคำสั่งทั้งหมด")
    
    await interaction.response.send_message(embed=help_embed, ephemeral=True)
    log_action("Command executed", interaction.user, "help")

# --- Message Filter (ป้องกัน Spam) ---
@bot.event
async def on_message(message):
    """ตรวจสอบข้อความทุกข้อความ"""
    
    # ตรวจสอบว่าไม่ใช่ข้อความจากบอทเอง
    if message.author == bot.user:
        return

    # ตรวจสอบข้อความที่เป็น bot
    if message.author.bot:
        return
    
    # ตรวจสอบว่ามี message_content intent หรือไม่
    # ถ้าไม่มีจะไม่สามารถอ่าน message.content ได้
    if message.content is None or not hasattr(message, 'content') or not message.content:
        # ถ้าไม่มี message content intent ก็ไม่สามารถตรวจสอบ spam/bad words ได้
        # แต่ยังสามารถประมวลผลคำสั่งได้ (slash commands ไม่ต้องการ message content)
        await bot.process_commands(message)
        return
    
    # ตรวจสอบ spam ด้วยระบบหลายมิติ
    spam_detected = False
    spam_reasons = []
    
    guild_id = message.guild.id if message.guild else None
    user_id = message.author.id
    lang = get_language_for_context(guild_id, user_id)
    
    # 1. ตรวจสอบข้อความซ้ำ
    if message.content and spam_detector.check_duplicate_messages(message.author.id, message.content):
        spam_detected = True
        spam_reasons.append(t('spam_reason_duplicate', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 2. ตรวจสอบข้อความเร็วเกินไป
    if spam_detector.check_rapid_messages(message.author.id):
        spam_detected = True
        spam_reasons.append(t('spam_reason_rapid', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 3. ตรวจสอบ emoji spam
    if message.content and spam_detector.check_emoji_spam(message.content):
        spam_detected = True
        spam_reasons.append(t('spam_reason_emoji', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 4. ตรวจสอบ character spam
    if message.content and spam_detector.check_character_spam(message.content):
        spam_detected = True
        spam_reasons.append(t('spam_reason_character', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 5. ตรวจสอบ link spam
    if message.content and spam_detector.check_link_spam(message.content):
        spam_detected = True
        spam_reasons.append(t('spam_reason_link', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 6. ตรวจสอบ mention spam
    if spam_detector.check_mention_spam(message):
        spam_detected = True
        spam_reasons.append(t('spam_reason_mention', guild_id=guild_id, user_id=user_id, lang=lang))
    
    # 7. ตรวจสอบคำหยาบคาย (Bad Words Filter)
    if guild_id and message.content:
        settings = bad_words_settings.get(guild_id, {})
        if settings.get('enabled', False):
            has_bad_words, found_words = check_bad_words(message.content, lang)
            if has_bad_words:
                log_action(
                    "Bad words detected",
                    message.author,
                    f"Words: {', '.join(found_words)} | Guild: {message.guild.name if message.guild else 'DM'}"
                )
                
                # ลบข้อความ
                try:
                    await message.delete()
                except:
                    pass
                
                # ส่งคำเตือน
                try:
                    warning_msg = t('badwords_warning', guild_id=guild_id, user_id=user_id, lang=lang, mention=message.author.mention)
                    warning_msg += f"\n**{t('badwords_detected_words', guild_id=guild_id, user_id=user_id, lang=lang, words=', '.join(found_words))}**"
                    await message.channel.send(warning_msg, delete_after=10)
                except:
                    pass
                
                # ไม่ประมวลผลต่อ
                return
    
    # หากตรวจพบ spam
    if spam_detected:
        log_action(
            "Spam detected", 
            message.author, 
            f"Reasons: {', '.join(spam_reasons)} | Content: {message.content[:50]}"
        )
        
        # เพิ่ม reaction
        try:
            await message.add_reaction('⚠️')
        except:
            pass
        
        # ส่งคำเตือน (ถ้าเป็นสมาชิกในเซิร์ฟเวอร์)
        if isinstance(message.author, discord.Member):
            try:
                warning_msg = t('spam_warning_msg', guild_id=guild_id, user_id=user_id, lang=lang, mention=message.author.mention, reasons=', '.join(spam_reasons))
                await message.channel.send(warning_msg, delete_after=10)
            except:
                pass
        
        # ไม่ประมวลผลคำสั่งต่อ
        return
    
    # รองรับ prefix commands เป็นสำรอง (ถ้าต้องการ)
    await bot.process_commands(message)

# --- ระบบเตะอัตโนมัติเมื่อ Join ---
@bot.event
async def on_member_join(member: discord.Member):
    """ตรวจสอบและเตะผู้ใช้ที่ไม่ตั้งโปรไฟล์เมื่อ join เซิร์ฟเวอร์"""
    guild = member.guild
    
    # ตรวจสอบว่ามีการเปิดใช้งานการเตะอัตโนมัติหรือไม่
    settings = auto_kick_settings.get(guild.id, {})
    if not settings.get('enabled', False):
        return
    
    # ตรวจสอบว่าเป็น bot หรือไม่
    if member.bot:
        return
    
    # ตรวจสอบว่าเป็นเจ้าของเซิร์ฟเวอร์หรือไม่
    if member == guild.owner:
        return
    
    # ตรวจสอบว่าผู้ใช้มีสิทธิ์ในเซิร์ฟเวอร์หรือไม่ (อาจเป็น admin)
    if member.guild_permissions.administrator:
        return
    
    try:
        # ตรวจสอบโปรไฟล์ - ใช้ภาษาของ guild
        guild_id = guild.id
        lang = get_guild_language(guild_id)
        has_issues, issues = has_default_profile(member, guild_id, kick_mode=True, lang=lang)
        
        if has_issues:
            # เตรียมข้อความเตะ
            kick_reason = f"⚠️ Auto-kicked from server. Reason: {', '.join(issues[:3])}"
            
            # ลองส่งข้อความเตือนก่อนเตะ (ใน DMs)
            # ใช้ภาษาของผู้ใช้ที่ถูกเตะ (ถ้ามี) หรือภาษาของ guild
            user_lang = get_language_for_context(guild_id, member.id)
            try:
                dm_embed = discord.Embed(
                    title=t('kick_dm_title', guild_id=guild_id, user_id=member.id, lang=user_lang),
                    description=f"{t('kick_dm_server', guild_id=guild_id, user_id=member.id, lang=user_lang)}: **{guild.name}**",
                    color=discord.Color.red()
                )
                dm_embed.add_field(
                    name=t('kick_dm_reason', guild_id=guild_id, user_id=member.id, lang=user_lang),
                    value="\n".join(f"• {issue}" for issue in issues),
                    inline=False
                )
                suggestions_value = f"• {t('kick_suggestion_avatar', guild_id=guild_id, user_id=member.id, lang=user_lang)}\n"
                suggestions_value += f"• {t('kick_suggestion_age', guild_id=guild_id, user_id=member.id, lang=user_lang)}\n"
                suggestions_value += f"• {t('kick_suggestion_name', guild_id=guild_id, user_id=member.id, lang=user_lang)}"
                dm_embed.add_field(
                    name=t('kick_dm_suggestions', guild_id=guild_id, user_id=member.id, lang=user_lang),
                    value=suggestions_value,
                    inline=False
                )
                await member.send(embed=dm_embed)
            except:
                pass  # ถ้าไม่สามารถส่ง DM ได้ (ปิด DMs)
            
            # เตะผู้ใช้ออกจากเซิร์ฟเวอร์
            try:
                await member.kick(reason=kick_reason)
                
                # บันทึก log
                log_action(
                    "Auto-kicked member",
                    member,
                    f"Guild: {guild.name}, Issues: {', '.join(issues)}"
                )
                
                # ส่งข้อความใน channel (ถ้ามี channel สำหรับ log)
                log_channel_id = settings.get('log_channel_id')
                if log_channel_id:
                    log_channel = guild.get_channel(log_channel_id)
                    if log_channel:
                        # ใช้ภาษาของ guild สำหรับ log channel
                        embed = discord.Embed(
                            title=t('autokick_log_title', guild_id=guild_id, user_id=None, lang=lang),
                            description=t('autokick_log_user', guild_id=guild_id, user_id=None, lang=lang, mention=member.mention, name=member.name),
                            color=discord.Color.red(),
                            timestamp=datetime.now()
                        )
                        embed.add_field(
                            name=t('kick_dm_reason', guild_id=guild_id, user_id=None, lang=lang),
                            value="\n".join(f"• {issue}" for issue in issues),
                            inline=False
                        )
                        embed.set_footer(text=f"ID: {member.id}")
                        await log_channel.send(embed=embed)
            except discord.Forbidden:
                log_action(
                    "Kick failed - no permission",
                    member,
                    f"Guild: {guild.name}"
                )
            except Exception as e:
                log_action(
                    "Kick error",
                    member,
                    f"Guild: {guild.name}, Error: {str(e)}"
                )
    except Exception as e:
        log_action(
            "Member join check error",
            member,
            f"Guild: {guild.name}, Error: {str(e)}"
        )

# --- Run Bot ---
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: DISCORD_TOKEN not found in .env file")
        print("Please create .env file and add DISCORD_TOKEN=your_token_here")
        exit(1)
    
    # Display token info (only first part for security)
if TOKEN: 
        token_preview = TOKEN[:20] + "..." if len(TOKEN) > 20 else TOKEN
        print(f"✅ Token loaded successfully: {token_preview}")
        print("Connecting to Discord...")
    
try:
        bot.run(TOKEN)
except discord.LoginFailure:
        print("❌ ERROR: Invalid token! Please check DISCORD_TOKEN")
        print("💡 Tip: Token may have expired or been reset")
        print("    Go to https://discord.com/developers/applications and create a new token")
except discord.PrivilegedIntentsRequired as e:
        print("⚠️ WARNING: Privileged Intents Required but not enabled!")
        print("=" * 60)
        print("The bot requires MESSAGE CONTENT INTENT to be enabled.")
        print("")
        print("📋 SOLUTION: Enable MESSAGE CONTENT INTENT")
        print("1. Go to: https://discord.com/developers/applications")
        print("2. Select your application")
        print("3. Go to 'Bot' section")
        print("4. Scroll down to 'Privileged Gateway Intents'")
        print("5. Enable: ✅ MESSAGE CONTENT INTENT")
        print("6. Save changes")
        print("7. Run the bot again")
        print("")
        print("⚠️ NOTE: Without MESSAGE CONTENT INTENT:")
        print("   - Bad words filter will NOT work")
        print("   - Spam detection will NOT work")
        print("   - Bot slash commands will STILL work")
        print("")
        print("💡 Alternative: Add ENABLE_MESSAGE_CONTENT=false to .env")
        print("   to disable message_content checking")
        print("=" * 60)
        print(f"\nDetailed error: {str(e)}")
        exit(1)
except Exception as e:
        print(f"❌ ERROR: An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()