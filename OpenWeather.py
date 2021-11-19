# openweather.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Michael Yeung
# myeung2@uci.edu
# 71598323

#APIKEY de81f1cd5761b067f3b3625d8d635530

import urllib, json
from urllib import request,error
from WebAPI import WebAPI
class OpenWeather(WebAPI):
    def __init__(self, zipcode=None, ccode=None):
        self.zipcode = zipcode
        self.ccode = ccode
        self.apikey = ''
        self.description = ''
        self.temperature = ''
        self.high_temperature = ''
        self.low_temperature = ''
        self.longitude = ''
        self.latitude = ''
        self.humidity = ''
        self.city = ''
        self.sunset = ''

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}"
        
        weather_obj = self._download_url(url)
        #print('DEBUG\n', weather_obj, '\n') #debug
        if weather_obj is not None:
            self.description = weather_obj['weather'][0]['description']
            self.temperature = weather_obj['main']['temp']
            self.high_temperature = weather_obj['main']['temp_max']
            self.low_temperature = weather_obj['main']['temp_min']
            self.longitude = weather_obj['coord']['lon']
            self.latitude = weather_obj['coord']['lat']
            self.humidity = weather_obj['main']['humidity']
            self.city = weather_obj['name']
            self.sunset = weather_obj['sys']['sunset']
    
    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        return message.replace('@weather', self.description)
        
if __name__ == '__main__':
    pass