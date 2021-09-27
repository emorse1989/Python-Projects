#Import modules for API requests, datetime translation, and time delay
import requests
import datetime
from time import sleep

#Designate global variable to make including the degree symbol simpler
degree_sign = u'\N{DEGREE SIGN}'

#Really long function to translate wind degrees into a compass direction
def wind_direction(wind):
    if wind in range(0,11):
        return 'N'
    elif wind in range(11,34):
        return 'NNE'
    elif wind in range(34,56):
        return 'NE'
    elif wind in range(56,79):
        return 'ENE'
    elif wind in range(79,101):
        return 'E'
    elif wind in range(101,124):
        return 'ESE'
    elif wind in range(124,146):
        return 'SE'
    elif wind in range(146,169):
        return 'SSE'
    elif wind in range(169,191):
        return 'S'
    elif wind in range(191,214):
        return 'SSW'
    elif wind in range(214,236):
        return 'SW'
    elif wind in range(236,259):
        return 'WSW'
    elif wind in range(259,281):
        return 'W'
    elif wind in range(281,304):
        return 'WNW'
    elif wind in range(304,326):
        return 'NW'
    elif wind in range(326,349):
        return 'NNW'
    elif wind in range(349,360):
        return 'N'

#receives dictionary from api request
def weather_summary(weather):
    print(f"\nRetrieving weather information for {weather['name'].title()}...\n")
    sleep(2)    
    print(f"Current conditions: {weather['weather'][0]['description'].title()}")
    print(f"Current temperature: {round(weather['main']['temp'])}{degree_sign}F")
    print(f"Feels like: {round(weather['main']['feels_like'])}{degree_sign}F")
    sunrise = int((weather['sys']['sunrise'])) + 14400 + int((weather['timezone']))
    sunrise = datetime.datetime.fromtimestamp(sunrise)
    print(f"Sunrise: {sunrise:%Y-%m-%d %H:%M:%S} local time")
    sunset = int((weather['sys']['sunset'])) + 14400 + int((weather['timezone']))
    sunset = datetime.datetime.fromtimestamp(sunset)
    print(f"Sunset: {sunset:%Y-%m-%d %H:%M:%S} local time")
    print(f"Wind Speed: {round(weather['wind']['speed'])} MPH")
    wind_dir = wind_direction(weather['wind']['deg'])
    print(f"Wind Direction: {wind_dir}\n")

#makes API request using ZIP and returns JSON response as a dictionary
def zip_request(zip_code):
    weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?zip={zip_code}'
                           '&units=imperial&appid=a044db901da46a189dae54efbc282ea6')
    weather = weather.json()
    weather = dict(weather)
    if weather['cod'] != 200:
            print("\nOops! Something went wrong. Please re-enter zip information.\n")
            zip_input()
    else:
        return weather
    
#makes API request using city/state/country and returns JSON response as a dictionary
def city_request(city, country, state):
    if state:
        weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{state},'+
                               f'{country}&units=imperial&appid=a044db901da46a189dae54efbc282ea6')
        weather = weather.json()
        weather = dict(weather)
        if weather['cod'] != 200:
            print("\nOops! Something went wrong. Please re-enter city information.\n")
            city_input()
        else:
            return weather
    else:
        weather = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}'+
                               '&units=imperial&appid=a044db901da46a189dae54efbc282ea6')
        weather = weather.json()
        weather = dict(weather)
        if weather['cod'] != 200:
            print("\nOops! Something went wrong. Please re-enter city information.\n")
            city_input()
        else:
            return weather

#takes ZIP code and runs api request and returns weather summary
def zip_input():
    location_zip = input('\nPlease enter a 5-digit ZIP code: ')
    if len(location_zip) == 5:
        weather = zip_request(location_zip)
        weather_summary(weather)
    else:
        print("\nInvalid input. Please try again.\n")
        zip_input()

#determines if city is inside or outside US, then runs the api request and returns weather summary
def city_input():
    in_us = input("Is your location inside the United States? (y/n): ").lower()
    if in_us == 'yes' or in_us == 'y':    
        location_city = input('Enter the name of the city: ')
        location_state = input('Enter the 2-letter state code: ').lower()
        location_country = 'US'
        weather = city_request(location_city, location_country, location_state)
        weather_summary(weather)
    elif in_us == 'no' or in_us == 'n':
        location_city = input('Enter the name of the city: ')
        location_country = input('Enter the 2-letter country code: ')
        location_state = ''
        weather = city_request(location_city, location_country, location_state)
        weather_summary(weather)

#displays fancy title and asks user to pick location type
def menu():
    print(''' _    _ _           _   _      ___  ___        _    _            _   _             ___  
| |  | | |         | | ( )     |  \/  |       | |  | |          | | | |           |__ \ 
| |  | | |__   __ _| |_|/ ___  | .  . |_   _  | |  | | ___  __ _| |_| |__   ___ _ __ ) |
| |/\| | '_ \ / _` | __| / __| | |\/| | | | | | |/\| |/ _ \/ _` | __| '_ \ / _ \ '__/ / 
\  /\  / | | | (_| | |_  \__ \ | |  | | |_| | \  /\  /  __/ (_| | |_| | | |  __/ | |_|  
 \/  \/|_| |_|\__,_|\__| |___/ \_|  |_/\__, |  \/  \/ \___|\__,_|\__|_| |_|\___|_| (_)  
                                        __/ |                                           
                                       |___/                                            
****************************************************************************************

         WELCOME TO "WHAT'S MY WEATHER?" - THE WEATHER APP
         
****************************************************************************************''')
    retry = 'yes'
    while retry == 'yes' or retry == 'y':
        location_mode = input('Lookup Type - Enter "Zip" or "City": ')
        if location_mode.lower() == 'zip':
            zip_input()
            retry = 'n'
        elif location_mode.lower() == 'city':
            city_input()
            retry = 'n'
        else:
            print("\nInput not recognized. Please try again.\n")

#creates a while loop, opens the menu, and asks user to retry after getting their weather summary, also closes program if retry is no
def main():
    global_retry = 'yes'
    while global_retry.lower() == 'yes' or global_retry.lower() == 'y':    
        menu()
        global_retry = input("Would you like to look up another location? (y/n): ")
    if global_retry.lower() == 'no' or global_retry.lower() == 'n':
        input('\nThank you for using "What\'s My Weather?". Press enter to exit the program.')
        quit()
    else:
        print("Invalid input. Please try again.")

#starts the program
main()

    