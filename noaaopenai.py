# Developed by
# Partha Pratim Ray
# https://github.com/ParthaPRay/
# parthapratimray1986@gmail.com

######## NOAA API WEATHER FORECAST SUMMARIZATION
# Text summarization
# NOAA Raw Response + Sumarize weather forecast 
# Detailed forecast + detailed summary
# Short forecat + short summary

#### NOAA API WEATHER FORECAST SUMMARIZATION
# NOAA Raw Response + Sumarize weather forecast 
# Detailed forecast + detailed summary
# Short forecat + short summary
######## OpenaAI summarization

import os
import json
import logging
from typing import Optional, Tuple, List, Dict
from datetime import datetime

import requests
from cachetools import TTLCache, cached
import spacy
import gradio as gr

# NEW (OpenAI v1 migration)
from openai import OpenAI
# Hardcode your API key here
client = OpenAI(
    api_key="YOUR_OPENAI_API"  # <-- Replace with your actual key
)

# ---------------------- Configuration ----------------------

USER_AGENT = "WeatherApp/1.0 (your.email@example.com)"  # Replace with your actual email
CACHE_TTL = 600  # Cache Time-To-Live in seconds (e.g., 10 minutes)
FORECAST_DAYS = 14  # Number of days to include in the summary

# Optional: Hugging Face Token for authenticated access
HF_TOKEN = os.getenv("HF_TOKEN")  # Ensure this environment variable is set if you have a token

# ---------------------- Logging Setup ----------------------

