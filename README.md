# Valorant Tournament Overlay System

A professional overlay system for Valorant tournament streams, featuring real-time updates and a clean, esports-inspired design.

## Features

-  **Scene Management**: Switch between different scenes (Intro, Match, Scoreboard, Winner)
-  **Team Management**: Update team names, logos, and scores in real-time
-  **Player Stats**: Track player statistics including kills, deaths, and assists
-  **Match Timer**: Keep track of match duration
-  **Killfeed**: Real-time kill notifications
-  **Responsive Design**: Works with standard streaming resolutions (1920x1080)
-  **Real-time Updates**: Changes appear instantly in OBS

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Open the control panel in your browser:
   ```
   http://localhost:8000
   ```

3. Add the overlay to OBS:
   - In OBS, add a new Browser Source
   - Set the URL to: `http://localhost:8000/overlay`
   - Set the width to 1920 and height to 1080
   - Check "Shutdown source when not visible" and "Refresh browser when scene becomes active"

## Control Panel

The control panel provides an intuitive interface to manage your tournament:

- **Scene Selection**: Switch between different scenes (Intro, Match, Scoreboard, Winner)
- **Team Management**: Update team names, logos, and scores
- **Player Stats**: Update player information and statistics
- **Match Timer**: Control the match timer
- **Killfeed**: Add kill events to the feed

## Customization

You can customize the appearance by modifying the CSS in `templates/overlay.html`. The design uses Tailwind CSS for easy customization.

## Project Structure

- `main.py`: Main application file with FastAPI server and WebSocket support
- `templates/`: Contains HTML templates for the control panel and overlay
  - `control_panel.html`: Control panel interface
  - `overlay.html`: The overlay that appears in OBS
- `static/`: Static files (CSS, JS, images)
- `data/`: Stores the overlay data in `overlay_data.json`

## License

This project is open source and available under the MIT License.

## Credits

- Icons by [Font Awesome](https://fontawesome.com/)
- Styling with [Tailwind CSS](https://tailwindcss.com/)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
