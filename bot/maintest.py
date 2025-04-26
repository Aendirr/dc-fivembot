import discord
from discord import app_commands
from discord.ext import commands
import config
import servercomp
import aiohttp  

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=config.GUILD_ID))
        print("✅ Slash komutları sync edildi.")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"✅ {bot.user} olarak giriş yapıldı.")

    bot.tree.copy_global_to(guild=discord.Object(id=config.GUILD_ID))
    synced = await bot.tree.sync(guild=discord.Object(id=config.GUILD_ID))
    print(f"🔁 {len(synced)} komut sunucuya sync edildi.")
    for cmd in synced:
        print(f"🔗 /{cmd.name} - {cmd.description}")


# --- /ip Slash Komutu ---
@bot.tree.command(name="ip", description="Sunucuya bağlantı linki gönderir.")
async def ip(interaction: discord.Interaction):
    embed = discord.Embed(title="Sunucuya Bağlan", description="Aşağıdaki butona tıklayarak bağlanabilirsin.", color=discord.Color.green())
    view = discord.ui.View()
    button = discord.ui.Button(label="Bağlan", url=config.IP_URL)
    view.add_item(button)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)


# --- /sunucu Slash Komutu ---
@bot.tree.command(name="sunucu", description="Sunucunun özelliklerini ve açıklamasını gösterir.")
async def sunucu(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🎮 Sunucu Bilgileri",
        description=servercomp.SERVER_DESCRIPTION,
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)

# --- /admin Slash Komutu ---
@bot.tree.command(name="admin", description="Aktif admin ekibini listeler.")
async def admin(interaction: discord.Interaction):
    # Şu anlık dummy liste
    active_admins = [
        "👮‍♂️ Admin1",
        "👮 Admin2",
        "👩‍✈️ Admin3"
    ]

    embed = discord.Embed(
        title="👮‍♂️ Aktif Adminler",
        description="\n".join(active_admins),
        color=discord.Color.gold()
    )
    await interaction.response.send_message(embed=embed, ephemeral=False)

# --- /sunucures Slash Komutu ---
@bot.tree.command(name="sunucures", description="Sunucuyu yeniden başlatır (Admin komutu).")
async def sunucures(interaction: discord.Interaction):
    await interaction.response.defer()  # İşlem süreceği için defer edelim

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            async with session.post(f"{config.BACKEND_URL}/restart", headers=headers) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="✅ Sunucu Yeniden Başlatılıyor...",
                        description="Lütfen birkaç dakika bekleyin. Sunucu restart işlemi başlatıldı.",
                        color=discord.Color.green()
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Sunucu Restart Başarısız",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                    await interaction.followup.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="❌ Sunucu Restart Başarısız",
            description=f"Bir hata oluştu: {str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="kullanıcı", description="Kullanıcının toplam aktif süresini gösterir.")
