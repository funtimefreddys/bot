# i18n.py - Internationalization (i18n) Support
# Multi-language support for the bot

import os
from dotenv import load_dotenv

load_dotenv()

# Default language (can be set in .env)
DEFAULT_LANGUAGE = os.getenv('BOT_LANGUAGE', 'th').lower()

# Language translations
LANGUAGES = {
    'th': {
        # Bot messages
        'bot_ready': '🤖 บอทเชื่อมต่อสำเร็จ!',
        'bot_name': 'ชื่อ',
        'bot_id': 'ID',
        'connected_to': 'เชื่อมต่อกับ {count} เซิร์ฟเวอร์',
        'sync_commands': '🔄 กำลัง sync slash commands...',
        'sync_success': '✅ Sync slash commands สำเร็จ! ({count} คำสั่ง)',
        'sync_error': '❌ เกิดข้อผิดพลาดในการ sync commands: {error}',
        'bot_ready_message': '✅ บอทพร้อมใช้งาน! ลองพิมพ์ / ใน Discord เพื่อดูคำสั่ง',
        
        # Commands
        'hello_response': 'สวัสดีค่ะ {name}! ยินดีที่ได้รู้จักค่ะ {mention}',
        'hello_response_no_name': 'สวัสดีค่ะ {mention}! ยินดีที่ได้รู้จักค่ะ',
        'ping_response': '🏓 Pong! Latency: {latency}ms',
        
        # Errors
        'rate_limit': '⏰ คุณใช้คำสั่งเร็วเกินไป! กรุณารอ {seconds} วินาที',
        'permission_denied': '❌ คุณไม่มีสิทธิ์ใช้คำสั่งนี้!',
        'command_error': '❌ เกิดข้อผิดพลาดในการดำเนินการคำสั่ง!',
        'token_not_found': '❌ ERROR: ไม่พบ DISCORD_TOKEN ในไฟล์ .env',
        'token_invalid': '❌ ERROR: Token ไม่ถูกต้อง! โปรดตรวจสอบ DISCORD_TOKEN',
        
        # Help
        'help_title': '📋 คำสั่งที่ใช้ได้',
        'help_description': 'คำสั่ง Slash Commands ทั้งหมดของบอท',
        'help_security': '🔒 ระบบความปลอดภัย',
        'help_footer': 'พิมพ์ / เพื่อดูคำสั่งทั้งหมด',
        
        # Spam detection
        'spam_warning': '⚠️ ตรวจพบพฤติกรรม spam!',
        'spam_reasons': '**เหตุผล:** {reasons}',
        'spam_stop': 'กรุณาหยุดพฤติกรรมดังกล่าว',
        
        # Profile check
        'profile_issues': '⚠️ ตรวจพบปัญหาโปรไฟล์',
        'profile_normal': '✅ {mention} มีโปรไฟล์ปกติ',
        'profile_no_issues': '✅ ไม่พบผู้ใช้ที่มีปัญหาโปรไฟล์',
        'profile_checked': '📋 รายงานผู้ใช้ที่ไม่ตั้งโปรไฟล์',
        
        # Auto-kick
        'autokick_title': '⚙️ ตั้งค่าระบบเตะอัตโนมัติ',
        'autokick_enabled': '✅ เปิดใช้งาน',
        'autokick_disabled': '❌ ปิดใช้งาน',
        'autokick_settings': '**อายุบัญชีขั้นต่ำ:** {days} วัน\n**ต้องมี avatar:** {require}',
        
        # Clear command
        'clear_success': '✅ ลบข้อความ {count} ข้อความแล้ว',
        'clear_invalid': '❌ จำนวนข้อความที่ลบได้อยู่ระหว่าง 1-100 ข้อความ',
        'clear_permission': '❌ บอทไม่มีสิทธิ์ลบข้อความ!',
        'clear_error': '❌ เกิดข้อผิดพลาดในการลบข้อความ!',
        
        # Kick
        'kick_success': '✅ เตะสมาชิกออกแล้ว',
        'kick_cannot_bot': '❌ ไม่สามารถเตะ bot ได้',
        'kick_cannot_owner': '❌ ไม่สามารถเตะเจ้าของเซิร์ฟเวอร์ได้',
        'kick_cannot_admin': '❌ ไม่สามารถเตะผู้ดูแลระบบได้',
        'kick_profile_normal': '❌ {mention} มีโปรไฟล์ปกติ ไม่ควรเตะ',
        'kick_permission': '❌ บอทไม่มีสิทธิ์เตะสมาชิก!',
        
        # Profile issues
        'profile_issue_no_avatar': 'ไม่มี avatar',
        'profile_issue_no_roles': 'ไม่มี roles พิเศษ',
        'profile_issue_short_name': 'ชื่อสั้นเกินไป',
        'profile_issue_new_account': 'บัญชีใหม่มาก ({days} วัน)',
        
        # Kick messages
        'kick_dm_title': '🚫 คุณถูกเตะออกจากเซิร์ฟเวอร์',
        'kick_dm_server': 'เซิร์ฟเวอร์',
        'kick_dm_reason': 'เหตุผล',
        'kick_dm_suggestions': 'คำแนะนำ',
        'kick_suggestion_avatar': 'ตั้งค่า avatar',
        'kick_suggestion_age': 'รอให้บัญชีมีอายุมากขึ้น',
        'kick_suggestion_name': 'ตั้งชื่อที่เหมาะสม',
        'kick_reason_prefix': 'เตะโดย {user} - เหตุผล: {reasons}',
        
        # Command responses (Thai)
        'rate_limit_cooldown': '⏰ คำสั่งนี้ถูกจำกัด! กรุณารอ {seconds} วินาที',
        'command_invalid_amount': '❌ จำนวนข้อความที่ลบได้อยู่ระหว่าง 1-100 ข้อความ',
        'command_server_only': '❌ คำสั่งนี้ใช้ได้เฉพาะในเซิร์ฟเวอร์เท่านั้น',
        'clear_amount': '❌ จำนวนข้อความที่ลบได้อยู่ระหว่าง 1-100 ข้อความ',
        'sync_success_msg': '✅ Sync commands สำเร็จ! ({count} คำสั่ง)\nคำสั่งจะปรากฏใน Discord ภายใน 1-5 นาที',
        'sync_deleted': '🗑️ ลบคำสั่งเก่าแล้ว กำลัง sync ใหม่...',
        'checkprofile_found': '📋 รายงานผู้ใช้ที่ไม่ตั้งโปรไฟล์',
        'checkprofile_found_count': 'พบ {count} คน',
        'checkprofile_showing': 'แสดง {shown} คนแรกจากทั้งหมด {total} คน',
        'checkprofile_user_info': 'ข้อมูล',
        'checkprofile_issues': 'ปัญหา',
        'autokick_status': 'สถานะ',
        'autokick_settings_label': 'ตั้งค่า',
        'autokick_log_channel': 'Log Channel',
        'invalid_language': '❌ Invalid language! Use \'th\' for Thai or \'en\' for English\n❌ ภาษาไม่ถูกต้อง! ใช้ \'th\' สำหรับไทย หรือ \'en\' สำหรับอังกฤษ',
        'language_changed_server': '✅ Server language changed to {lang} / เปลี่ยนภาษาของเซิร์ฟเวอร์เป็น {lang} แล้ว!\n🌐 All users in this server will see {lang} by default',
        'language_changed_user': '✅ Your personal language changed to {lang} / เปลี่ยนภาษาส่วนตัวของคุณเป็น {lang} แล้ว!\n🌐 You will see bot messages in {lang} (unless server has different language)',
        'language_invalid_scope': '❌ Invalid scope! Use \'server\' or \'user\'\n❌ ขอบเขตไม่ถูกต้อง! ใช้ \'server\' หรือ \'user\'',
        'language_need_permission': '❌ You need \'Manage Server\' permission to change server language!\n❌ คุณต้องมีสิทธิ์ \'จัดการเซิร์ฟเวอร์\' เพื่อเปลี่ยนภาษาของเซิร์ฟเวอร์!',
        'language_dm_only': '❌ This command can only be used in a server',
        
        # Spam detection messages
        'spam_reason_duplicate': 'ข้อความซ้ำ',
        'spam_reason_rapid': 'ส่งข้อความเร็วเกินไป',
        'spam_reason_emoji': 'emoji มากเกินไป',
        'spam_reason_character': 'ตัวอักษรซ้ำ',
        'spam_reason_link': 'ลิงก์มากเกินไป',
        'spam_reason_mention': 'mention มากเกินไป',
        'spam_warning_msg': '{mention} ⚠️ ตรวจพบพฤติกรรม spam!\n**เหตุผล:** {reasons}\nกรุณาหยุดพฤติกรรมดังกล่าว',
        
        # Auto-kick log
        'autokick_log_title': '🚫 เตะสมาชิกออกอัตโนมัติ',
        'autokick_log_user': 'ผู้ใช้: {mention} ({name})',
        
        # Bad Words Filter
        'badwords_title': '🚫 ระบบกรองคำหยาบคาย',
        'badwords_enabled': '✅ เปิดใช้งาน',
        'badwords_disabled': '❌ ปิดใช้งาน',
        'badwords_detected': '⚠️ ตรวจพบคำหยาบคายในข้อความ!',
        'badwords_detected_words': 'คำหยาบคายที่พบ: {words}',
        'badwords_warning': '{mention} ⚠️ กรุณาหยุดใช้คำหยาบคาย!',
        'badwords_added': '✅ เพิ่มคำหยาบคาย: {word}',
        'badwords_removed': '✅ ลบคำหยาบคาย: {word}',
        'badwords_list': '📋 รายการคำหยาบคาย ({count} คำ)',
        'badwords_not_found': '❌ ไม่พบคำหยาบคายในรายการ',
        'badwords_already_exists': '⚠️ คำหยาบคายนี้มีในรายการแล้ว',
        'badwords_check_result': '🔍 ผลการตรวจสอบ: {result}',
        'badwords_check_clean': '✅ ข้อความสะอาด ไม่มีคำหยาบคาย',
        'badwords_check_found': '⚠️ พบคำหยาบคาย: {words}',
        'badwords_status': 'สถานะ',
        'badwords_action': 'Action',
        'badwords_word': 'คำ',
        'badwords_count': 'จำนวน',
        
        # Generic
        'yes': 'ใช่',
        'no': 'ไม่ใช่',
        'error_occurred': '❌ เกิดข้อผิดพลาด: {error}',
    },
    'en': {
        # Bot messages
        'bot_ready': '🤖 Bot connected successfully!',
        'bot_name': 'Name',
        'bot_id': 'ID',
        'connected_to': 'Connected to {count} server(s)',
        'sync_commands': '🔄 Syncing slash commands...',
        'sync_success': '✅ Slash commands synced successfully! ({count} commands)',
        'sync_error': '❌ Error syncing commands: {error}',
        'bot_ready_message': '✅ Bot is ready! Type / in Discord to see commands',
        
        # Commands
        'hello_response': 'Hello {name}! Nice to meet you {mention}',
        'hello_response_no_name': 'Hello {mention}! Nice to meet you',
        'ping_response': '🏓 Pong! Latency: {latency}ms',
        
        # Errors
        'rate_limit': '⏰ You are using commands too fast! Please wait {seconds} seconds',
        'permission_denied': '❌ You do not have permission to use this command!',
        'command_error': '❌ An error occurred while executing the command!',
        'token_not_found': '❌ ERROR: DISCORD_TOKEN not found in .env file',
        'token_invalid': '❌ ERROR: Invalid token! Please check DISCORD_TOKEN',
        
        # Help
        'help_title': '📋 Available Commands',
        'help_description': 'All Slash Commands of the bot',
        'help_security': '🔒 Security System',
        'help_footer': 'Type / to see all commands',
        
        # Spam detection
        'spam_warning': '⚠️ Spam behavior detected!',
        'spam_reasons': '**Reason:** {reasons}',
        'spam_stop': 'Please stop this behavior',
        
        # Profile check
        'profile_issues': '⚠️ Profile issues detected',
        'profile_normal': '✅ {mention} has a normal profile',
        'profile_no_issues': '✅ No users with profile issues found',
        'profile_checked': '📋 Users without profile setup report',
        
        # Auto-kick
        'autokick_title': '⚙️ Auto-kick System Settings',
        'autokick_enabled': '✅ Enabled',
        'autokick_disabled': '❌ Disabled',
        'autokick_settings': '**Minimum account age:** {days} days\n**Require avatar:** {require}',
        
        # Clear command
        'clear_success': '✅ Cleared {count} messages',
        'clear_invalid': '❌ Number of messages to clear must be between 1-100',
        'clear_permission': '❌ Bot does not have permission to delete messages!',
        'clear_error': '❌ Error occurred while clearing messages!',
        
        # Kick
        'kick_success': '✅ Member kicked successfully',
        'kick_cannot_bot': '❌ Cannot kick bots',
        'kick_cannot_owner': '❌ Cannot kick server owner',
        'kick_cannot_admin': '❌ Cannot kick administrators',
        'kick_profile_normal': '❌ {mention} has a normal profile, should not kick',
        'kick_permission': '❌ Bot does not have permission to kick members!',
        
        # Profile issues
        'profile_issue_no_avatar': 'No avatar',
        'profile_issue_no_roles': 'No special roles',
        'profile_issue_short_name': 'Name too short',
        'profile_issue_new_account': 'Account too new ({days} days)',
        
        # Kick messages
        'kick_dm_title': '🚫 You were kicked from the server',
        'kick_dm_server': 'Server',
        'kick_dm_reason': 'Reason',
        'kick_dm_suggestions': 'Suggestions',
        'kick_suggestion_avatar': 'Set avatar',
        'kick_suggestion_age': 'Wait for account to age',
        'kick_suggestion_name': 'Set appropriate name',
        'kick_reason_prefix': 'Kicked by {user} - Reason: {reasons}',
        
        # Command responses (English)
        'rate_limit_cooldown': '⏰ Command is on cooldown! Please wait {seconds} seconds',
        'command_invalid_amount': '❌ Number of messages to clear must be between 1-100',
        'command_server_only': '❌ This command can only be used in a server',
        'clear_amount': '❌ Number of messages to clear must be between 1-100',
        'sync_success_msg': '✅ Commands synced successfully! ({count} commands)\nCommands will appear in Discord within 1-5 minutes',
        'sync_deleted': '🗑️ Deleted old commands, syncing new ones...',
        'checkprofile_found': '📋 Users without profile setup report',
        'checkprofile_found_count': 'Found {count} users',
        'checkprofile_showing': 'Showing first {shown} of {total} users',
        'checkprofile_user_info': 'Information',
        'checkprofile_issues': 'Issues',
        'autokick_status': 'Status',
        'autokick_settings_label': 'Settings',
        'autokick_log_channel': 'Log Channel',
        'invalid_language': '❌ Invalid language! Use \'th\' for Thai or \'en\' for English',
        'language_changed_server': '✅ Server language changed to {lang}!\n🌐 All users in this server will see {lang} by default',
        'language_changed_user': '✅ Your personal language changed to {lang}!\n🌐 You will see bot messages in {lang} (unless server has different language)',
        'language_invalid_scope': '❌ Invalid scope! Use \'server\' or \'user\'',
        'language_need_permission': '❌ You need \'Manage Server\' permission to change server language!',
        'language_dm_only': '❌ This command can only be used in a server',
        
        # Spam detection messages
        'spam_reason_duplicate': 'Duplicate messages',
        'spam_reason_rapid': 'Messages too rapid',
        'spam_reason_emoji': 'Too many emojis',
        'spam_reason_character': 'Repeating characters',
        'spam_reason_link': 'Too many links',
        'spam_reason_mention': 'Too many mentions',
        'spam_warning_msg': '{mention} ⚠️ Spam behavior detected!\n**Reason:** {reasons}\nPlease stop this behavior',
        
        # Auto-kick log
        'autokick_log_title': '🚫 Auto-kicked member',
        'autokick_log_user': 'User: {mention} ({name})',
        
        # Bad Words Filter
        'badwords_title': '🚫 Bad Words Filter',
        'badwords_enabled': '✅ Enabled',
        'badwords_disabled': '❌ Disabled',
        'badwords_detected': '⚠️ Bad words detected in message!',
        'badwords_detected_words': 'Bad words found: {words}',
        'badwords_warning': '{mention} ⚠️ Please stop using bad words!',
        'badwords_added': '✅ Added bad word: {word}',
        'badwords_removed': '✅ Removed bad word: {word}',
        'badwords_list': '📋 Bad words list ({count} words)',
        'badwords_not_found': '❌ Bad word not found in list',
        'badwords_already_exists': '⚠️ Bad word already exists in list',
        'badwords_check_result': '🔍 Check result: {result}',
        'badwords_check_clean': '✅ Message is clean, no bad words',
        'badwords_check_found': '⚠️ Found bad words: {words}',
        'badwords_status': 'Status',
        'badwords_action': 'Action',
        'badwords_word': 'Word',
        'badwords_count': 'Count',
        
        # Generic
        'yes': 'Yes',
        'no': 'No',
        'error_occurred': '❌ An error occurred: {error}',
    }
}

def get_text(key: str, language: str = None, **kwargs) -> str:
    """
    Get translated text
    
    Args:
        key: Translation key
        language: Language code ('th' or 'en'), defaults to DEFAULT_LANGUAGE
        **kwargs: Variables to format into the text
    
    Returns:
        Translated and formatted text
    """
    if language is None:
        language = DEFAULT_LANGUAGE
    
    # Fallback to English if language not found
    if language not in LANGUAGES:
        language = 'en'
    
    # Get text from language dict
    lang_dict = LANGUAGES.get(language, LANGUAGES['en'])
    text = lang_dict.get(key, LANGUAGES['en'].get(key, key))
    
    # Format with kwargs if provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            # If formatting fails, return text as is
            pass
    
    return text

def set_language(lang: str):
    """Set default language (th or en)"""
    global DEFAULT_LANGUAGE
    if lang.lower() in ['th', 'en']:
        DEFAULT_LANGUAGE = lang.lower()
        return True
    return False

def get_language() -> str:
    """Get current default language"""
    return DEFAULT_LANGUAGE

