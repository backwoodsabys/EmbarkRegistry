import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

keep_alive()

TARGET_CHANNEL_ID = 1453693161435041854
ADD_ROLE_ID = 1453693160931987572
NON_CLAN_ROLE_ID = 1453693160931987573
NEED_ROLE_ID = 1453693160893972583
MOD_CHANNEL_ID = 1453693161435041846

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)

    if message.author.bot:
        return
    if message.channel.id != TARGET_CHANNEL_ID:
        return

    member = message.author
    if not isinstance(member, discord.Member):
        guild = bot.get_guild(message.guild.id)
        member = guild.get_member(message.author.id)

    if member is None:
        return
    
    content = message.content
    lower = message.content.lower()
    modChannel = bot.get_channel(MOD_CHANNEL_ID)
    remove_role = message.guild.get_role(NEED_ROLE_ID)
    add_role = message.guild.get_role(ADD_ROLE_ID)
    non_clan_role = message.guild.get_role(NON_CLAN_ROLE_ID)
    
    if remove_role is None or add_role is None or non_clan_role is None:
        return

    try:
        
        await member.remove_roles(remove_role, reason="Typed game name in channel")
        
        if lower == "clan friend":
            await member.add_roles(non_clan_role, reason="Registered as a clan friend")
            await message.channel.send(
                f"{member.mention} registered as 'clan friend'. Role updated."
            )
            await message.delete()
        else:
            await member.add_roles(add_role, reason="Typed game name in channel")
            await member.edit(nick=content, reason="Set via game name registration")
            await message.channel.send(f"{member.name} registered game name '{content}' and nickname was updated.")
            await modChannel.send(f"{member.name} registered game name as '{content}' and nickname was updated.")
            await message.delete()

    except discord.Forbidden:
        print("Missing permissions to edit roles or nickname.")
    except discord.HTTPException as e:
        print(f"HTTP error: {e}")

@bot.event
async def on_member_join(member: discord.Member):
    role = member.guild.get_role(NEED_ROLE_ID)
    if role is None:
        return

    try:
        await member.add_roles(role, reason="Auto member role on join")
        print(f"Gave {member} the member role.")
    except discord.Forbidden:
        print("Missing permissions to add roles.")
    except discord.HTTPException as e:
        print(f"HTTP error while adding role: {e}")

bot.run(TOKEN)