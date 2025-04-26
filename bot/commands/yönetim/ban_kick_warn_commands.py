from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):
    
    @bot.tree.command(name="banla", description="Kullanıcıyı sunucudan banlar.")
    @app_commands.describe(user_id="Kullanıcının ID'si", reason="Ban sebebi")
    async def banla(interaction: Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {"user_id": user_id, "reason": reason}
                async with session.post(f"{config.BACKEND_URL}/ban", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="⛔ Kullanıcı Banlandı",
                            description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                            color=discord.Color.red()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Ban Başarısız",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @bot.tree.command(name="kick", description="Kullanıcıyı sunucudan atar.")
    @app_commands.describe(user_id="Kullanıcının ID'si", reason="Atılma sebebi")
    async def kick(interaction: Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {"user_id": user_id, "reason": reason}
                async with session.post(f"{config.BACKEND_URL}/kick", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="👢 Kullanıcı Atıldı",
                            description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                            color=discord.Color.orange()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Kick Başarısız",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @bot.tree.command(name="warn", description="Kullanıcıya uyarı gönderir.")
    @app_commands.describe(user_id="Kullanıcının ID'si", reason="Uyarı sebebi")
    async def warn(interaction: Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {"user_id": user_id, "reason": reason}
                async with session.post(f"{config.BACKEND_URL}/warn", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="⚠️ Uyarı Gönderildi",
                            description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                            color=discord.Color.yellow()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Uyarı Başarısız",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
