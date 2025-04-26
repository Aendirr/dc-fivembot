from discord import app_commands, Interaction
from discord.ext import commands, tasks
import discord
import config
import asyncio
from datetime import datetime, timedelta

# Ceza bitiş sürelerini takip edeceğiz
active_punishments = {}

def setup_commands(bot: commands.Bot):

    @bot.tree.command(name="punish", description="Kullanıcıya süreli ceza verir.")
    @app_commands.describe(user="Cezalandırılacak kullanıcı", duration="Ceza süresi (2g, 3g, 1h, 1a, perma)", reason="Ceza sebebi")
    async def punish(interaction: Interaction, user: discord.Member, duration: str, reason: str = "Sebep belirtilmedi"):
        await interaction.response.defer()

        role_id = config.PUNISH_ROLES.get(duration.lower())
        if not role_id:
            await interaction.followup.send(content="❌ Geçerli bir süre belirtmelisin! (2g, 3g, 1h, 1a, perma)", ephemeral=True)
            return

        role = interaction.guild.get_role(role_id)
        if not role:
            await interaction.followup.send(content="❌ Ceza rolü bulunamadı. Lütfen config.py dosyasını kontrol edin.", ephemeral=True)
            return

        try:
            await user.add_roles(role, reason=reason)
            
            # Embed oluştur
            embed = discord.Embed(
                title="🔒 Ceza Verildi",
                description=f"**{user}** kullanıcısına `{duration}` süresiyle ceza verildi.\nSebep: {reason}",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Ceza veren: {interaction.user}")

            # Ceza log kanalına gönder
            log_channel = interaction.guild.get_channel(config.PUNISH_LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(embed=embed)

            await interaction.followup.send(embed=embed)

            # Eğer perma değilse süre başlat
            if duration.lower() != "perma":
                end_time = get_end_time(duration)
                active_punishments[user.id] = (role_id, end_time)
        except Exception as e:
            await interaction.followup.send(content=f"❌ Hata oluştu: {str(e)}", ephemeral=True)

    # Ceza takip döngüsü
    @tasks.loop(minutes=1)
    async def check_punishments():
        now = datetime.utcnow()
        to_remove = []

        for user_id, (role_id, end_time) in active_punishments.items():
            if now >= end_time:
                guild = discord.utils.get(bot.guilds, id=config.GUILD_ID)
                member = guild.get_member(user_id)
                if member:
                    role = guild.get_role(role_id)
                    if role:
                        await member.remove_roles(role)
                        print(f"[INFO] {member} kullanıcısından ceza kaldırıldı.")

                        # Log
                        log_channel = guild.get_channel(config.PUNISH_LOG_CHANNEL_ID)
                        if log_channel:
                            await log_channel.send(f"🔓 **{member}** kullanıcısının ceza süresi dolduğu için rolü kaldırıldı.")

                to_remove.append(user_id)

        for user_id in to_remove:
            del active_punishments[user_id]

    check_punishments.start()

def get_end_time(duration_str):
    now = datetime.utcnow()
    if duration_str == "2g":
        return now + timedelta(days=2)
    if duration_str == "3g":
        return now + timedelta(days=3)
    if duration_str == "1h":
        return now + timedelta(weeks=1)
    if duration_str == "1a":
        return now + timedelta(days=30)
    return now + timedelta(days=9999)  # perma gibi (aslında kaldırmıyoruz)
