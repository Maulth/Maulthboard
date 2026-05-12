"""Maulthboard - Executive Dashboard."""

import reflex as rx
from rxconfig import config
from sqlmodel import select

from .models import IdeaCard, ProjectStat
from .watcher import start_watcher

class WatcherState(rx.State):
    """State to periodically fetch project stats."""
    projects: list[ProjectStat] = []

    def fetch_stats(self):
        with rx.session() as session:
            self.projects = session.exec(select(ProjectStat).order_by(ProjectStat.activity.desc())).all()

    @rx.event(background=True)
    async def poll_stats(self):
        import asyncio
        while True:
            async with self:
                self.fetch_stats()
            yield
            await asyncio.sleep(2) # Poll every 2 seconds

class CanvasState(rx.State):
    """The state for the interactive canvas and idea cards."""
    cards: list[IdeaCard] = []

    # State for new card modal
    new_card_title: str = ""
    new_card_content: str = ""
    is_modal_open: bool = False

    # Edit State
    editing_card_id: int = -1
    edit_card_title: str = ""
    edit_card_content: str = ""

    def open_edit_modal(self, card_id: int):
        with rx.session() as session:
            card = session.exec(select(IdeaCard).where(IdeaCard.id == card_id)).first()
            if card:
                self.editing_card_id = card.id
                self.edit_card_title = card.title
                self.edit_card_content = card.content

    def close_edit_modal(self):
        self.editing_card_id = -1

    def save_edit(self):
        if self.editing_card_id != -1:
            with rx.session() as session:
                card = session.exec(select(IdeaCard).where(IdeaCard.id == self.editing_card_id)).first()
                if card:
                    card.title = self.edit_card_title
                    card.content = self.edit_card_content
                    session.add(card)
                    session.commit()
            self.editing_card_id = -1
            self.load_cards()

    def set_edit_card_title(self, val: str):
        self.edit_card_title = val

    def set_edit_card_content(self, val: str):
        self.edit_card_content = val

    def set_new_card_title(self, val: str):
        self.new_card_title = val

    def set_new_card_content(self, val: str):
        self.new_card_content = val

    def load_cards(self):
        with rx.session() as session:
            self.cards = session.exec(select(IdeaCard)).all()

    def add_card(self):
        with rx.session() as session:
            session.add(
                IdeaCard(
                    title=self.new_card_title,
                    content=self.new_card_content,
                    x_pos=100, # Default starting pos
                    y_pos=100,
                )
            )
            session.commit()
        self.new_card_title = ""
        self.new_card_content = ""
        self.is_modal_open = False
        self.load_cards()

    def toggle_modal(self):
        self.is_modal_open = not self.is_modal_open


def idea_card(card: IdeaCard) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.heading(card.title, size="4", color="#00ffcc", font_family="monospace"),
                rx.spacer(),
                rx.icon(
                    "pencil",
                    color="#00ffcc",
                    cursor="pointer",
                    on_click=CanvasState.open_edit_modal(card.id),
                    size=16
                ),
            ),
            rx.text(card.content, color="#e0e0e0", font_family="monospace"),
        ),
        position="absolute",
        left=f"{card.x_pos}px",
        top=f"{card.y_pos}px",
        width="250px",
        padding="15px",
        background_color="rgba(10, 10, 10, 0.8)",
        backdrop_filter="blur(10px)",
        border="1px solid #00ffcc",
        box_shadow="0 0 10px rgba(0, 255, 204, 0.5)",
    )

def project_card(stat: ProjectStat) -> rx.Component:
    return rx.hstack(
        rx.text(stat.name, color="#00ffcc", font_family="monospace", font_weight="bold"),
        rx.spacer(),
        rx.badge(
            f"ACT: {stat.activity}",
            color_scheme="cyan",
            variant="outline",
        ),
        width="100%",
        padding="10px",
        background_color="rgba(10, 10, 10, 0.8)",
        border="1px solid #333",
        border_left="3px solid #00ffcc",
        margin_bottom="10px",
    )


def index() -> rx.Component:
    # "Cyber-Command Center" dark theme base layout
    return rx.box(
        rx.hstack(
            rx.heading("MAULTHBOARD", size="9", color="#00ffcc", font_family="monospace"),
            rx.spacer(),
            rx.button(
                "NEW INTEL",
                on_click=CanvasState.toggle_modal,
                background_color="#ff00ff",
                color="white",
                font_family="monospace",
                border="1px solid #ff00ff",
                box_shadow="0 0 5px rgba(255, 0, 255, 0.5)",
            ),
            width="100%",
            padding_bottom="20px",
        ),
        rx.text("SYSTEM ACTIVE // AWAITING COMMAND...", color="#ff00ff", font_family="monospace", padding_bottom="10px"),

        # New Card Modal
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("ENTER NEW IDEA INTEL"),
                rx.vstack(
                    rx.input(
                        placeholder="Title...",
                        value=CanvasState.new_card_title,
                        on_change=CanvasState.set_new_card_title,
                    ),
                    rx.text_area(
                        placeholder="Content...",
                        value=CanvasState.new_card_content,
                        on_change=CanvasState.set_new_card_content,
                    ),
                    rx.hstack(
                        rx.button("CANCEL", on_click=CanvasState.toggle_modal, color_scheme="gray"),
                        rx.button("SUBMIT", on_click=CanvasState.add_card, color_scheme="cyan"),
                    ),
                ),
            ),
            open=CanvasState.is_modal_open,
        ),

        # Edit Card Modal
        rx.dialog.root(
            rx.dialog.content(
                rx.dialog.title("EDIT INTEL"),
                rx.vstack(
                    rx.input(
                        placeholder="Title...",
                        value=CanvasState.edit_card_title,
                        on_change=CanvasState.set_edit_card_title,
                    ),
                    rx.text_area(
                        placeholder="Content...",
                        value=CanvasState.edit_card_content,
                        on_change=CanvasState.set_edit_card_content,
                    ),
                    rx.hstack(
                        rx.button("CANCEL", on_click=CanvasState.close_edit_modal, color_scheme="gray"),
                        rx.button("SAVE", on_click=CanvasState.save_edit, color_scheme="cyan"),
                    ),
                ),
            ),
            open=CanvasState.editing_card_id != -1,
        ),

        rx.hstack(
            # Left panel: Project Activity
            rx.box(
                rx.heading("ALYRIA5_PROJECT_STATUS", size="4", color="#ff00ff", font_family="monospace", margin_bottom="15px"),
                rx.foreach(WatcherState.projects, project_card),
                width="25%",
                height="80vh",
                padding="15px",
                border="1px solid #333",
                background_color="rgba(15, 15, 15, 0.9)",
                overflow_y="auto",
            ),

            # Right panel: Canvas container
            rx.box(
                rx.box(
                    rx.foreach(CanvasState.cards, idea_card),
                    width="100%",
                    min_height="100%",
                    position="relative",
                    background_color="#0a0a0a",
                    background_image="radial-gradient(circle, #333 1px, transparent 1px)",
                    background_size="50px 50px", # Grid dot pattern
                ),
                width="75%",
                height="80vh",
                overflow="auto",
                border="1px solid #333",
            ),
            width="100%",
            spacing="4",
        ),

        background_color="#000000",
        min_height="100vh",
        width="100vw",
        padding="20px",
        on_mount=[CanvasState.load_cards, WatcherState.poll_stats],
    )

# Start watcher outside of component render to avoid blocking SSR
start_watcher()

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        has_background=True,
        radius="none",
        accent_color="cyan",
    )
)
app.add_page(index, title="Maulthboard | Command Center")
