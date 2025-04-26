from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):

    @bot.tree.command(name="kullanıcı", description="Bir kullanıcının toplam aktif süresini gösterir.")
    @app_commands.describe(discord_id="Kullanıcının Discord ID'si")
    async def kullanıcı(interaction: Interaction, discord_id: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                async with session.get(f"{config.BACKEND_URL}/playerinfo/{discord_id}", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        total_time = data.get("total_playtime", "Bilinmiyor")
                        embed = discord.Embed(
                            title="🕒 Kullanıcı Oyun Süresi",
                            description=f"**{discord_id}** kullanıcısının toplam aktif süresi: `{total_time}`",
                            color=discord.Color.purple()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Kullanıcı Bilgisi Bulunamadı",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)

    @bot.tree.command(name="envanter", description="Bir kullanıcının envanterini gösterir.")
    @app_commands.describe(user_id="Kullanıcının ID'si")
    async def envanter(interaction: Interaction, user_id: str):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                async with session.get(f"{config.BACKEND_URL}/inventory/{user_id}", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get("items", [])

                        if not items:
                            desc = "Bu kullanıcının envanteri boş."
                        else:
                            desc = "\n".join([f"• {item['name']} x{item['count']}" for item in items])

                        embed = discord.Embed(
                            title="🎒 Kullanıcı Envanteri",
                            description=desc,
                            color=discord.Color.orange()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Envanter Bilgisi Bulunamadı",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
