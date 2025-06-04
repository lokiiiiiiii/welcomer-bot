import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from keep_alive import keep_alive  # Optional: Only if using Replit or cyclic.sh

load_dotenv()

TOKEN = os.getenv("TOKEN")  # Discord bot token
GUILD_ID = int(os.getenv("GUILD_ID") or "0")
ROLE_NAME = os.getenv("ROLE_NAME")

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

gif_urls = [
    "https://media.tenor.com/bUvy12q0dGQAAAAC/welcome.gif",
    "https://media.tenor.com/t1_tBvlC-BsAAAAC/hello-hi.gif",
    "https://media.tenor.com/58ZehUpuw3UAAAAC/hi-there-hello.gif",
    "https://media.tenor.com/YqCj9a-5vBMAAAAC/welcome-anime.gif",
    "https://media.tenor.com/pX9n1cfPtOgAAAAC/welcome-cute.gif",
    "https://media.tenor.com/kC7ZpG8lwhgAAAAC/hi-hello.gif",
]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Serving Loki!"))
    print(f"✅ Loki Welcomer is active as {bot.user}")

@bot.event
async def on_member_join(member):
    try:
        guild = bot.get_guild(GUILD_ID)
        if guild is None:
            print(f"⚠️ Guild with ID {GUILD_ID} not found.")
            return

        channel = discord.utils.get(guild.text_channels, name="welcome")
        if not channel:
            print("⚠️ 'welcome' channel not found.")
            return

        gif = random.choice(gif_urls)
        print(f"Selected GIF URL: {gif}")  # Debug print to check selected GIF

        embed = discord.Embed(
            title="🎉 स्वागत है!",
            description=f"🙏 नमस्ते {member.mention}, हमारे सर्वर में आपका दिल से स्वागत है!\n\n🎮 Enjoy your stay!",
            color=discord.Color.green()
        )
        embed.set_image(url=gif)
        embed.set_footer(text="Powered by Loki AI")

        await channel.send(embed=embed)

        role = discord.utils.get(guild.roles, name=ROLE_NAME)
        if role:
            await member.add_roles(role)
            print(f"✅ Role '{ROLE_NAME}' assigned to {member.name}")
        else:
            print(f"⚠️ Role '{ROLE_NAME}' not found.")

    except Exception as e:
        print(f"❌ Error in on_member_join: {e}")

@bot.command()
async def testgif(ctx):
    try:
        test_gif_url = "https://media.tenor.com/bUvy12q0dGQAAAAC/welcome.gif"
        embed = discord.Embed(title="Test GIF Embed")
        embed.set_image(url=test_gif_url)
        await ctx.send(embed=embed)
        print("✅ testgif command executed successfully.")
    except Exception as e:
        await ctx.send(f"❌ Error sending test GIF: {e}")
        print(f"❌ Error in testgif command: {e}")

keep_alive()

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ TOKEN not found in .env file")
