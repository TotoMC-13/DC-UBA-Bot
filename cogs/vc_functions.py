import os

import discord
from discord.ext import commands
from dotenv import load_dotenv


class VcFunctions(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        #self.category_id = int(os.getenv("CATEGORY_ID"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None:  # Si el usuario entra a un canal
            category = after.channel.category
            #if category and category.id == self.category_id:
            if category:
                all_occupied = await self.all_channels_occupied(category.voice_channels)
                
                if all_occupied:
                    new_channel_number = await self.get_next_channel_number(category)
                    await member.guild.create_voice_channel(name=f"sala de estudio {new_channel_number}", category=category)

        if before.channel is not None:  # Si el usuario sale de un canal
            category = before.channel.category
            if category:
                free_channels = await self.free_channels_list(category.voice_channels)
                
                if len(free_channels) > 1:
                    await free_channels[-1].delete()

    async def get_next_channel_number(self, category: discord.CategoryChannel) -> int:
        """Encuentra el siguiente número disponible para un canal de estudio"""
        existing_numbers = []

        for channel in category.voice_channels:
            if "sala de estudio" in channel.name:
                parts = channel.name.split()
                if parts[-1].isdigit():  # Si el último elemento del nombre es un número
                    existing_numbers.append(int(parts[-1]))

        return max(existing_numbers, default=0) + 1  # Siguiente número disponible

    async def all_channels_occupied(self, channels: list[discord.VoiceChannel]) -> bool:
        return all(len(channel.members) > 0 for channel in channels)

    async def free_channels_list(self, channels: list[discord.VoiceChannel]) -> list[discord.VoiceChannel]:
        return [channel for channel in channels if len(channel.members) == 0]

async def setup(client: commands.Bot) -> None:
    await client.add_cog(VcFunctions(client))
    print(f"Module vc_functions.py was loaded succesfully.")