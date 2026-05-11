import reflex as rx

class IdeaCard(rx.Model, table=True):
    title: str
    content: str
    x_pos: int = 0
    y_pos: int = 0

class ProjectStat(rx.Model, table=True):
    name: str
    path: str
    activity: int = 0
