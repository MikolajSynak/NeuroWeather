import logging
import gradio as gr
from core.assistant import WeatherAssistant
from settings import config

logger = logging.getLogger("NeuroWeather")


def run_web_ui(app: WeatherAssistant) -> None:
    """Launches the Gradio Web Interface."""

    def interact(user_input: str) -> str:
        if not user_input.strip():
            return "ERROR: Empty Input"
        try:
            return app.process_query(user_input)
        except Exception as e:
            logger.error(f"Web UI Error: {e}")
            return f"SYSTEM FAILURE: {str(e)}"

    with gr.Blocks(css=config.UI_CUSTOM_CSS, title=config.UI_TITLE) as demo:

        gr.Markdown(f"# {config.UI_HEADER}", elem_id="header-title")

        with gr.Row():
            with gr.Column():
                input_box = gr.Textbox(
                    label="COMMAND INPUT",
                    placeholder="Enter weather query...",
                    lines=2
                )
                submit_btn = gr.Button("EXECUTE", variant="primary", elem_classes=["primary-btn"])

        with gr.Row():
            output_box = gr.Markdown(label="SYSTEM READOUT", value="> Standby...")

        # Event Bindings
        submit_btn.click(fn=interact, inputs=input_box, outputs=output_box)
        input_box.submit(fn=interact, inputs=input_box, outputs=output_box)

    print(f"Launching Web UI: {config.UI_TITLE}")
    demo.launch(inbrowser=True)