@app_commands.describe(discord_id="Oyuncunun Discord ID'si")
async def kullanıcı(interaction: discord.Interaction, discord_id: str):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            async with session.get(f"{config.BACKEND_URL}/playerinfo/{discord_id}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    total_time = data.get("total_playtime", "Bilinmiyor")
                    
                    embed = discord.Embed(
                        title="🕒 Kullanıcı Oyun Süresi",
                        description=f"**{discord_id}** kullanıcısının toplam aktif süresi: `{total_time}`",
                        color=discord.Color.purple()
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Kullanıcı Bilgisi Bulunamadı",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                    await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Bir hata oluştu",
            description=f"{str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)


# --- /envanter Slash Komutu ---
@bot.tree.command(name="envanter", description="Bir kullanıcının envanterini listeler.")
@app_commands.describe(user_id="Oyuncunun Kullanıcı ID'si")
async def envanter(interaction: discord.Interaction, user_id: str):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            async with session.get(f"{config.BACKEND_URL}/inventory/{user_id}", headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    inventory_items = data.get("items", [])

                    if not inventory_items:
                        desc = "Bu kullanıcının envanteri boş."
                    else:
                        desc = "\n".join([f"• {item['name']} x{item['count']}" for item in inventory_items])

                    embed = discord.Embed(
                        title="🎒 Kullanıcı Envanteri",
                        description=desc,
                        color=discord.Color.orange()
                    )
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="❌ Envanter Bilgisi Bulunamadı",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                    await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="❌ Bir hata oluştu",
            description=f"{str(e)}",
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="banla", description="Belirtilen kullanıcıyı sunucudan banlar.")
@app_commands.describe(user_id="Kullanıcının ID'si", reason="Ban sebebi")
async def banla(interaction: discord.Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
            json_data = {"user_id": user_id, "reason": reason}
            async with session.post(f"{config.BACKEND_URL}/ban", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="⛔ Kullanıcı Banlandı",
                        description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                        color=discord.Color.red()
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Ban İşlemi Başarısız",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(embed=discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red()))

@bot.tree.command(name="kick", description="Kullanıcıyı sunucudan atar.")
@app_commands.describe(user_id="Kullanıcının ID'si", reason="Atılma sebebi")
async def kick(interaction: discord.Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
            json_data = {"user_id": user_id, "reason": reason}
            async with session.post(f"{config.BACKEND_URL}/kick", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="👢 Kullanıcı Atıldı",
                        description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                        color=discord.Color.orange()
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Kick İşlemi Başarısız",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(embed=discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red()))

@bot.tree.command(name="warn", description="Kullanıcıya uyarı gönderir.")
@app_commands.describe(user_id="Kullanıcının ID'si", reason="Uyarı sebebi")
async def warn(interaction: discord.Interaction, user_id: str, reason: str = "Sebep belirtilmedi"):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {config.BACKEND_API_TOKEN}"}
            json_data = {"user_id": user_id, "reason": reason}
            async with session.post(f"{config.BACKEND_URL}/warn", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="⚠️ Uyarı Gönderildi",
                        description=f"**ID:** `{user_id}`\n**Sebep:** {reason}",
                        color=discord.Color.yellow()
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Uyarı Gönderilemedi",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(embed=discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red()))

@bot.tree.command(name="item", description="Bir kullanıcıya item verir.")
@app_commands.describe(user_id="Kullanıcının ID'si", item_code="Item kodu", count="Verilecek miktar")
async def item(interaction: discord.Interaction, user_id: str, item_code: str, count: int):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            json_data = {
                "user_id": user_id,
                "item_code": item_code,
                "count": count
            }
            async with session.post(f"{config.BACKEND_URL}/giveitem", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="🎁 Item Verildi",
                        description=f"**{user_id}** adlı kullanıcıya `{item_code}` item'inden `{count}` adet verildi.",
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

@bot.tree.command(name="itemsil", description="Bir kullanıcıdan item siler.")
@app_commands.describe(user_id="Kullanıcının ID'si", item_code="Silinecek item kodu", count="Silinecek miktar")
async def itemsil(interaction: discord.Interaction, user_id: str, item_code: str, count: int):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            json_data = {
                "user_id": user_id,
                "item_code": item_code,
                "count": count
            }
            async with session.post(f"{config.BACKEND_URL}/removeitem", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="🗑️ Item Silindi",
                        description=f"**{user_id}** adlı kullanıcıdan `{item_code}` item’inden `{count}` adet silindi.",
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

@bot.tree.command(name="event", description="Sunucuya canlı etkinlik duyurusu gönderir.")
@app_commands.describe(title="Etkinlik başlığı", description="Etkinlik açıklaması")
async def event(interaction: discord.Interaction, title: str, description: str):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            json_data = {
                "title": title,
                "description": description
            }
            async with session.post(f"{config.BACKEND_URL}/event", headers=headers, json=json_data) as response:
                if response.status == 200:
                    embed = discord.Embed(
                        title="📢 Etkinlik Yayınlandı",
                        description=f"**{title}**\n{description}",
                        color=discord.Color.green()
                    )
                else:
                    embed = discord.Embed(
                        title="❌ Etkinlik Gönderilemedi",
                        description=f"Hata Kodu: {response.status}",
                        color=discord.Color.red()
                    )
                await interaction.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title="❌ Hata", description=str(e), color=discord.Color.red())
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="event_sil", description="Sunucudaki etkinliği iptal eder.")
@app_commands.describe(title="İptal edilecek etkinliğin başlığı", reason="İptal sebebi")
async def event_sil(interaction: discord.Interaction, title: str, reason: str = "Etkinlik iptal edilmiştir."):
    await interaction.response.defer()

    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {config.BACKEND_API_TOKEN}"
            }
            json_data = {
                "title": title,
                "reason": reason
            }
            async with session.post(f"{config.BACKEND_URL}/event_cancel", headers=headers, json=json_data) as response:
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



bot.run(config.DISCORD_TOKEN)
