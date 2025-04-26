from discord import app_commands, Interaction
from discord.ext import commands
import discord
import servercomp

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="sunucu", description="Sunucunun açıklamasını gönderir.")
    async def sunucu(interaction: Interaction):
        embed = discord.Embed(
            title="🎮 Sunucu Bilgileri",
            description=servercomp.SERVER_DESCRIPTION,
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
