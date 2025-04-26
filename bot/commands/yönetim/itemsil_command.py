from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="itemsil", description="Bir kullanıcıdan item siler.")
    @app_commands.describe(user_id="Kullanıcının ID'si", item_code="Silinecek item kodu", count="Miktar")
    async def itemsil(interaction: Interaction, user_id: str, item_code: str, count: int):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {
                    "user_id": user_id,
                    "item_code": item_code,
                    "count": count
                }
                async with session.post(f"{config.BACKEND_URL}/removeitem", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="🗑️ Item Silindi",
                            description=f"**{user_id}** kullanıcısından `{item_code}` iteminden `{count}` adet silindi.",
                            color=discord.Color.dark_red()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Item Silinemedi",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
