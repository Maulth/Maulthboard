import reflex as rx

class State(rx.State):
    @rx.event(background=True)
    async def poll_stats(self):
        pass
