# Don't Remove Credit @VJ_Botz  
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ

# Ask Doubt on telegram @KingVJ01

import sys, glob, importlib, logging, logging.config, pytz, asyncio
from pathlib import Path

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

from pyrogram import Client, idle 
from info import *
from typing import Union, Optional, AsyncGenerator
from Script import script 
from datetime import date, datetime 
from aiohttp import web
from plugins import web_server

from TechVJ.bot import TechVJBot, TechVJBackUpBot
from TechVJ.util.keepalive import ping_server
from TechVJ.bot.clients import initialize_clients

ppath = "plugins/*.py"
files = glob.glob(ppath)

TechVJBot.start()
TechVJBackUpBot.start()

loop = asyncio.get_event_loop()

# 🔒 Optional Watchdog to keep process alive silently
async def watchdog():
    while True:
        await asyncio.sleep(600)  # 10 min
        logging.info("Watchdog: still alive ✅")

async def start():
    print('\n')
    print('Initalizing Your Bot')

    bot_info = await TechVJBot.get_me()
    await initialize_clients()

    for name in files:
        try:
            with open(name) as a:
                patt = Path(a.name)
                plugin_name = patt.stem.replace(".py", "")
                plugins_dir = Path(f"plugins/{plugin_name}.py")
                import_path = "plugins.{}".format(plugin_name)
                spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
                load = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(load)
                sys.modules["plugins." + plugin_name] = load
                print("Tech VJ Imported => " + plugin_name)
        except Exception as e:
            logging.error(f"❌ Plugin load failed: {name} | {e}")

    if ON_HEROKU:
        asyncio.create_task(ping_server())  # Heroku keep-alive ping

    asyncio.create_task(watchdog())  # Optional watchdog

    me = await TechVJBot.get_me()
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    time = now.strftime("%H:%M:%S %p")

    await TechVJBot.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))

    # Start aiohttp web server with alive route
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0"
    port = int(PORT) if PORT else 8080
    await web.TCPSite(app, bind_address, port).start()

    await idle()

if __name__ == '__main__':
    try:
        loop.run_until_complete(start())
    except KeyboardInterrupt:
        logging.info('Service Stopped Bye 👋')
