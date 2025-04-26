import discord
from discord.ext import commands
import config
from commands import ip_command, sunucu_command, admin_command
from commands.yönetim import sunucures_command, ban_kick_warn_commands, item_command, itemsil_command, event_commands, kullanici_envanter_command, dc, punish# diğerleri sırayla gelecek

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

class AendirBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, intents=intents)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=discord.Object(id=config.GUILD_ID))
        await self.tree.sync(guild=discord.Object(id=config.GUILD_ID))

        # Komutları buraya ekle
        ip_command.setup_commands(self)
        sunucu_command.setup_commands(self)
        admin_command.setup_commands(self)
        sunucures_command.setup_commands(self)
        ban_kick_warn_commands.setup_commands(self)
        item_command.setup_commands(self)
        itemsil_command.setup_commands(self)
        event_commands.setup_commands(self)
        kullanici_envanter_command.setup_commands(self)
        dc.setup_commands(self)
        punish.setup_commands(self)
        print("✅ Komutlar yüklendi.")

bot = AendirBot()
@bot.event
async def on_ready():
    print(f"✅ {bot.user} olarak giriş yapıldı.")

    bot.tree.copy_global_to(guild=discord.Object(id=config.GUILD_ID))
    synced = await bot.tree.sync(guild=discord.Object(id=config.GUILD_ID))
    print(f"🔁 {len(synced)} komut sunucuya sync edildi.")
    for cmd in synced:
        print(f"🔗 /{cmd.name} - {cmd.description}")

bot.run(config.DISCORD_TOKEN)
