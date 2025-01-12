import requests
import environ
import json

# taking the value from env variable
env= environ.Env()
api_key= env('weatherapi')

url= f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=kathmandu&days=1'

def morning_result():
    response= requests.get(url=url)
    result=json.loads(response.text)
    current_condition= result['current']
    Current_temp= current_condition['temp_c']
    current_condition_text= current_condition['condition']['text']
    sunrise=result['forecast']['forecastday'][0]['astro']['sunrise']
    sunset=result['forecast']['forecastday'][0]['astro']['sunset']
    # print(current_condition_text)
    # print(Current_temp)
    # print(sunrise)
    # print(sunset)
    data={
        "current_condition_text":current_condition_text,
        "current_temp":Current_temp,
        "sunrise":sunrise,
        "sunset":sunset
    }
    # print(data)
    return data

result=morning_result()
# print("@@@@",result)