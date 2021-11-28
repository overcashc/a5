from OpenWeather import OpenWeather
from a4 import test_api

zipcode = "92697"
ccode = "US"
apikey = "de81f1cd5761b067f3b3625d8d635530"

open_weather = OpenWeather(zipcode, ccode)
open_weather.set_apikey(apikey)
open_weather.load_data()

print(f"The temperature for {zipcode} is {open_weather.temperature} degrees")
print(f"The high for today in {zipcode} will be {open_weather.high_temperature} degrees")
print(f"The low for today in {zipcode} will be {open_weather.low_temperature} degrees")
print(f"The coordinates for {zipcode} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
print(f"The current weather for {zipcode} is {open_weather.description}")
print(f"The current humidity for {zipcode} is {open_weather.humidity}")
print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")
print(test_api("Hello World! Today is the first day of the rest of my life. It is @weather and the best day of my life", apikey, open_weather))