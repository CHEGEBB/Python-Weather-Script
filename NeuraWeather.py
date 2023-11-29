import requests
from rich.console import Console
from rich.progress import Progress
from rich.prompt import Prompt
import time

console = Console()

def get_weather(api_key, city, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Error fetching weather data: {e}[/red]")
        return None

def display_loading_animation():
    with Progress() as progress:
        task = progress.add_task("[cyan]Fetching weather data...", total=10)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(0.1)

def display_weather(weather_data, units):
    if weather_data is None:
        return

    if "cod" in weather_data and weather_data["cod"] == "404":
        console.print("[red]City not found. Please check the city name.[/red]")
        return

    city = weather_data.get("name", "Unknown City")
    temperature = weather_data["main"]["temp"] if "main" in weather_data else "Unknown Temperature"
    description = weather_data["weather"][0]["description"] if "weather" in weather_data and len(weather_data["weather"]) > 0 else "Unknown Description"

    unit_label = "C" if units == "metric" else "F"
    styled_output = f"[cyan]{city}[/cyan]\n[green]{temperature}°{unit_label}[/green]\n[blue]{description}[/blue]"
    console.print(styled_output)

def welcome_message():
    console.print("[bold cyan]Welcome to Weather App![/bold cyan]")
    console.print("Enter the city name to get the current weather.")
    console.print("Temperature will be displayed in Celsius.")

def main():
    api_key = "aaf06191d54d5d7adcf736c7380775ce"  # Replace with your actual API key

    welcome_message()

    city_name = Prompt.ask('Enter the city name: ')

    display_loading_animation()
    weather_data = get_weather(api_key, city_name)

    display_weather(weather_data, "metric")

if __name__ == "__main__":
    main()
