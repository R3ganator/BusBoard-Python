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
    def __init__(self):
        self.buses = []

    def timetable(self, departures):
        counter = 0
        keep_running = True
        for all_buses in departures:
            bus_list = departures[all_buses]
            while keep_running:
                for bus in bus_list:
                    if counter == 5:
                        keep_running = False
                        break
                    number = bus['line']
                    time = bus['aimed_departure_time']
                    direction = bus['direction']
                    self.buses.append(f'Bus number {number} headed to {direction} departing at {time}')
                    counter += 1
        return self.buses


def getTimetable(atcocode):
    # for i in atcocode:
    r = requests.get(f'http://transportapi.com/v3/uk/bus/stop/{atcocode}/live.json?app_id={appId}&app_key={appKey}&group=no&limit=2')
    r_response = r.json()
    stop = BusStop(r_response)
    stop.departures()
    stop.name()
    return stop


class BusStop:
    def __init__(self, data):
        self.data = data
        self.info = []
        self.stop_name = ''

    def name(self):
        self.stop_name = self.data['stop_name']
        return self.stop_name

    def departures(self):
        departures = self.data['departures']
        timetables = Buses()
        self.info.append(timetables.timetable(departures))
        return self.info


def main():
    print("Welcome to BusBoard.")
    user_input = get_postcode()
    atcocode = get_atcocode(user_input)
    for i in atcocode:
        stop = getTimetable(i)
        print(f'Bus information for {stop.stop_name}')
        for list in stop.info:
            for bus in list:
                print(f'{bus}')


if __name__ == "__main__":
    main()