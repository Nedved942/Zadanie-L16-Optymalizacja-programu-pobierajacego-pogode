import requests
from datetime import date, timedelta
from json import dumps, loads, JSONDecodeError

print("*** Obsługa biblioteki zewnętrznej ***")

try:
    with open("history_weather_forecast.json") as file_stream:
        history_weather_forecast = file_stream.read()

        if not history_weather_forecast:
            history_weather_forecast = {}
        else:
            history_weather_forecast = loads(history_weather_forecast)
except FileNotFoundError:
    print("Nie znaleziono pliku z historią.")
except JSONDecodeError as e:
    print(f"Wystąpił nieoczekiwany błąd {e}.")

day_from_user = input("Podaj dzień, dla którego chcesz sprawdzić pogodę (YYYY-mm-dd): ")
# day_from_user = "2023-10-30"

try:
    day_from_user = date.fromisoformat(day_from_user)
    day_from_user = str(day_from_user)
except ValueError:
    day_from_user = None

if day_from_user:
    searched_date = day_from_user
else:
    searched_date = str(date.today() + timedelta(days=1))

if searched_date in history_weather_forecast:
    rain_sum = history_weather_forecast[searched_date]
else:
    latitude = "51.248258"  # Szerokość geograficzna
    longitude = "22.535016"  # Długość geograficzna
    URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude" \
          f"={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&" \
          f"start_date={searched_date}&end_date={searched_date}"
    data = requests.get(URL)
    data_dict = data.json()
    # pprint(data_dict)
    try:
        rain_sum = data_dict['daily']['rain_sum'][0]
    except KeyError:
        rain_sum = None

    if rain_sum is None:
        print("Nie wiem")
        exit()

    history_weather_forecast[searched_date] = rain_sum
    with open("history_weather_forecast.json", "w") as file_stream:
        file_stream.write(dumps(history_weather_forecast))

print(f"Data prognozy pogody: {searched_date}.")
if rain_sum > 0:
    print("Będzie padać.")
elif rain_sum == 0:
    print("Nie będzie padać.")
else:
    print("Nie wiem.")
