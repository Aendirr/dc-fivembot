from discord import app_commands, Interaction
from discord.ext import commands
import discord

def setup_commands(bot: commands.Bot):

    @bot.tree.command(name="dcbanla", description="Discord sunucusundan bir kullanıcıyı banlar.")
    @app_commands.describe(user="Banlanacak kullanıcı", reason="Ban sebebi")
    async def dcbanla(interaction: Interaction, user: discord.Member, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()
        try:
            await user.ban(reason=reason)
            embed = discord.Embed(
                title="⛔ Kullanıcı Banlandı",
                description=f"**{user}** sunucudan banlandı.\nSebep: {reason}",
                color=discord.Color.red()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Ban Başarısız",
                description=str(e),
                color=discord.Color.red()
            )
        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="dckick", description="Discord sunucusundan bir kullanıcıyı atar.")
    @app_commands.describe(user="Atılacak kullanıcı", reason="Atılma sebebi")
    async def dckick(interaction: Interaction, user: discord.Member, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()
        try:
            await user.kick(reason=reason)
            embed = discord.Embed(
                title="👢 Kullanıcı Atıldı",
                description=f"**{user}** sunucudan atıldı.\nSebep: {reason}",
                color=discord.Color.orange()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Kick Başarısız",
                description=str(e),
                color=discord.Color.red()
            )
        await interaction.followup.send(embed=embed)

    @bot.tree.command(name="chatclear", description="Belirli sayıda mesajı siler.")
    @app_commands.describe(amount="Silinecek mesaj sayısı (1-100)")
    async def chatclear(interaction: Interaction, amount: int):
        await interaction.response.defer()
        if amount < 1 or amount > 100:
            await interaction.followup.send(content="❌ 1 ile 100 arasında bir sayı girmelisin!", ephemeral=True)
            return
        try:
            await interaction.channel.purge(limit=amount)
            embed = discord.Embed(
                title="🧹 Sohbet Temizlendi",
                description=f"{amount} mesaj silindi.",
                color=discord.Color.blue()
            )
        except Exception as e:
            embed = discord.Embed(
                title="❌ Temizlik Başarısız",
                description=str(e),
                color=discord.Color.red()
            )
        await interaction.followup.send(embed=embed)
