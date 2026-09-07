# ASH // System Monitor

A cyberpunk-inspired local system monitoring dashboard built with Python, JavaScript, HTML, CSS, and `psutil`.

It displays live:

- CPU usage
- RAM usage
- Disk usage
- Network upload/download activity
- Hostname
- Operating system
- Local IP address
- Process count
- System uptime

## Screenshot

Run the project and add your own screenshot here:

```md
![Dashboard Screenshot](screenshot.png)
```

## Tech Stack

- Python 3
- `psutil`
- HTML5
- CSS3
- Vanilla JavaScript
- Python `http.server`

## Setup

Clone the repository:

```bash
git clone https://github.com/ashlinculpepper01-sketch/ash-system-monitor.git
cd ash-system-monitor
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:8080
```

## Why I Built It

I wanted a lightweight way to visualize system health while practicing Python automation, operating-system telemetry, APIs, and frontend development.

## Possible Upgrades

- Process viewer
- Temperature monitoring
- Historical graphs
- Exportable reports
- Dark/light themes
- Remote machine monitoring
- Authentication
- Alerts when CPU/RAM/disk usage gets too high

## Security Note

The server binds to `127.0.0.1`, so the dashboard is only accessible from the local computer by default.

## License

MIT
