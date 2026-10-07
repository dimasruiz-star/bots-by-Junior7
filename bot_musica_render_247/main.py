import os
import discord
from discord.ext import commands
from discord import app_commands
import wavelink
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        node = wavelink.Node(
            uri="https://lava-v3.ajiehospitality.com:443", 
            password="https://discord.gg/ajiehospitality"
        )
        await wavelink.Pool.connect(nodes=[node], client=self)
        print("Sincronizando comandos Slash...")
        await self.tree.sync()

bot = MusicBot()

@bot.event
async def on_ready():
    print(f"✅ Bot de música activo en Render como: {bot.user}")
    activity = discord.Activity(type=discord.ActivityType.listening, name="/play")
    await bot.change_presence(status=discord.Status.online, activity=activity)

@bot.tree.command(name="play", description="Reproduce una canción o playlist.")
@app_commands.describe(busqueda="Nombre de la canción o enlace")
async def play(interaction: discord.Interaction, busqueda: str):
    if not interaction.user.voice:
        await interaction.response.send_message("❌ Debes estar en un canal de voz.", ephemeral=True)
        return

    await interaction.response.defer()
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc:
        vc = await interaction.user.voice.channel.connect(cls=wavelink.Player)

    tracks: wavelink.Search = await wavelink.Playable.search(busqueda)
    if not tracks:
        await interaction.followup.send("❌ No se encontraron resultados.")
        return

    track = tracks[0] if isinstance(tracks, list) else tracks.tracks[0]

    if vc.is_playing():
        await vc.queue.put_wait(track)
        embed = discord.Embed(
            title="📥 Añadido a la cola",
            description=f"[{track.title}]({track.uri}) - `{track.author}`",
            color=discord.Color.blue()
        )
        await interaction.followup.send(embed=embed)
    else:
        await vc.play(track)
        embed = discord.Embed(
            title="🎶 Reproduciendo ahora",
            description=f"[{track.title}]({track.uri}) - `{track.author}`",
            color=discord.Color.green()
        )
        await interaction.followup.send(embed=embed)

@bot.tree.command(name="pause", description="Pausa la canción actual.")
async def pause(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc and vc.is_playing():
        await vc.pause(True)
        await interaction.response.send_message("⏸️ Reproducción pausada.")
    else:
        await interaction.response.send_message("❌ No hay nada reproduciéndose.", ephemeral=True)

@bot.tree.command(name="resume", description="Reanuda la reproducción pausada.")
async def resume(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc and vc.is_paused():
        await vc.pause(False)
        await interaction.response.send_message("▶️ Reproducción reanudada.")
    else:
        await interaction.response.send_message("❌ El reproductor no está pausado.", ephemeral=True)

@bot.tree.command(name="skip", description="Pasa a la siguiente canción en la cola.")
async def skip(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc and vc.is_playing():
        await vc.skip()
        await interaction.response.send_message("⏭️ Canción saltada.")
    else:
        await interaction.response.send_message("❌ No hay ninguna canción en reproducción.", ephemeral=True)

@bot.tree.command(name="queue", description="Muestra la lista de canciones en espera.")
async def queue(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc or vc.queue.is_empty:
        await interaction.response.send_message("📜 La cola de reproducción está vacía.", ephemeral=True)
        return

    lista = ""
    for i, track in enumerate(vc.queue, start=1):
        lista += f"**{i}.** {track.title} - `{track.author}`\n"
        if i >= 10:
            lista += f"\n*...y {len(vc.queue) - 10} más en espera.*"
            break

    embed = discord.Embed(
        title="📜 Cola de Reproducción",
        description=lista,
        color=discord.Color.purple()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stop", description="Detiene la música y desconecta al bot.")
async def stop(interaction: discord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("⏹️ Música detenida.")
    else:
        await interaction.response.send_message("❌ El bot no está en un canal de voz.", ephemeral=True)

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: Agrega tu DISCORD_TOKEN en el archivo .env")
