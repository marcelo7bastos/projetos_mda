import requests 
import json 
from datetime import datetime 
import os 

# API Params
url = "https://weatherapi-com.p.rapidapi.com/current.json"

#querystring = {"q":"53.1,-0.13"}
querystring = {"q":"London"}

headers = {
	"x-rapidapi-key": "4b42f377a2msh07cef5247dc90d4p18a597jsn8b8ad421bf3f",
	"x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
}


try:
    response = requests.get(url, headers=headers, params=querystring)    
    if response.status_code == 200: 
        # get the json data 
        json_data = response.json() 
        file_name = str( datetime.now().date() ) + '.json' 
        tot_name = os.path.join( os.path.dirname( __file__ ), 'data', file_name ) 

        with open( tot_name, 'w' ) as outputfile: 
            json.dump( json_data, outputfile ) 
    
    else: 
        print( response.status_code ) 
        print( 'Error in API call.' )

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
