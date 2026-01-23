# NeuroWeather

NeuroWeather is an LLM-based weather assistant that integrates real-time meteorological data with historical climate analysis.

The system utilizes a RAG-like architecture to bridge natural language queries with precise data from the Open-Meteo API using Pythonic tools.

## Features

- **Intent Recognition:** Parses user queries using Llama 3 (via Groq) to understand context and intent.
- **Context Awareness:** Maintains conversation state (location and date) across multiple turns.
- **Historical Analysis:** Searches for past weather events (last snow, rain, wind, heatwaves, frost).
- **Climate Records:** Retrieves all-time weather records since 1960.
- **Guardrails:** Automatically filters out non-weather related queries to save API costs.
- **Dual Interface:** Supports both Terminal (CLI) and Web Interface (Gradio).

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MikolajSynak/NeuroWeather.git](https://github.com/MikolajSynak/NeuroWeather.git
   cd NeuroWeather
   
2. **Create and activate a virtual environment:**

   ```bash
   # Windows:
   python -m venv .venv
   .venv\Scripts\activate
   # Linux/Mac:
   python3 -m venv .venv
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
   # or explicitly:
   python main.py --mode cli
    ```
   
5. **Run the script with a User Interface**
   ```bash
   python main.py --mode web
   # To see all available boot options:
   python main.py --help
   ```
   

## Architecture
main.py - Entry Point & Orchestration

core/ - Main controller and state management.

services/ - Business logic domain (Weather Service, Location Tool).

interfaces/ - Presentation Layer (CLI & Web adapters)

data/ - Raw data access layer (OpenMeteo API wrappers).

settings/ - Configuration, prompts, and static data.



###### Powered by Groq & Open-Meteo.
