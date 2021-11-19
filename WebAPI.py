# webapi.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Michael Yeung
# myeung2@uci.edu
# 71598323

from abc import ABC, abstractmethod
from urllib import request,error
import urllib,json
import sys

class WebAPI(ABC):
  def _download_url(self, url_to_download: str) -> dict:
    #TODO: Implement web api request code in a way that supports ALL types of web APIs
    response = None
    r_obj = None

    try: 
        url = url_to_download
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        headers = {'User-Agent': user_agent}
        request = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(request)
        #code_response = response.getcode()   #Error Handling, we receive response code
        #print(code_response)
        
        json_results = response.read()
        r_obj = json.loads(json_results)
        return r_obj
        
    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        sys.exit()

    except urllib.error.URLError as e:
      print('Failed to download contents of URL')
      sys.exit()

    finally:
        if response != None:
            response.close()
	
  def set_apikey(self, apikey:str) -> None:
    self.apikey = apikey 
    
  @abstractmethod
  def load_data(self):
    pass
	
  @abstractmethod
  def transclude(self, message:str) -> str:
    pass
