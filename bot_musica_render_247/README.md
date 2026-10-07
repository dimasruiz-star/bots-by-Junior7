# Bot de Música para Discord (Anti-Sleep para Render 24/7)

## 🚀 Cómo desplegar en Render gratis:

1. Extrae los archivos de este ZIP.
2. Sube los archivos a un repositorio de **GitHub**.
3. Ve a **Render.com** -> **New +** -> **Web Service**.
4. Conecta tu repositorio de GitHub.
5. Configura los comandos:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main_render.py`
6. En **Environment Variables** agrega:
   - `DISCORD_TOKEN`: Tu token de Discord.
7. Para evitar que Render suspenda el bot tras inactividad, copia la URL que te asigna Render y agrégala en [UptimeRobot.com](https://uptimerobot.com) (monitor HTTP gratis cada 5 min).
