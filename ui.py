import gradio as gr
import logging
from dotenv import load_dotenv
from core.assistant import WeatherAssistant

# --- KONFIGURACJA ---
logging.basicConfig(level=logging.INFO)
load_dotenv()

# --- INICJALIZACJA ASYSTENTA ---
try:
    assistant = WeatherAssistant()
except Exception as e:
    print(f"Błąd inicjalizacji asystenta: {e}")
    assistant = None

# --- FUNKCJE LOGIKI ---
def interact_with_weather(user_input):
    if not assistant:
        return "CRITICAL ERROR: System not initialized."
    if not user_input.strip():
        return "INPUT ERROR: Empty query."

    try:
        return assistant.process_query(user_input)
    except Exception as e:
        logging.error(f"Błąd przetwarzania: {e}")
        return f"SYSTEM FAILURE: {str(e)}"

# --- STYLIZACJA CSS (Grey/Orange Terminal) ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Fira+Code:wght@400;700&display=swap');

:root {
    --terminal-orange: #ff6600;       /* Główny kolor tekstu */
    --terminal-dark-orange: #cc4400;  /* Ciemniejszy akcent */
    --terminal-bg: #1a1a1a;           /* CIEMNY SZARY (zamiast czarnego) */
    --terminal-panel: #262626;        /* Nieco jaśniejszy szary dla pól */
    --terminal-glow: 0 0 8px rgba(255, 102, 0, 0.4);
}

body, .gradio-container {
    background-color: var(--terminal-bg) !important;
    color: var(--terminal-orange) !important;
    font-family: 'Fira Code', 'Courier New', monospace !important;
}

/* Główne kontenery */
.block, .panel {
    background-color: var(--terminal-bg) !important;
    border: 1px solid #444 !important; /* Szare obramowanie */
}

/* Nagłówek */
#header-title {
    color: var(--terminal-orange);
    text-shadow: var(--terminal-glow);
    font-family: 'VT323', monospace;
    font-size: 3em;
    text-align: center;
    border-bottom: 2px solid var(--terminal-orange);
    padding-bottom: 10px;
    margin-bottom: 20px;
    background-color: var(--terminal-panel); /* Tło nagłówka */
    border-radius: 4px;
}

/* Pola tekstowe (Input/Output) */
textarea, .output-markdown, .prose {
    background-color: var(--terminal-panel) !important; /* Szare tło pola */
    color: var(--terminal-orange) !important;
    border: 1px solid #555 !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 16px !important;
}

/* Labelki */
label span {
    color: #aaaaaa !important; /* Jasnoszary dla etykiet */
    text-transform: uppercase;
    font-weight: bold;
    font-size: 0.9em !important;
}

/* Przycisk */
button.primary-btn {
    background-color: var(--terminal-orange) !important;
    color: #1a1a1a !important; /* Ciemny tekst na przycisku */
    border: 1px solid var(--terminal-orange) !important;
    font-weight: bold;
    text-transform: uppercase;
    transition: 0.2s;
}

button.primary-btn:hover {
    background-color: #ff8533 !important; /* Jaśniejszy pomarańcz po najechaniu */
    box-shadow: 0 0 10px var(--terminal-orange);
}

/* Ukrycie standardowej stopki Gradio */
footer { display: none !important; }
"""

# --- DEFINICJA INTERFEJSU ---
with gr.Blocks(css=custom_css, title="NeuroWeather GreyOps") as demo:
    
    gr.Markdown("# // NEURO_WEATHER_V3.167", elem_id="header-title")
    
    with gr.Row():
        with gr.Column(scale=4):
            gr.Markdown("### > SYSTEM STATUS: ACTIVE\n###")
            
            input_box = gr.Textbox(
                label="COMMAND INPUT", 
                placeholder="Zadaj pytanie pogodowe...",
                lines=2,
                elem_classes=["terminal-input"]
            )
            
            submit_btn = gr.Button("INITIALIZE SCAN", variant="primary", elem_classes=["primary-btn"])
    
    with gr.Row():
        with gr.Column():
             output_box = gr.Markdown(label="DATA READOUT", value="> Standby for input...", elem_classes=["terminal-output"])

    # Obsługa zdarzeń
    submit_btn.click(fn=interact_with_weather, inputs=input_box, outputs=output_box)
    input_box.submit(fn=interact_with_weather, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    demo.launch(inbrowser=True)