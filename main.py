import requests
from datetime import date, timedelta
from json import dumps, loads, JSONDecodeError

print("*** Obsługa biblioteki zewnętrznej ***")


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

    def read_file(self, path_file):
        try:
            with open(path_file) as file_stream:
                self.file = file_stream.read()

            if not self.file:
                self.file = {}
            else:
                self.file = loads(self.file)
        except FileNotFoundError:
            print("Nie znaleziono pliku z historią.")
        except JSONDecodeError as e:
            print(f"Wystąpił nieoczekiwany błąd {e}.")

# TODO Zweryfikuj przydatność tych zapisów, szczególnie z try-except

    def write_file(self, path_file, file):
        with open(path_file, "w") as file_stream:
            file_stream.write(dumps(file))

    def request_to_API(self, latitude, longtitude):
        latitude = "51.248258"  # Szerokość geograficzna
        longitude = "22.535016"  # Długość geograficzna
        URL = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude" \
              f"={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&" \
              f"start_date={searched_date}&end_date={searched_date}"
        data = requests.get(URL)
        data_dict = data.json()


day_from_user = input("Podaj dzień, dla którego chcesz sprawdzić pogodę (YYYY-mm-dd): ")

try:
    day_from_user = date.fromisoformat(day_from_user)
    day_from_user = str(day_from_user)
except ValueError:
    day_from_user = None

if day_from_user:
    searched_date = day_from_user
else:
    searched_date = str(date.today() + timedelta(days=1))
    print(f"Jako datę przyjęto jutrzejszy dzień: {searched_date}")

weather_forecast = WeatherForecast(searched_date)









# print(weather_forecast[date])
# print(next(weather_forecast.items()))
# for item in weather_forecast:
#     print(item)


#
# if searched_date in history_weather_forecast:
#     rain_sum = history_weather_forecast[searched_date]
# else:
#
#
#     data_dict = data.json()
#     try:
#         rain_sum = data_dict['daily']['rain_sum'][0]
#     except KeyError:
#         rain_sum = None
#
#     if rain_sum is None:
#         print("Nie wiem")
#         exit()
#
#     history_weather_forecast[searched_date] = rain_sum
#
# print(f"Data prognozy pogody: {searched_date}.")
# if rain_sum > 0:
#     print("Będzie padać.")
# elif rain_sum == 0:
#     print("Nie będzie padać.")
# else:
#     print("Nie wiem.")
