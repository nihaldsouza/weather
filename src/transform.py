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

# Maps to icon names rendered by the `weather_icon` Liquid template (shared.liquid)
WMO_ICON = {
    0: "sun", 1: "sun", 2: "cloud-sun", 3: "cloud",
    45: "fog", 48: "fog",
    51: "cloud-drizzle", 53: "cloud-drizzle", 55: "cloud-drizzle",
    56: "cloud-drizzle", 57: "cloud-drizzle",
    61: "cloud-rain", 63: "cloud-rain", 65: "cloud-rain",
    66: "cloud-rain", 67: "cloud-rain",
    71: "cloud-snow", 73: "cloud-snow", 75: "cloud-snow", 77: "cloud-snow",
    80: "cloud-rain", 81: "cloud-rain", 82: "cloud-rain",
    85: "cloud-snow", 86: "cloud-snow",
    95: "cloud-lightning", 96: "cloud-lightning", 99: "cloud-lightning",
}


UV_CATEGORY = [
    (3, "Low"),
    (6, "Moderate"),
    (8, "High"),
    (11, "Very High"),
]


def uv_category(uv_index):
    for threshold, label in UV_CATEGORY:
        if uv_index < threshold:
            return label
    return "Extreme"


def run(input):
    current = input["current"]
    daily = input["daily"]
    hourly = input["hourly"]

    # hourly[0] is the current hour (already shown as "now"); take the next 8.
    upcoming_temps = [round(t) for t in hourly["temperature_2m"][1:9]]
    temp_min, temp_max = min(upcoming_temps), max(upcoming_temps)
    temp_range = temp_max - temp_min or 1  # avoid div-by-zero when temps are flat
    bar_min, bar_max = 6, 24  # px, for the quadrant hourly bar chart

    upcoming = []
    for time_str, temp, code in zip(
        hourly["time"][1:9], hourly["temperature_2m"][1:9], hourly["weather_code"][1:9]
    ):
        hour = datetime.strptime(time_str, "%Y-%m-%dT%H:%M")
        label = hour.strftime("%I %p").lstrip("0")
        rounded_temp = round(temp)
        bar_height = round(
            bar_min + (rounded_temp - temp_min) / temp_range * (bar_max - bar_min)
        )
        upcoming.append({
            "time": label,
            "temp": rounded_temp,
            "condition": WMO_SHORT.get(code, "—"),
            "icon": WMO_ICON.get(code, "cloud"),
            "bar_height": bar_height,
        })

    # daily["time"][0] is today; take the next 6 days.
    daily_forecast = []
    for time_str, day_max, day_min, code in zip(
        daily["time"][1:7],
        daily["temperature_2m_max"][1:7],
        daily["temperature_2m_min"][1:7],
        daily["weather_code"][1:7],
    ):
        day = datetime.strptime(time_str, "%Y-%m-%d")
        daily_forecast.append({
            "day": day.strftime("%a"),
            "high": round(day_max),
            "low": round(day_min),
            "icon": WMO_ICON.get(code, "cloud"),
        })

    return {
        "location": "Burnaby, BC",
        "temperature": round(current["temperature_2m"]),
        "feels_like": round(current["apparent_temperature"]),
        "humidity": current["relative_humidity_2m"],
        "wind_speed": round(current["wind_speed_10m"]),
        "condition": WMO_CONDITIONS.get(current["weather_code"], "Unknown"),
        "icon": WMO_ICON.get(current["weather_code"], "cloud"),
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
        "hourly": upcoming,
        "daily": daily_forecast,
        "uv_index": round(daily["uv_index_max"][0]),
        "uv_category": uv_category(daily["uv_index_max"][0]),
    }
