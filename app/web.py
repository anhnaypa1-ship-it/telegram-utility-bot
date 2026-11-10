import logging
from aiohttp import web

logger = logging.getLogger(__name__)

async def health_check(request: web.Request) -> web.Response:
    """
    Endpoint phản hồi kiểm tra sức khỏe hệ thống.
    Dùng cho Render và cron-job.org ping định kỳ để giữ bot luôn thức.
    """
    return web.json_response({
        "status": "healthy",
        "service": "telegram-utility-bot",
        "uptime": "active"
    })

def create_web_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/health", health_check)
    return app

async def start_web_server(port: int):
    app = create_web_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    logger.info(f"🌐 Web Server sẵn sàng tại cổng {port} (đường dẫn /health)")
    await site.start()
    return runner
