# NOAA Weather Forecast Summarizer NLP and OpenAI

## Overview

The NOAA Weather Summarizer is a Python-based project that retrieves weather forecasts from the National Weather Service (NWS) API, processes the data, and provides detailed and summarized forecasts. The application uses Gradio for a user-friendly web interface and OpenAI for text summarization.

## Features

- Fetch raw weather data from NOAA's National Weather Service (NWS) API.
- Parse and summarize:
  - Detailed weather forecasts.
  - Short weather forecasts.
- Summarize merged forecasts using OpenAI's GPT models.
- Interactive Gradio interface for user input and display.

## Workflow

```mermaid
graph TD
    A[Input Latitude & Longitude] -->|Gradio Interface| B[Fetch NOAA Data]
    B --> C[Parse Forecast Data]
    C --> D[Detailed Forecasts]
    C --> E[Short Forecasts]
    D --> F[Summarize Detailed Forecasts]
    E --> G[Summarize Short Forecasts]
    F --> H[Output Summarized Detailed Forecast]
    G --> I[Output Summarized Short Forecast]
```

## Installation

### Prerequisites

- Python 3.8 or later
- Pip

### Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/noaa-weather-summarizer.git
    cd noaa-weather-summarizer
    ```
2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up your OpenAI API key and optional Hugging Face token:
    - Add your OpenAI API key directly in the script or as an environment variable (`OPENAI_API_KEY`).
    - Optionally, set `HF_TOKEN` in your environment for authenticated Hugging Face access.

## Usage

Run the application:

```bash
python app.py
```

This will launch a Gradio interface where you can input latitude and longitude values to fetch and display weather forecasts.

### Example Inputs

- **Dallas, TX:** Latitude `32.7767`, Longitude `-96.7970`
- **New York City, NY:** Latitude `40.7128`, Longitude `-74.0060`

## Requirements

### `requirements.txt`

```
spacy
transformers
torch
thinc
requests
gradio
```

```python
python -m spacy download en_core_web_trf
```

**RESTART SESSION**



## Sample RAW Data JSON from NOAA API

```json
{
  "@context": [
    "https://geojson.org/geojson-ld/geojson-context.jsonld",
    {
      "@version": "1.1",
      "wx": "https://api.weather.gov/ontology#",
      "geo": "http://www.opengis.net/ont/geosparql#",
      "unit": "http://codes.wmo.int/common/unit/",
      "@vocab": "https://api.weather.gov/ontology#"
    }
  ],
  "type": "Feature",
  "geometry": {
    "type": "Polygon",
    "coordinates": [
      [
        [
          -96.7897,
          32.7685
        ],
        [
          -96.78999999999999,
          32.7911
        ],
        [
          -96.81689999999999,
          32.7908
        ],
        [
          -96.81649999999999,
          32.7682
        ],
        [
          -96.7897,
          32.7685
        ]
      ]
    ]
  },
  "properties": {
    "units": "us",
    "forecastGenerator": "BaselineForecastGenerator",
    "generatedAt": "2024-12-26T13:00:41+00:00",
    "updateTime": "2024-12-26T10:08:34+00:00",
    "validTimes": "2024-12-26T04:00:00+00:00/P8DT6H",
    "elevation": {
      "unitCode": "wmoUnit:m",
      "value": 136.8552
    },
    "periods": [
      {
        "number": 1,
        "name": "Today",
        "startTime": "2024-12-26T07:00:00-06:00",
        "endTime": "2024-12-26T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 62,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": 90
        },
        "windSpeed": "0 to 5 mph",
        "windDirection": "NNE",
        "icon": "https://api.weather.gov/icons/land/day/tsra,90?size=medium",
        "shortForecast": "Patchy Fog",
        "detailedForecast": "A chance of rain showers and patchy fog before 9am, then patchy fog and showers and thunderstorms between 9am and noon, then patchy fog and showers and thunderstorms. Cloudy. High near 62, with temperatures falling to around 60 in the afternoon. North northeast wind 0 to 5 mph. Chance of precipitation is 90%. New rainfall amounts between a half and three quarters of an inch possible."
      },
      {
        "number": 2,
        "name": "Tonight",
        "startTime": "2024-12-26T18:00:00-06:00",
        "endTime": "2024-12-27T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 49,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "0 to 5 mph",
        "windDirection": "WNW",
        "icon": "https://api.weather.gov/icons/land/night/bkn/fog?size=medium",
        "shortForecast": "Mostly Cloudy then Patchy Fog",
        "detailedForecast": "Patchy fog after 2am. Mostly cloudy, with a low around 49. West northwest wind 0 to 5 mph."
      },
      {
        "number": 3,
        "name": "Friday",
        "startTime": "2024-12-27T06:00:00-06:00",
        "endTime": "2024-12-27T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 68,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "0 to 10 mph",
        "windDirection": "SW",
        "icon": "https://api.weather.gov/icons/land/day/fog/sct?size=medium",
        "shortForecast": "Patchy Fog then Mostly Sunny",
        "detailedForecast": "Patchy fog before 10am. Mostly sunny. High near 68, with temperatures falling to around 64 in the afternoon. Southwest wind 0 to 10 mph."
      },
      {
        "number": 4,
        "name": "Friday Night",
        "startTime": "2024-12-27T18:00:00-06:00",
        "endTime": "2024-12-28T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 48,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 mph",
        "windDirection": "SSW",
        "icon": "https://api.weather.gov/icons/land/night/sct?size=medium",
        "shortForecast": "Partly Cloudy",
        "detailedForecast": "Partly cloudy, with a low around 48. South southwest wind around 5 mph."
      },
      {
        "number": 5,
        "name": "Saturday",
        "startTime": "2024-12-28T06:00:00-06:00",
        "endTime": "2024-12-28T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 70,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 to 10 mph",
        "windDirection": "WSW",
        "icon": "https://api.weather.gov/icons/land/day/sct?size=medium",
        "shortForecast": "Mostly Sunny",
        "detailedForecast": "Mostly sunny. High near 70, with temperatures falling to around 65 in the afternoon. West southwest wind 5 to 10 mph."
      },
      {
        "number": 6,
        "name": "Saturday Night",
        "startTime": "2024-12-28T18:00:00-06:00",
        "endTime": "2024-12-29T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 45,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "0 to 5 mph",
        "windDirection": "WNW",
        "icon": "https://api.weather.gov/icons/land/night/few?size=medium",
        "shortForecast": "Mostly Clear",
        "detailedForecast": "Mostly clear. Low around 45, with temperatures rising to around 47 overnight. West northwest wind 0 to 5 mph."
      },
      {
        "number": 7,
        "name": "Sunday",
        "startTime": "2024-12-29T06:00:00-06:00",
        "endTime": "2024-12-29T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 69,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "0 to 5 mph",
        "windDirection": "SW",
        "icon": "https://api.weather.gov/icons/land/day/few?size=medium",
        "shortForecast": "Sunny",
        "detailedForecast": "Sunny, with a high near 69. Southwest wind 0 to 5 mph."
      },
      {
        "number": 8,
        "name": "Sunday Night",
        "startTime": "2024-12-29T18:00:00-06:00",
        "endTime": "2024-12-30T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 50,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 mph",
        "windDirection": "S",
        "icon": "https://api.weather.gov/icons/land/night/few?size=medium",
        "shortForecast": "Mostly Clear",
        "detailedForecast": "Mostly clear, with a low around 50. South wind around 5 mph."
      },
      {
        "number": 9,
        "name": "Monday",
        "startTime": "2024-12-30T06:00:00-06:00",
        "endTime": "2024-12-30T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 76,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 to 10 mph",
        "windDirection": "SW",
        "icon": "https://api.weather.gov/icons/land/day/few?size=medium",
        "shortForecast": "Sunny",
        "detailedForecast": "Sunny, with a high near 76. Southwest wind 5 to 10 mph, with gusts as high as 25 mph."
      },
      {
        "number": 10,
        "name": "Monday Night",
        "startTime": "2024-12-30T18:00:00-06:00",
        "endTime": "2024-12-31T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 44,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 to 10 mph",
        "windDirection": "NW",
        "icon": "https://api.weather.gov/icons/land/night/skc?size=medium",
        "shortForecast": "Clear",
        "detailedForecast": "Clear, with a low around 44."
      },
      {
        "number": 11,
        "name": "Tuesday",
        "startTime": "2024-12-31T06:00:00-06:00",
        "endTime": "2024-12-31T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 60,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 to 10 mph",
        "windDirection": "N",
        "icon": "https://api.weather.gov/icons/land/day/skc?size=medium",
        "shortForecast": "Sunny",
        "detailedForecast": "Sunny, with a high near 60."
      },
      {
        "number": 12,
        "name": "Tuesday Night",
        "startTime": "2024-12-31T18:00:00-06:00",
        "endTime": "2025-01-01T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 38,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 mph",
        "windDirection": "N",
        "icon": "https://api.weather.gov/icons/land/night/few?size=medium",
        "shortForecast": "Mostly Clear",
        "detailedForecast": "Mostly clear, with a low around 38."
      },
      {
        "number": 13,
        "name": "New Year's Day",
        "startTime": "2025-01-01T06:00:00-06:00",
        "endTime": "2025-01-01T18:00:00-06:00",
        "isDaytime": true,
        "temperature": 56,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "5 mph",
        "windDirection": "NNE",
        "icon": "https://api.weather.gov/icons/land/day/sct?size=medium",
        "shortForecast": "Mostly Sunny",
        "detailedForecast": "Mostly sunny, with a high near 56."
      },
      {
        "number": 14,
        "name": "Wednesday Night",
        "startTime": "2025-01-01T18:00:00-06:00",
        "endTime": "2025-01-02T06:00:00-06:00",
        "isDaytime": false,
        "temperature": 36,
        "temperatureUnit": "F",
        "temperatureTrend": "",
        "probabilityOfPrecipitation": {
          "unitCode": "wmoUnit:percent",
          "value": null
        },
        "windSpeed": "0 to 5 mph",
        "windDirection": "NE",
        "icon": "https://api.weather.gov/icons/land/night/sct?size=medium",
        "shortForecast": "Partly Cloudy",
        "detailedForecast": "Partly cloudy, with a low around 36."
      }
    ]
  }
}
```

## Summary

```python
Here's a summary of the weather forecast for the upcoming days:

