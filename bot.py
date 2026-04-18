import discord
from discord.ext import commands
from typing import Optional
from aiohttp import web
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

async def handle(request):
    data = await request.json()
    command = data.get("command").strip()
    guild_id = int(data.get("guild_id"))
    
    guild = client.get_guild(guild_id)
    text_channels = [c for c in guild.channels if isinstance(c, discord.TextChannel)]
    channel = random.choice(text_channels)

    if command == "!test":
        await channel.send("✅ Bot is working!")
    elif command.startswith("!create_channels"):
        parts = command.split()
        amount = int(parts[1])
        name = parts[2]
        for i in range(1, amount + 1):
            await guild.create_text_channel(f"{name}-{str(i).zfill(3)}")
    elif command.startswith("!nuke_channels"):
        parts = command.split()
        exclude = parts[1] if len(parts) > 1 else None
        for ch in guild.channels:
            if exclude and str(ch.id) == exclude:
                continue
            try:
                await ch.delete()
            except:
                pass

    return web.Response(text=f"Executed '{command}'")

async def start_server():
    app = web.Application()
    app.router.add_post("/send", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    await site.start()

@client.command()
async def test(ctx):
    await ctx.send("✅ Bot is working!")

@client.command()
@commands.has_permissions(administrator=True)
async def create_channels(ctx, amount: int, name: str):
    for i in range(1, amount + 1):
        channel_name = f"{name}-{str(i).zfill(3)}"
        await ctx.guild.create_text_channel(channel_name)

@client.command()
@commands.has_permissions(administrator=True)
async def nuke_channels(ctx, exclude: Optional[str] = None):
    for channel in ctx.guild.channels:
        if exclude and str(channel.id) == exclude:
            continue
        try:
            await channel.delete(reason="Server rebrand - channel nuke")
        except discord.Forbidden:
            pass
        except discord.HTTPException:
            pass

@client.event
async def on_ready():
    asyncio.ensure_future(start_server())
    print(f"HTTP server started on port 8080")
    print(f"Logged in as {client.user}")

client.run("TOKEN_HERE")
