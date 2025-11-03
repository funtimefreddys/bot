# language_chooser.py - Interactive language selector
# Creates a view with buttons to select language

import discord
from discord import app_commands
from i18n import get_text

class LanguageView(discord.ui.View):
    """Interactive language selector with buttons"""
    
    def __init__(self, guild_id: int = None, user_id: int = None):
        super().__init__(timeout=60)
        self.guild_id = guild_id
        self.user_id = user_id
        self.current_lang = 'th'  # Will be determined
    
    @discord.ui.button(label='🇹🇭 ไทย', style=discord.ButtonStyle.primary, row=0)
    async def select_thai(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Select Thai language"""
        # Import here to avoid circular import
        from main import user_languages, guild_languages
        
        if self.guild_id and interaction.user.guild_permissions.manage_guild:
            # Server language change
            guild_languages[self.guild_id] = 'th'
            await interaction.response.send_message(
                "✅ Server language changed to **ไทย (Thai)** / เปลี่ยนภาษาของเซิร์ฟเวอร์เป็น **ไทย** แล้ว!\n"
                "🌐 All users in this server will see Thai by default",
                ephemeral=True
            )
        else:
            # User personal language
            user_languages[self.user_id] = 'th'
            await interaction.response.send_message(
                "✅ Your personal language changed to **ไทย (Thai)** / เปลี่ยนภาษาส่วนตัวของคุณเป็น **ไทย** แล้ว!\n"
                "🌐 You will see bot messages in Thai",
                ephemeral=True
            )
        
        self.stop()
    
    @discord.ui.button(label='🇬🇧 English', style=discord.ButtonStyle.primary, row=0)
    async def select_english(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Select English language"""
        # Import here to avoid circular import
        from main import user_languages, guild_languages
        
        if self.guild_id and interaction.user.guild_permissions.manage_guild:
            # Server language change
            guild_languages[self.guild_id] = 'en'
            await interaction.response.send_message(
                "✅ Server language changed to **English** / เปลี่ยนภาษาของเซิร์ฟเวอร์เป็น **อังกฤษ** แล้ว!\n"
                "🌐 All users in this server will see English by default",
                ephemeral=True
            )
        else:
            # User personal language
            user_languages[self.user_id] = 'en'
            await interaction.response.send_message(
                "✅ Your personal language changed to **English** / เปลี่ยนภาษาส่วนตัวของคุณเป็น **อังกฤษ** แล้ว!\n"
                "🌐 You will see bot messages in English",
                ephemeral=True
            )
        
        self.stop()

