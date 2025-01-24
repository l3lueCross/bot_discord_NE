import os
import discord
from discord.ext import commands
from discord import app_commands
from myserv  import server_on
import re  # ใช้สำหรับดึง Role ID

intents = discord.Intents.default()
intents.messages = True  # Enable messages
intents.message_content = True  # Enable message content
intents.members = True  # Enable member intents to access member data

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def test(ctx):
    await ctx.send('Hello!')

@bot.tree.command(name='helloworld', description='Say hello to the world')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message('Hello World!')
@bot.tree.command(name='list', description='List all members with a specific role')
@app_commands.describe(role_name='The ID or name of the role')
async def list_member(interaction: discord.Interaction, role_name: str):
    guild = interaction.guild

    # หากพิมพ์ @role_name แล้วจะมีรูปแบบ "<@&RoleID>"
    role_id_match = re.match(r"<@&(\d+)>", role_name)

    if role_id_match:
        # หากพบ Role ID จาก @role_name ให้ใช้ ID นั้น
        role_id = int(role_id_match.group(1))
        role = discord.utils.get(guild.roles, id=role_id)
    else:
        # หากไม่พบ Role ID ให้ใช้ชื่อบทบาท
        role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        await interaction.response.send_message(f"Role '{role_name}' not found.")
        return

    # ใช้ guild.chunk() เพื่อโหลดสมาชิกทั้งหมดทีละชุด
    members_with_role = []

    # chunk() จะโหลดสมาชิกทั้งหมดทีละชุด และจะทำให้บอทไม่หน่วง
    await guild.chunk()  # ทำให้ข้อมูลสมาชิกโหลดเสร็จสมบูรณ์

    # คัดเลือกสมาชิกที่มี Role ตามที่กำหนด
    for member in guild.members:
        if role in member.roles:
            members_with_role.append(member.display_name)

    if members_with_role:
        # แสดงรายชื่อสมาชิกที่มี Role นี้
        await interaction.response.send_message(f"Members with the role '{role_name}':\n" + "\n".join(members_with_role))
    else:
        await interaction.response.send_message(f"No members found with the role '{role_name}'.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} command(s)')
    
server_on()
# Run the bot with your token
bot.run(os.getenv('TOKEN'))