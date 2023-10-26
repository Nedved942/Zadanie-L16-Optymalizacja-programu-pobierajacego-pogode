import requests
from datetime import date, timedelta
from json import dumps, loads, JSONDecodeError

print("*** Obsługa biblioteki zewnętrznej - wersja zoptymalizowana ***")


class WeatherForecast:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def __getitem__(self, item):
        return self.weather_data[item]

    def __setitem__(self, key, value):
        self.weather_data[key] = value

    def __iter__(self):
        return iter(self.weather_data.keys())

    def items(self):
        return ((key, value) for key, value in self.weather_data.items())

    def write_file(self, path_file):
        with open(path_file, "w") as file_stream:
            file_stream.write(dumps(self.weather_data))

    @staticmethod
    def request_to_api(latitude, longitude, searched_date):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude" \
              f"={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&" \
              f"start_date={searched_date}&end_date={searched_date}"
        data = requests.get(url)
        data_dict = data.json()
        try:
            return data_dict['daily']['rain_sum'][0]
        except KeyError:
            print("Uwaga: Nie ma podanej wartości opadów dla danego dnia.")
            return None


def read_file(path_file):
    try:
        with open(path_file) as file_stream:
            history_weather_forecast = file_stream.read()

        if not history_weather_forecast:
            return {}
        else:
            return loads(history_weather_forecast)
    except FileNotFoundError:
        print("Nie znaleziono pliku z historią.")
    except JSONDecodeError as e:
        print(f"Wystąpił nieoczekiwany błąd {e}.")


def return_correct_date(date_to_check):
    try:
        date_to_check = date.fromisoformat(date_to_check)
        date_to_check = str(date_to_check)
    except ValueError:
        date_to_check = None

    if date_to_check:
        return date_to_check
    else:
        tomorrow_day = str(date.today() + timedelta(days=1))
        print(f"Jako datę przyjęto jutrzejszy dzień: {tomorrow_day}")
        return tomorrow_day


def is_it_rain(sum_of_rain):
    if sum_of_rain is None:
        print("Nie wiadomo czy będzie padać.")
    elif sum_of_rain > 0:
        print("Będzie padać.")
    elif sum_of_rain == 0:
        print("Nie będzie padać.")


day_from_user = input("Podaj dzień, dla którego chcesz sprawdzić pogodę (YYYY-mm-dd): ")
searched_date = return_correct_date(day_from_user)
latitude = "51.248258"  # Szerokość geograficzna
longitude = "22.535016"  # Długość geograficzna
path_history_file = "history_weather_forecast.json"

weather_forecast = WeatherForecast(read_file(path_history_file))

if searched_date in weather_forecast:
    rain_sum = weather_forecast[searched_date]
else:
    rain_sum = WeatherForecast.request_to_api(latitude, longitude, searched_date)
    weather_forecast[searched_date] = rain_sum
    weather_forecast.write_file(path_history_file)

is_it_rain(rain_sum)

# Wywołanie metod magicznych
print(weather_forecast.weather_data)
print(weather_forecast["2023-10-24"])
weather_forecast["2023-10-24"] = 13.7
print(weather_forecast["2023-10-24"])
weather_data_generator = weather_forecast.items()
print(next(weather_data_generator))
print(next(weather_data_generator))

for item in weather_forecast:
    print(item)
