# WeatherLab

This project provides simple scripts for downloading hurricane track CSV files from DeepMind's Weather Lab and visualizing them on a map.

## Getting Started

1. Install dependencies:
   ```bash
   pip install flask requests beautifulsoup4 selenium webdriver-manager
   ```
   A Chrome browser is required for the downloader script.

2. Set your Google credentials as environment variables so Selenium can log in:
   ```bash
   export GOOGLE_EMAIL="you@example.com"
   export GOOGLE_PASSWORD="your-password"
   ```

3. Download the latest CSV:
   ```bash
   python weather-map/scripts/download_latest.py
   ```
   The file is saved in `weather-map/data/` with a date-based filename.

4. Start the map server:
   ```bash
   python weather-map/app.py
   ```
   Open `http://localhost:5000/` in your browser to view the Leaflet map.

CSV files placed in `weather-map/data/` are automatically listed and displayed on the map.
