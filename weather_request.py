#Import modules for API requests, datetime translation, and time delay
import requests
import datetime
from time import sleep

#Designate global variable to make including the degree symbol simpler
degree_sign = u'\N{DEGREE SIGN}'

def wind_direction(wind):
    '''Converts wind angle value into compass direction'''
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

def weather_summary(weather):
    '''receives dictionary from api request and outputs formatted summary using dictionary keys'''
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

def api_request(url, tries):
    '''Uses try block to issue api call to openweather.org'''
    try:
        weather = requests.get(url)
    except TimeoutError:
        print("The connection timed out. Retrying...")
        sleep(1)
        tries += 1
        if tries == 5:
            print("Unable to retrieve weather data. Returning to main menu.")
            menu()
        else:
            api_request(url, tries)
    except BaseException:
        print("Something has gone wrong. Retrying...")
        sleep(1)
        tries += 1
        if tries == 5:
            print("Connection unsuccessful. Returning to main menu.")
            menu()
        else:
            api_request(url, tries)        
    weather = weather.json()
    if weather['cod'] != 200:
        print(f"Something went wrong!\nError Code: {weather['cod']}\n"+
            f"Error Message: {weather['message']}\nReturning to main menu.")
        menu()
    else:
        return weather

def zip_input():
    '''takes ZIP code and runs api request and returns weather summary'''
    location_zip = input('\nPlease enter a 5-digit ZIP code: ')
    if len(location_zip) == 5:
        url = f'http://api.openweathermap.org/data/2.5/weather?zip={location_zip}&units=imperial&appid=a044db901da46a189dae54efbc282ea6'
        print(url)
        input()
        tries = 0
        weather = api_request(url, tries)
        weather_summary(weather)
    else:
        print("\nInvalid input. Please try again.\n")
        zip_input()

def city_input():
    '''determines if city is inside or outside US, then runs the api request and returns weather summary'''
    in_us = input("Is your location inside the United States? (y/n): ").lower()
    if in_us == 'yes' or in_us == 'y':    
        city = input('Enter the name of the city: ')
        state = input('Enter the 2-letter state code: ').lower()
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{state},US&units=imperial&appid=a044db901da46a189dae54efbc282ea6'
        tries = 0
        weather = api_request(url, tries)
        weather_summary(weather)
    elif in_us == 'no' or in_us == 'n':
        city = input('Enter the name of the city: ')
        country = input('Enter the 2-letter country code: ')
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city},{country}&units=imperial&appid=a044db901da46a189dae54efbc282ea6'
        tries = 0
        weather = api_request(url, tries)
        weather_summary(weather)
    else:
        print("Invalid input. Answer yes or no.")
        city_input()

def menu():
    '''displays fancy title and asks user to pick location type'''
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
        location_mode = input('(ENTER Q TO QUIT PROGRAM)\nLookup Type - Enter "Zip" or "City": ')
        if location_mode.lower() == 'zip':
            zip_input()
            retry = 'n'
        elif location_mode.lower() == 'city':
            city_input()
            retry = 'n'
        elif location_mode.lower() == 'q':
            input('\nThank you for using "What\'s My Weather?". Press enter to exit the program.')
            quit()
        else:
            print("\nInput not recognized. Please try again.\n")

def main():
    '''creates a while loop, opens the menu, and asks user to retry after 
    getting their weather summary also closes program if retry is no'''
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

    