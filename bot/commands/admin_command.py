from discord import app_commands, Interaction
from discord.ext import commands
import discord

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="admin", description="Aktif adminleri gösterir.")
    async def admin(interaction: Interaction):
        active_admins = ["👮 Admin1", "👮 Admin2", "👮‍♀️ Admin3"]
        embed = discord.Embed(
            title="👮 Aktif Adminler",
            description="\n".join(active_admins),
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
