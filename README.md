# API-based Weather Fetcher CLI

A simple yet robust command-line interface (CLI) tool built with Python to fetch and display real-time weather data from the OpenWeatherMap API.

## Features

-   **Real-Time Data:** Fetches current temperature, humidity, and weather conditions for any city.
-   **Command-Line Interface:** Easy-to-use interface powered by Python's `argparse`.
-   **Unit Conversion:** Supports both Metric (°C) and Imperial (°F) units.
-   **Secure API Key Management:** Uses a `.env` file to keep your API key safe and out of the source code.
-   **Smart Caching:** Implements a local caching system to reduce redundant API calls and improve performance.
-   **Installable Package:** Packaged for easy installation with `pip`.

## Requirements

-   Python 3.7+

## Installation & Configuration

Follow these steps to set up and run the project locally.

1.  **Clone the Repository (Optional):**
    If you have this project in a Git repository, clone it first.
    ```bash
    git clone https://your-repository-url/weather_cli.git
    cd weather_cli
    ```

2.  **Create and Activate a Virtual Environment:**
    It is highly recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the Project:**
    Install the CLI tool and its dependencies in editable mode. This allows you to make changes to the code without reinstalling.
    ```bash
    pip install -e .
    ```

4.  **Set Up Your API Key:**
    The tool requires an API key from [OpenWeatherMap](https://openweathermap.org/api).
    -   Create a file named `.env` in the root of the project directory.
    -   Add your API key to this file in the following format:
    ```
    OPENWEATHER_API_KEY=your_actual_api_key_here
    ```

## Usage

Once installed, you can use the `weather-cli` command directly from your terminal.

### Basic Usage

Provide a city name to get the weather in the default metric units (Celsius).

```bash
weather-cli "New York"
