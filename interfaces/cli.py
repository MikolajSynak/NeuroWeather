import logging
from core.assistant import WeatherAssistant

logger = logging.getLogger("NeuroWeather")


def run_cli(app: WeatherAssistant) -> None:
    """Runs the Command Line Interface loop."""
    print("NeuroWeather CLI initialized. Type 'exit' to quit.")
    print("-" * 60)

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Terminating session...")
                break

            response = app.process_query(user_input)
            print("-" * 60)
            print(response)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\nForce shutdown detected.")
            break
        except Exception as e:
            logger.critical(f"CLI Loop Error: {e}")