import asyncio
import os
import sys
import traceback

from telegram.ext import ApplicationBuilder

async def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("NO_TOKEN")
        sys.exit(2)
    app = ApplicationBuilder().token(token).build()
    try:
        await app.initialize()
        print("APP_INITIALIZED")
    except Exception:
        print("INIT_FAILED")
        traceback.print_exc()
        sys.exit(1)
    finally:
        try:
            await app.stop()
        except Exception:
            pass

if __name__ == '__main__':
    asyncio.run(main())