**Today:** 
- Temperature: 62°F, falling to around 60°F in the afternoon.
- Conditions: Patchy fog, rain showers, and thunderstorms expected, especially before noon.
- Winds: NNE at 0 to 5 mph.
- Chance of precipitation: 90%, with rainfall amounts between 0.5 to 0.75 inches.

**Friday:** 
- Temperature: 68°F, falling to around 64°F in the afternoon.
- Conditions: Patchy fog in the morning, then mostly sunny.
- Winds: SW at 0 to 10 mph.

**Saturday:** 
- Temperature: 70°F, falling to around 65°F in the afternoon.
- Conditions: Mostly sunny.
- Winds: WSW at 5 to 10 mph.

**Sunday:** 
- Temperature: 69°F.
- Conditions: Sunny.
- Winds: SW at 0 to 5 mph.

**Monday:** 
- Temperature: 76°F.
- Conditions: Sunny.
- Winds: SW at 5 to 10 mph, with gusts up to 25 mph.

**Tuesday:** 
- Temperature: 60°F.
- Conditions: Sunny.
- Winds: N at 5 to 10 mph.

**New Year's Day:** 
- Temperature: 56°F.
- Conditions: Mostly sunny.
- Winds: NNE at 5 mph.

Overall, expect a mix of rain and thunderstorms today, followed by a warming trend with mostly sunny conditions through the weekend and into the start of the new year.
```


## Detailed Forecasts

```python
day 1 forecast suggests A chance of rain showers and patchy fog before 9am, then patchy fog and showers and thunderstorms between 9am and noon, then patchy fog and showers and thunderstorms. Cloudy. High near 62, with temperatures falling to around 60 in the afternoon. North northeast wind 0 to 5 mph. Chance of precipitation is 90%. New rainfall amounts between a half and three quarters of an inch possible. day 2 forecast suggests Patchy fog after 2am. Mostly cloudy, with a low around 49. West northwest wind 0 to 5 mph. day 3 forecast suggests Patchy fog before 10am. Mostly sunny. High near 68, with temperatures falling to around 64 in the afternoon. Southwest wind 0 to 10 mph. day 4 forecast suggests Partly cloudy, with a low around 48. South southwest wind around 5 mph. day 5 forecast suggests Mostly sunny. High near 70, with temperatures falling to around 65 in the afternoon. West southwest wind 5 to 10 mph. day 6 forecast suggests Mostly clear. Low around 45, with temperatures rising to around 47 overnight. West northwest wind 0 to 5 mph. day 7 forecast suggests Sunny, with a high near 69. Southwest wind 0 to 5 mph. day 8 forecast suggests Mostly clear, with a low around 50. South wind around 5 mph. day 9 forecast suggests Sunny, with a high near 76. Southwest wind 5 to 10 mph, with gusts as high as 25 mph. day 10 forecast suggests Clear, with a low around 44. day 11 forecast suggests Sunny, with a high near 60. day 12 forecast suggests Mostly clear, with a low around 38. day 13 forecast suggests Mostly sunny, with a high near 56. day 14 forecast suggests Partly cloudy, with a low around 36.
```

## Detailed Forecast Summary


```python
Here's a detailed summary of the weather forecast over the next two weeks:

