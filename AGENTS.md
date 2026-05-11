# Maulthboard

## Purpose
Maulthboard is an executive dashboard for a Windows Server 2025 homelab. Its main purpose is to serve as a daily hub to manage goals, organize ideas, monitor writing progress in Alyria5, and provide a unified entry point for other integrated homelab projects.

## Architecture & Technology Stack
- **Frontend & Backend Framework**: Pure Python via Reflex (No Node.js is required or desired).
- **Layout Model**: An infinite, zoomable canvas based on absolute positioning, primarily used to place and arrange "Idea Cards".
- **Visual Style**: "Cyber-Command Center". High-contrast, dark mode, neon accents, sleek borders, monospace fonts, and glassmorphism card effects.
- **Database**: SQLite (managed via Reflex's ORM, `SQLModel` / `SQLAlchemy`), used for storing positions of Idea Cards and statistics for tracked projects.
- **Background Processes**:
  - **The Watcher**: Integration with `watchdog` to monitor specific Windows file paths recursively (e.g., `C:\Alyria5\data\users\Maulth\projects`). It detects file changes to update the corresponding "Activity" statistics on Project Cards within the dashboard.
  - **Hardware Monitoring**: Integration with `nvidia-ml-py` to power a VRAM monitor widget tracking Tesla GPUs.
