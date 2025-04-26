from discord import app_commands, Interaction
from discord.ext import commands
import discord
import aiohttp
import config

def setup_commands(bot: commands.Bot):
    @bot.tree.command(name="item", description="Bir kullanıcıya item verir.")
    @app_commands.describe(user_id="Kullanıcının ID'si", item_code="Verilecek item kodu", count="Miktar")
    async def item(interaction: Interaction, user_id: str, item_code: str, count: int):
        await interaction.response.defer()
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
                payload = {
                    "user_id": user_id,
                    "item_code": item_code,
                    "count": count
                }
                async with session.post(f"{config.BACKEND_URL}/giveitem", headers=headers, json=payload) as response:
                    if response.status == 200:
                        embed = discord.Embed(
                            title="🎁 Item Verildi",
                            description=f"**{user_id}** kullanıcısına `{item_code}` iteminden `{count}` adet verildi.",
                            color=discord.Color.green()
                        )
                    else:
                        embed = discord.Embed(
                            title="❌ Item Verilemedi",
                            description=f"Hata Kodu: {response.status}",
                            color=discord.Color.red()
                        )
                    await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
            await interaction.followup.send(embed=embed)