**Day 1:**
- **Weather:** Chance of rain showers and patchy fog before 9 AM, followed by showers and thunderstorms from 9 AM to noon, continuing with patchy fog and thunderstorms throughout the day.
- **Temperature:** High near 62°F, dropping to around 60°F in the afternoon.
- **Wind:** North northeast at 0 to 5 mph.
- **Precipitation:** 90% chance of rain, with expected rainfall amounts between 0.5 to 0.75 inches.

**Day 2:**
- **Weather:** Patchy fog after 2 AM, mostly cloudy throughout the day.
- **Temperature:** Low around 49°F.
- **Wind:** West northwest at 0 to 5 mph.

**Day 3:**
- **Weather:** Patchy fog before 10 AM, mostly sunny for the rest of the day.
- **Temperature:** High near 68°F, falling to around 64°F in the afternoon.
- **Wind:** Southwest at 0 to 10 mph.

**Day 4:**
- **Weather:** Partly cloudy.
- **Temperature:** Low around 48°F.
- **Wind:** South southwest at around 5 mph.

**Day 5:**
- **Weather:** Mostly sunny.
- **Temperature:** High near 70°F, dropping to around 65°F in the afternoon.
- **Wind:** West southwest at 5 to 10 mph.

**Day 6:**
- **Weather:** Mostly clear.
- **Temperature:** Low around 45°F, with temperatures rising to around 47°F overnight.
- **Wind:** West northwest at 0 to 5 mph.

