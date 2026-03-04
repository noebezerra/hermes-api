from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.grafana import router as grafana_router
from app.core.config import get_settings

import textwrap

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title=get_settings().app_name,
)
app.mount("/static", StaticFiles(directory="static"), name="static")
description=f"""
    <p align="center">
        <img src="./static/logo.png" alt="Hermes API" size="50px" />
    </p>

    <p align="center">
        <em>Hermes API, uma API mensageira</em>
    </p>
"""

app.description = textwrap.dedent(description)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(grafana_router, prefix="/grafana", tags=["grafana"])
