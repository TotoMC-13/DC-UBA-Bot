import os
from pathlib import Path

import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv


class client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.default(),
            application_id=os.getenv("BOT_ID"),
        )
        self.synced = False
        self.intents.members = True

    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()
 
        target_dir = Path.cwd() / "cogs"

        for cog in target_dir.rglob("*.py"):
            await self.load_extension(f"cogs.{cog.stem}")

        await cltree.sync()

        self.synced = True

    async def on_ready(self):
        await self.wait_until_ready()
        print(f"Logged in as {self.user}")


aclient = client()
cltree = aclient.tree

load_dotenv()

if __name__ == "__main__":
    aclient.run(os.getenv("TOKEN"))