**Day 7:**
- **Weather:** Sunny.
- **Temperature:** High near 69°F.
- **Wind:** Southwest at 0 to 5 mph.

**Day 8:**
- **Weather:** Mostly clear.
- **Temperature:** Low around 50°F.
- **Wind:** South at around 5 mph.

**Day 9:**
- **Weather:** Sunny.
- **Temperature:** High near 76°F.
- **Wind:** Southwest at 5 to 10 mph, with gusts up to 25 mph.

**Day 10:**
- **Weather:** Clear.
- **Temperature:** Low around 44°F.

**Day 11:**
- **Weather:** Sunny.
- **Temperature:** High near 60°F.

**Day 12:**
- **Weather:** Mostly clear.
- **Temperature:** Low around 38°F.

**Day 13:**
- **Weather:** Mostly sunny.
- **Temperature:** High near 56°F.

**Day 14:**
- **Weather:** Partly cloudy.
- **Temperature:** Low around 36°F.

Overall, the forecast indicates a wet start with thunderstorms on Day 1, transitioning to mostly sunny and clear conditions in the following days, with temperatures gradually warming up towards Day 9.
```

## Short Forecasts

```python
day 1 forecast suggests Patchy Fog day 2 forecast suggests Mostly Cloudy then Patchy Fog day 3 forecast suggests Patchy Fog then Mostly Sunny day 4 forecast suggests Partly Cloudy day 5 forecast suggests Mostly Sunny day 6 forecast suggests Mostly Clear day 7 forecast suggests Sunny day 8 forecast suggests Mostly Clear day 9 forecast suggests Sunny day 10 forecast suggests Clear day 11 forecast suggests Sunny day 12 forecast suggests Mostly Clear day 13 forecast suggests Mostly Sunny day 14 forecast suggests Partly Cloudy
```


## Short Forecast Summary


```python
Here's a summary of the weather forecast for the next 14 days:

- **Day 1**: Patchy Fog
- **Day 2**: Mostly Cloudy, then Patchy Fog
- **Day 3**: Patchy Fog, then Mostly Sunny
- **Day 4**: Partly Cloudy
- **Day 5**: Mostly Sunny
- **Day 6**: Mostly Clear
- **Day 7**: Sunny
- **Day 8**: Mostly Clear
- **Day 9**: Sunny
- **Day 10**: Clear
- **Day 11**: Sunny
- **Day 12**: Mostly Clear
- **Day 13**: Mostly Sunny
- **Day 14**: Partly Cloudy

Overall, expect a mix of fog, clouds, and plenty of sunny days ahead!
```



## Screenshots

![image](https://github.com/user-attachments/assets/edf7d67a-dbe7-4c5c-ba00-95161ff70c2b)

![image](https://github.com/user-attachments/assets/ec0c858e-8609-414e-8401-9f4eb01ae3ce)


![image](https://github.com/user-attachments/assets/567c4497-d8cf-4192-99bb-dc8e6c80c9c2)

![image](https://github.com/user-attachments/assets/dae1d6e8-262f-4cf3-a9a9-f4cfc355fee0)


![image](https://github.com/user-attachments/assets/c945188d-0043-425e-a974-5a56a4689870)

![image](https://github.com/user-attachments/assets/03af3eb3-58f2-4bf7-bcce-dcf4986722c3)




## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgements

- [NOAA National Weather Service API](https://www.weather.gov/documentation/services-web-api)
- [OpenAI GPT Models](https://openai.com/)
- [Gradio](https://gradio.app/)
- [spaCy](https://spacy.io/)

## Contact

For issues or inquiries, please contact [your.email@example.com](mailto:your.email@example.com).

