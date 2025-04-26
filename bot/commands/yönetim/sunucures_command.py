from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="sunucures", description="Sunucuyu yeniden başlatır (Admin komutu).")
    async def sunucures(interaction: Interaction):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
                }
                async with session.post(f"{config.BACKEND_URL}/restart", headers=headers) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="🛠️ Sunucu Yeniden Başlatılıyor...",
                            description="Lütfen birkaç dakika bekleyin. Sunucu restart işlemi başlatıldı.",
                            color=discord.Color.green()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Restart Başarısız",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
