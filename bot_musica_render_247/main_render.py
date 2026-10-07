import os
import main
from keep_alive import keep_alive

# Iniciar servidor Flask para evitar el modo sleep de Render
keep_alive()

# Iniciar bot de Discord
if __name__ == "__main__":
    if main.TOKEN:
        main.bot.run(main.TOKEN)
    else:
        print("❌ Error: Agrega tu DISCORD_TOKEN en las variables de entorno.")
