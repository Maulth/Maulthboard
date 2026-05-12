# Maulthboard

**Maulthboard** is an executive dashboard designed specifically for a Windows Server 2025 homelab. It serves as a centralized hub to organize chaotic workflows, manage goals, create and iterate on new ideas via an interactive canvas, and monitor writing progress in Alyria5.

Designed with a sleek "Cyber-Command Center" aesthetic, Maulthboard leverages high-contrast neon accents, monospace fonts, and a dark mode canvas to give you a powerful, command-line-inspired executive view.

---

## 🚀 Features

- **Pure Python Architecture**: Built entirely with [Reflex](https://reflex.dev/) (No Node.js/JavaScript required).
- **Interactive Idea Canvas**: A zoomable canvas space where you can create, edit, and organize "Idea Cards" to capture sudden inspiration.
- **The Watcher (Background Service)**: A recursive file monitor powered by `watchdog`. It tracks the file system (defaulting to `C:\Alyria5\data\users\Maulth\projects`) and automatically updates Project Cards with recent activity metrics.
- **Local SQLite Storage**: Fast, self-contained persistence utilizing `SQLModel`/`SQLAlchemy` under the hood.

*Upcoming/Planned:*
- *Hardware Monitoring: Real-time VRAM monitoring widgets for Tesla GPUs via `nvidia-ml-py`.*
- *Native Canvas Drag-and-Drop.*

---

## 🛠 Installation & Setup

### Prerequisites
- Python 3.10+
- (Optional but recommended) `uv` or `virtualenv` for environment management.

### 1. Clone the repository
```bash
git clone https://github.com/Maulth/Maulthboard.git
cd Maulthboard
```

### 2. Install dependencies
Install the required Python packages from the `requirements.txt` file.

Using standard pip:
```bash
pip install -r requirements.txt
```
*(Or, if you use `uv`, you can run `uv pip install -r requirements.txt`)*

### 3. Initialize the Database
Maulthboard uses SQLite. You need to create the database and apply the initial migrations to establish the `IdeaCard` and `ProjectStat` tables.

```bash
reflex db init
reflex db makemigrations
reflex db migrate
```

### 4. Run the Application
Start the Reflex server in development mode.

```bash
reflex run
```

The application will be available at `http://localhost:3000`.

---

## 📂 Configuration Notes

**The Watcher Pathing:**
By default, the watcher background service attempts to monitor the explicit Windows path: `C:\Alyria5\data\users\Maulth\projects`.

If you are running the application on a different operating system (like Linux) or the folder does not exist, the watcher will automatically fallback and generate a `./dummy_projects` directory inside the repository root to allow for localized testing without crashing the application.