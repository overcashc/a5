# lastfm.py

# Starter code for assignment 4 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Michael Yeung
# myeung2@uci.edu
# 71598323

#APIKEY 33f7f26663017ea24945be21492594b2

import urllib, json
from urllib import request,error
from WebAPI import WebAPI

class LastFM(WebAPI):
    def __init__(self):
        self.apikey = ''
        self.topartist = ''

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        url = f"http://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&api_key={self.apikey}&format=json"
        #chart.gettopartist
        lastfm_obj = self._download_url(url)
        self.topartist = lastfm_obj['artists']['artist'][0]['name']

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        return message.replace('@lastfm', self.topartist)
if __name__ == '__main__':
    pass