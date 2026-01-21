import sys
import logging
import argparse
from core.assistant import WeatherAssistant
from interfaces.cli import run_cli
from interfaces.web import run_web_ui


def setup_logging() -> None:
    """Configures global logging format."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )


def parse_arguments() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="NeuroWeather AI System")
    parser.add_argument(
        "--mode",
        choices=["cli", "web"],
        default="cli",
        help="Interface mode: 'cli' for terminal, 'web' for browser UI."
    )
    return parser.parse_args()


def main() -> None:
    # 1. Setup Environment
    setup_logging()
    args = parse_arguments()
    logger = logging.getLogger(__name__)

    # 2. Initialize Core Logic (Dependency Injection)
    try:
        app = WeatherAssistant()
    except Exception as e:
        logger.critical(f"Failed to initialize WeatherAssistant: {e}")
        sys.exit(1)

    # 3. Launch Selected Interface
    if args.mode == "web":
        logger.info("Starting Web Interface...")
        try:
            run_web_ui(app)
        except ImportError:
            logger.error("Gradio is not installed. Run: pip install gradio")
    else:
        logger.info("Starting CLI Interface...")
        run_cli(app)


if __name__ == "__main__":
    main()
