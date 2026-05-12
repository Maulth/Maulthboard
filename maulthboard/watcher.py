import os
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from sqlmodel import Session, select, create_engine
import reflex as rx

from .models import ProjectStat

# We need an engine to write to DB from a separate thread outside of Reflex state
db_url = "sqlite:///reflex.db"
engine = create_engine(db_url)

WATCH_PATH = r"C:\Alyria5\data\users\Maulth\projects"

class ProjectActivityHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            self._update_activity(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._update_activity(event.src_path)

    def _update_activity(self, file_path):
        try:
            # Try to extract project name from the subfolder immediately under WATCH_PATH
            # e.g., C:\...\projects\ProjectA\file.txt -> ProjectA
            rel_path = os.path.relpath(file_path, WATCH_PATH)
            parts = Path(rel_path).parts

            if not parts:
                return

            project_name = parts[0]

            with Session(engine) as session:
                stat = session.exec(select(ProjectStat).where(ProjectStat.name == project_name)).first()
                if stat:
                    stat.activity += 1
                else:
                    # Create a new project stat tracking
                    project_path = os.path.join(WATCH_PATH, project_name)
                    stat = ProjectStat(name=project_name, path=project_path, activity=1)

                session.add(stat)
                session.commit()
                print(f"[{project_name}] Activity updated: {stat.activity}")
        except Exception as e:
            print(f"Error updating project activity: {e}")

_observer = None

def start_watcher():
    global _observer
    global WATCH_PATH

    if _observer is not None:
        return # Already running

    # Check if path exists, fallback to a dummy local path for testing if not on the Windows Server
    watch_dir = WATCH_PATH
    if not os.path.exists(watch_dir):
        print(f"Warning: {WATCH_PATH} does not exist. Falling back to local './dummy_projects'.")
        watch_dir = "./dummy_projects"
        os.makedirs(watch_dir, exist_ok=True)
        # Update global for the handler to calculate relative paths correctly
        WATCH_PATH = os.path.abspath(watch_dir)

    event_handler = ProjectActivityHandler()
    _observer = Observer()
    _observer.schedule(event_handler, watch_dir, recursive=True)

    # Run observer in a daemon thread so it doesn't block Reflex
    def run_observer():
        _observer.start()
        try:
            while _observer.is_alive():
                _observer.join(1)
        except Exception as e:
            pass
        finally:
            _observer.stop()
            _observer.join()

    watcher_thread = threading.Thread(target=run_observer, daemon=True)
    watcher_thread.start()
    print(f"Watcher started on: {WATCH_PATH}")

def stop_watcher():
    global _observer
    if _observer:
        _observer.stop()
        _observer.join()
        _observer = None
        print("Watcher stopped.")
