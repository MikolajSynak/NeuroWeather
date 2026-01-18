# NeuroWeather

NeuroWeather is an LLM-based weather assistant that integrates real-time meteorological data with historical climate analysis.

The system utilizes a RAG-like architecture to bridge natural language queries with precise data from the Open-Meteo API using Pythonic tools.

## Features

- **Intent Recognition:** Parses user queries using Llama 3 (via Groq) to understand context.
- **Context Awareness:** Maintains conversation state (location and date) across multiple turns.
- **Historical Analysis:** Searches for past weather events (last snow, rain, wind, heatwaves, frost).
- **Climate Records:** Retrieves all-time weather records since 1960.
- **Guardrails:** Automatically filters out non-weather related queries to save API costs.

## Installation & usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/NeuroWeather.git](https://github.com/YOUR_USERNAME/NeuroWeather.git)
   cd NeuroWeather
   ```
   
2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   Bash
   pip install -r requirements.txt
   ```

##### Configuration: Create a .env file in the root directory and add your Groq API key:
   ```Ini, TOML
    GROQ_API_KEY=gsk_your_key_here
   ```

4. **Run the script:**
    ```bash
    python main.py
    ```

## Architecture
core/ - Main controller and state management.

services/ - Business logic domain (Weather Service, Location Tool).

data/ - Raw data access layer (OpenMeteo API wrappers).

settings/ - Configuration, prompts, and static data.

Powered by Groq & Open-Meteo.


### Step 4: Initialize Git and Push
Open your terminal in the `NeuroWeather` folder and run these commands one by one.

1.  **Initialize the repository:**
    ```bash
    git init
    ```

2.  **Add files to staging (Git will automatically ignore files from Step 1):**
    ```bash
    git add .
    ```

3.  **Commit your changes:**
    ```bash
    git commit -m "Initial commit: NeuroWeather V3 Architecture"
    ```

4.  **Connect to GitHub:**
    * Go to [github.com/new](https://github.com/new).
    * Name your repository `NeuroWeather`.
    * **Do not** check "Add a README file" (you already made one).
    * Click "Create repository".
    * Copy the commands from the section *"...or push an existing repository from the command line"* and run them. They usually look like this:

    ```bash
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/NeuroWeather.git
    git push -u origin main
    ```

**Done.** Your code is now live, documented, and secure.