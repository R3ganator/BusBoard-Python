import pprint
import requests
from constants import *


def get_postcode():
    code = input('What postcode do you want to check bus times for?:\n')
    while True:
        try:
            check(code)
            return code
        except ValueError:
            print('Invalid post code, please try again.')
            code = input('What postcode do you want to check bus times for?:\n')


def check(code):
    p_check = requests.get(
        f'https://api.postcodes.io/postcodes/{code}')
    error_check = p_check.json()
    if 'error' in error_check:
        raise ValueError


def get_atcocode(postcode):
    p = requests.get(f'http://api.postcodes.io/postcodes/{postcode}')
    p_response = p.json()
    result = p_response['result']
    latitude = result['latitude']
    longitude = result['longitude']
    a = requests.get(
        f'https://transportapi.com/v3/uk/places.json?app_id={appId}&app_key={appKey}&lat={latitude}&lon={longitude}&type=bus_stop&limit=2')
    a_response = a.json()
    member = a_response['member']
    atcocode = []
    for bus_stop in member:
        atcocode.append(bus_stop['atcocode'])
    return atcocode


class Buses:
    departure_time = []
    direction = []
    number = []

    def timetable(self, departures):
        for all_buses in departures:
            bus_list = departures[all_buses]
            for bus in bus_list:
                self.number.append(bus['line'])
                self.departure_time.append(bus['expected_departure_time'])
                self.direction.append(bus['direction'])

    def printer(self):
        line = '--' * 20
        print(f'{line}')
        for i in range(5):
            print(f'{self.number[i]:<5} | {self.direction[i]:<20} | {self.departure_time[i]}')


def main():
    print("Welcome to BusBoard.")
    user_input = get_postcode()
    # user_input = 'nw1 2hs'
    atcocode = get_atcocode(user_input)
    for i in atcocode:
        r = requests.get(f'http://transportapi.com/v3/uk/bus/stop/{i}/live.json?app_id={appId}&app_key={appKey}&group=no')
        r_response = r.json()
        departures = r_response["departures"]
        timetables = Buses()
        timetables.timetable(departures)
        timetables.printer()


if __name__ == "__main__":
    main()