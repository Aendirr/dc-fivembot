from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):

    @bot.tree.command(name="event", description="Sunucuda etkinlik duyurusu başlatır.")
    @app_commands.describe(title="Etkinlik başlığı", description="Etkinlik açıklaması")
    async def event(interaction: Interaction, title: str, description: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {"title": title, "description": description}
                async with session.post(f"{config.BACKEND_URL}/event", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="📢 Etkinlik Yayınlandı",
                            description=f"**{title}**\n{description}",
                            color=discord.Color.green()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Etkinlik Başlatılamadı",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @bot.tree.command(name="event_sil", description="Sunucudaki etkinliği iptal eder.")
    @app_commands.describe(title="İptal edilecek etkinlik başlığı", reason="İptal sebebi")
    async def event_sil(interaction: Interaction, title: str, reason: str = "Etkinlik iptal edilmiştir."):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {"title": title, "reason": reason}
                async with session.post(f"{config.BACKEND_URL}/event_cancel", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="🚫 Etkinlik İptal Edildi",
                            description=f"**{title}** etkinliği iptal edildi.\nSebep: {reason}",
                            color=discord.Color.red()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Etkinlik İptal Edilemedi",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
