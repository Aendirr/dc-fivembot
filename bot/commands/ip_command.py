from discord import app_commands, Interaction
from discord.ext import commands
import discord
import config

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="ip", description="Sunucuya bağlantı linki gönderir.")
    async def ip(interaction: Interaction):
        embed = discord.Embed(
            title="Sunucuya Bağlan",
            description="Aşağıdaki butona tıklayarak bağlanabilirsin.",
            color=discord.Color.green()
        )
        view = discord.ui.View()
        button = discord.ui.Button(label="Bağlan", url=config.IP_URL)
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
