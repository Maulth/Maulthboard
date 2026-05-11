"""Maulthboard - Executive Dashboard."""

import reflex as rx
from rxconfig import config

from .models import IdeaCard, ProjectStat

class State(rx.State):
    """The app state."""
    pass

def index() -> rx.Component:
    # "Cyber-Command Center" dark theme base layout
    return rx.box(
        rx.heading("MAULTHBOARD", size="9", color="#00ffcc", font_family="monospace"),
        rx.text("INITIALIZING SYSTEM...", color="#ff00ff", font_family="monospace"),
        # Base container for the infinite zoomable canvas
        rx.box(
            width="100vw",
            height="100vh",
            position="relative",
            overflow="hidden",
            background_color="#0a0a0a",
        ),
        background_color="#000000",
        min_height="100vh",
        width="100vw",
        padding="20px",
    )

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="none",
        accent_color="cyan",
    )
)
app.add_page(index, title="Maulthboard | Command Center")