def setup_logging():
    """
    Configures the logging settings.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

setup_logging()

# ---------------------- Cache Setup ----------------------

# Initialize a TTL cache
forecast_cache = TTLCache(maxsize=100, ttl=CACHE_TTL)

# ---------------------- NOAA Data Fetcher ----------------------

class NOAADataFetcher:
    """
    Fetches weather forecast data from NOAA's National Weather Service (NWS) API.
    """

    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.headers = {'User-Agent': self.user_agent}
        self.endpoint_template = "https://api.weather.gov/points/{latitude},{longitude}"

    @cached(cache=forecast_cache)
    def fetch_forecast(self, latitude: float, longitude: float) -> Optional[dict]:
        """
        Fetches the weather forecast data for the given latitude and longitude.
        """
        endpoint = self.endpoint_template.format(latitude=latitude, longitude=longitude)
        try:
            logging.info(f"Fetching metadata from NOAA NWS API for lat: {latitude}, lon: {longitude}.")
            response = requests.get(endpoint, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            logging.debug(f"Metadata Response: {json.dumps(data, indent=2)}")

            # Extract the forecast URL
            forecast_url = data['properties']['forecast']
            logging.info("Fetching forecast data from NOAA NWS API.")
            forecast_response = requests.get(forecast_url, headers=self.headers, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            logging.debug(f"Forecast Response: {json.dumps(forecast_data, indent=2)}")

            return forecast_data

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Request exception: {req_err}")
        except KeyError as key_err:
            logging.error(f"Key error: {key_err}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

        return None

# ---------------------- Weather Data Parser ----------------------

class WeatherDataParser:
    """
    Parses and processes raw weather forecast data from NOAA's NWS API.
    """

    def parse_forecast(self, forecast_data: dict, days: int = 14) -> List[str]:
        """
        Parses forecast data and constructs descriptive paragraphs.
        """
        try:
            logging.info("Parsing weather data.")
            periods = forecast_data['properties']['periods']
            filtered_periods = self.filter_forecast_periods(periods, days)
            paragraphs = self.construct_paragraphs(filtered_periods)
            logging.debug(f"Full Paragraph: {' '.join(paragraphs)}")
            return paragraphs
        except KeyError as key_err:
            logging.error(f"Key error while parsing weather data: {key_err}")
            raise
        except Exception as e:
            logging.error(f"Error parsing weather data: {e}")
            raise

    def filter_forecast_periods(self, periods: List[dict], days: int) -> List[dict]:
        """
        Filters forecast periods to include only the specified number of days.
        """
        filtered = []
        current_day = None
        for period in periods:
            day = period['startTime'][:10]  # Extract YYYY-MM-DD
            if day != current_day:
                current_day = day
                filtered.append(period)
                if len(filtered) >= days * 2:  # Day and Night for each day
                    break
        logging.info(f"Filtered down to {len(filtered)} periods for summarization.")
        return filtered

    def construct_paragraphs(self, periods: List[dict]) -> List[str]:
        """
        Constructs descriptive paragraphs from forecast periods.
        """
        paragraphs = []
        for period in periods:
            name = period.get('name', 'N/A')
            temperature = period.get('temperature', 'N/A')
            temperature_unit = period.get('temperatureUnit', '')
            wind_speed = period.get('windSpeed', 'N/A')
            wind_direction = period.get('windDirection', 'N/A')
            short_forecast = period.get('shortForecast', '')
            detailed_forecast = period.get('detailedForecast', '')

            forecast_paragraph = (
                f"{name}: The temperature will be {temperature}°{temperature_unit} "
                f"with {short_forecast.lower()}. Winds are expected to be {wind_speed} "
                f"from the {wind_direction.lower()}. {detailed_forecast}"
            )
            paragraphs.append(forecast_paragraph)
            logging.debug(f"Parsed forecast for {name}: {forecast_paragraph}")
        return paragraphs

    def extract_and_merge_detailed_forecasts(self, forecast_data: dict) -> str:
        """
        Extracts 'number' and 'detailedForecast', transforms them, and concatenates into a paragraph.
        """
        try:
            logging.info("Extracting and merging detailed forecasts.")
            periods = forecast_data['properties']['periods']
            merged_content = ""
            for period in periods:
                number = period.get('number')
                detailed_forecast = period.get('detailedForecast', '').strip()
                if number is not None and detailed_forecast:
                    day_forecast = f"day {number} forecast suggests {detailed_forecast}"
                    merged_content += f"{day_forecast} "
            merged_content = merged_content.strip()
            logging.debug(f"Merged Detailed Forecasts Paragraph: {merged_content}")
            return merged_content
        except KeyError as key_err:
            logging.error(f"Key error while extracting detailed forecasts: {key_err}")
            raise
        except Exception as e:
            logging.error(f"Error extracting detailed forecasts: {e}")
            raise

    def extract_and_merge_short_forecasts(self, forecast_data: dict) -> str:
        """
        Extracts 'number' and 'shortForecast', transforms them, and concatenates into a paragraph.
        """
        try:
            logging.info("Extracting and merging short forecasts.")
            periods = forecast_data['properties']['periods']
            merged_content = ""
            for period in periods:
                number = period.get('number')
                short_forecast = period.get('shortForecast', '').strip()
                if number is not None and short_forecast:
                    day_forecast = f"day {number} forecast suggests {short_forecast}"
                    merged_content += f"{day_forecast} "
            merged_content = merged_content.strip()
            logging.debug(f"Merged Short Forecasts Paragraph: {merged_content}")
            return merged_content
        except KeyError as key_err:
            logging.error(f"Key error while extracting short forecasts: {key_err}")
            raise
        except Exception as e:
            logging.error(f"Error extracting short forecasts: {e}")
            raise

# ---------------------- Weather Summarizer ----------------------

class WeatherSummarizer:
    """
    Generates summaries using OpenAI GPT-4o-mini (via the new v1 migration).
    """

    def __init__(self):
        """
        Initializes the summarizer.
        Loads spaCy for potential text processing if needed.
        """
        try:
            logging.info("Loading spaCy language model.")
            self.nlp = spacy.load("en_core_web_trf")
            logging.info("spaCy model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load spaCy model: {e}")
            raise

    def summarize(self, paragraphs: List[str], max_length: int = 150, min_length: int = 40) -> str:
        """
        (Optional) Summarize a list of paragraphs using GPT-4o-mini.
        """
        try:
            logging.info("Generating summary with GPT-4o-mini (optional).")
            full_text = " ".join(paragraphs)

            # Use the new openai v1 style calls
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant summarizing weather data."
                    },
                    {
                        "role": "user",
                        "content": full_text
                    }
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during summarization: {e}")
            raise

    def summarize_merged_detailed_forecasts(self, merged_content: str, max_length: int = 700, min_length: int = 40) -> str:
        """
        Generates a summary from the merged detailed forecasts using GPT-4o-mini.
        """
        try:
            logging.info("Generating GPT-4o-mini summary for merged detailed forecasts.")

            doc = self.nlp(merged_content)
            sentences = [sent.text for sent in doc.sents]
            paragraph = " ".join(sentences)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant summarizing weather forecasts in detail."
                    },
                    {
                        "role": "user",
                        "content": paragraph
                    }
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during detailed forecasts summarization: {e}")
            raise

    def summarize_merged_short_forecasts(self, merged_content: str, max_length: int = 150, min_length: int = 40) -> str:
        """
        Generates a summary from the merged short forecasts using GPT-4o-mini.
        """
        try:
            logging.info("Generating GPT-4o-mini summary for merged short forecasts.")

            doc = self.nlp(merged_content)
            sentences = [sent.text for sent in doc.sents]
            paragraph = " ".join(sentences)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant summarizing short weather forecasts."
                    },
                    {
                        "role": "user",
                        "content": paragraph
                    }
                ],
                temperature=0,
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error during short forecasts summarization: {e}")
            raise

# ---------------------- Input Validation ----------------------

def validate_coordinates(latitude: float, longitude: float) -> Optional[str]:
    """
    Validates the latitude and longitude values.
    """
    errors = []
    if not (-90 <= latitude <= 90):
        errors.append("Latitude must be between -90 and 90.")
    if not (-180 <= longitude <= 180):
        errors.append("Longitude must be between -180 and 180.")
    if errors:
        return " ".join(errors)
    return None

# ---------------------- Gradio Interface Function ----------------------

def weather_gradio_interface(latitude: float, longitude: float) -> Tuple[str, str, str, str, str, str]:
    """
    Gradio interface function to fetch, parse, and summarize weather data.
    Returns:
        tuple:
            - Raw NOAA API response (as text)
            - Summary of forecast
            - Merged Detailed Forecasts
            - Summarized Detailed Forecast
            - Merged Short Forecasts
            - Summarized Short Forecast
    """
    # Validate inputs
    validation_error = validate_coordinates(latitude, longitude)
    if validation_error:
        logging.error(f"Input validation failed: {validation_error}")
        return (
            validation_error,
            "Unable to generate summary due to invalid inputs.",
            "",
            "",
            "",
            ""
        )

    # Initialize components
    fetcher = NOAADataFetcher(user_agent=USER_AGENT)
    parser = WeatherDataParser()
    summarizer = WeatherSummarizer()

    try:
        # Fetch data
        forecast_data = fetcher.fetch_forecast(latitude, longitude)
        if not forecast_data:
            logging.error("No forecast data retrieved.")
            return (
                "No forecast data retrieved.",
                "Unable to generate summary.",
                "",
                "",
                "",
                ""
            )

        # Parse data
        paragraphs = parser.parse_forecast(forecast_data, days=FORECAST_DAYS)
        if not paragraphs:
            logging.error("No weather information available to summarize.")
            return (
                "No weather information available to summarize.",
                "Unable to generate summary.",
                "",
                "",
                "",
                ""
            )

        # Summarize (using GPT-4o-mini)
        summary = summarizer.summarize(paragraphs)

        # Prepare raw data
        raw_data = json.dumps(forecast_data, indent=2)

        # Extract/Merge & Summarize Detailed Forecasts
        merged_detailed_forecasts = parser.extract_and_merge_detailed_forecasts(forecast_data)
        merged_detailed_summary = summarizer.summarize_merged_detailed_forecasts(merged_detailed_forecasts)

        # Extract/Merge & Summarize Short Forecasts
        merged_short_forecasts = parser.extract_and_merge_short_forecasts(forecast_data)
        merged_short_summary = summarizer.summarize_merged_short_forecasts(merged_short_forecasts)

        return (
            raw_data,
            summary,
            merged_detailed_forecasts,
            merged_detailed_summary,
            merged_short_forecasts,
            merged_short_summary
        )

    except Exception as e:
        logging.critical(f"Error in Gradio interface: {e}")
        return (
            f"An error occurred: {e}",
            "Unable to generate summary.",
            "",
            "",
            "",
            ""
        )

# ---------------------- Main Execution ----------------------

if __name__ == "__main__":
    if HF_TOKEN:
        os.environ["HUGGINGFACE_HUB_TOKEN"] = HF_TOKEN
        logging.info("Hugging Face token found and set.")
    else:
        logging.warning("""
        Hugging Face token (HF_TOKEN) not found.
        Proceeding without authentication may lead to rate limiting.
        """)

    import torch
    device = 0 if torch.cuda.is_available() else -1
    if device == 0:
        logging.info("GPU is available, though not used by GPT-4o-mini here.")
    else:
        logging.info("Using CPU for summarization calls to GPT-4o-mini.")

    with gr.Blocks() as demo:
        gr.Markdown("# NOAA API Weather Forecast Summarizer by using Spacy and OpenAI")
        gr.Markdown("""
        Developed by **Partha Pratim Ray**, **parthapratimray1986@gmail.com**
        """)
        gr.Markdown("""
        Enter the **latitude** and **longitude** of a location to retrieve a summarized weather forecast.
        """)

        with gr.Row():
            latitude_input = gr.Number(label="Latitude", value=32.7767)
            longitude_input = gr.Number(label="Longitude", value=-96.7970)

        submit_button = gr.Button("Submit")

        with gr.Tab("Raw Data"):
            raw_output = gr.Textbox(label="Raw NOAA API Response", lines=20, interactive=False)

        with gr.Tab("Summary"):
            summary_output = gr.Textbox(label="Summarized Weather Forecast", lines=10, interactive=False)

        with gr.Tab("Detailed Forecasts"):
            merged_detailed_forecast_output = gr.Textbox(label="Merged Detailed Forecasts", lines=30, interactive=False)

        with gr.Tab("Detailed Forecast Summary"):
            merged_detailed_summary_output = gr.Textbox(label="Summarized Detailed Forecast", lines=5, interactive=False)

        with gr.Tab("Short Forecasts"):
            merged_short_forecast_output = gr.Textbox(label="Merged Short Forecasts", lines=30, interactive=False)

        with gr.Tab("Short Forecast Summary"):
            merged_short_summary_output = gr.Textbox(label="Summarized Short Forecasts", lines=5, interactive=False)

        submit_button.click(
            fn=weather_gradio_interface,
            inputs=[latitude_input, longitude_input],
            outputs=[
                raw_output,
                summary_output,
                merged_detailed_forecast_output,
                merged_detailed_summary_output,
                merged_short_forecast_output,
                merged_short_summary_output
            ]
        )

        gr.Markdown("""
        ---
        **Note:** Ensure that the latitude and longitude values are valid. For example:
        - **Dallas, TX:** Latitude `32.7767`, Longitude `-96.7970`
        - **New York City, NY:** Latitude `40.7128`, Longitude `-74.0060`
        """)

    demo.launch()

