from datetime import datetime

WMO_CONDITIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}

# Short forms for tight spaces (hourly strip in a quadrant cell)
WMO_SHORT = {
    0: "Sun", 1: "Sun", 2: "Cloud", 3: "Cloud",
    45: "Fog", 48: "Fog",
    51: "Drzl", 53: "Drzl", 55: "Drzl", 56: "Drzl", 57: "Drzl",
    61: "Rain", 63: "Rain", 65: "Rain", 66: "Rain", 67: "Rain",
    71: "Snow", 73: "Snow", 75: "Snow", 77: "Snow",
    80: "Rain", 81: "Rain", 82: "Rain",
    85: "Snow", 86: "Snow",
    95: "Strm", 96: "Strm", 99: "Strm",
}


def run(input):
    current = input["current"]
    daily = input["daily"]
    hourly = input["hourly"]

    # hourly[0] is the current hour (already shown as "now"); take the next 4.
    upcoming = []
    for time_str, temp, code in zip(
        hourly["time"][1:5], hourly["temperature_2m"][1:5], hourly["weather_code"][1:5]
    ):
        hour = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        label = hour.strftime("%I %p").lstrip("0")
        upcoming.append({
            "time": label,
            "temp": round(temp),
            "condition": WMO_SHORT.get(code, "—"),
        })

    return {
        "location": "Burnaby, BC",
        "temperature": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"],
        "wind_speed": round(current["wind_speed_10m"]),
        "condition": WMO_CONDITIONS.get(current["weather_code"], "Unknown"),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
        "hourly": upcoming,
    }
