import logging
from core.assistant import WeatherAssistant


def setup_logging() -> None:
    """Configures global logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def main() -> None:
    setup_logging()
    app = WeatherAssistant()

    print("NeuroWeather initialized. Type a weather-related question or type 'exit' to quit.")

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'q']:
                break

            response = app.process_query(user_input)
            print("-" * 60)
            print(response)
            print("-" * 60)

        except KeyboardInterrupt:
            print("\nShutting down...")
            break
        except Exception as e:
            logging.critical(f"Unhandled exception: {e}")


if __name__ == "__main__":
    main()
