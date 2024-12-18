import json
import os
from pprint import pprint
from flight import Flight
from route import Route
from flight_calc import FlightCalc
from aircraft_type import AircraftType
from tests.test_data1 import test_data


tests_path = "./tests"

def test(data):
    flight = Flight(data['flights']['1']['flight_params'])
    route = Route(data['route_params'])
    aircraft_type = AircraftType(flight.plane_type)
    result = 0
    result_dict = {}
    
    for calc_arr_or_dep, groups in data['groups'].items():
        for group_name, calc_names in groups.items():
            for calc_name in calc_names:
                calc_result = 0
                if calc_arr_or_dep == 'departure_calcs':
                    tax_value = data['flights']['1']['flight_taxes']['airport_taxes_departure'][calc_name]
                elif calc_arr_or_dep == 'arrival_calcs':
                    tax_value = data['flights']['1']['flight_taxes']['airport_taxes_arrival'][calc_name]
                elif calc_arr_or_dep == 'business_calcs':
                    tax_value = data['flights']['1']['flight_taxes']['business_taxes'][calc_name]

                flight_calc = FlightCalc()
                method_name = getattr(flight_calc, group_name)
                calc_result = method_name(**(flight.__dict__ | 
                                   {"tax" : tax_value} | 
                                   {"max_load" : aircraft_type.max_load} |
                                   {"crew_count" : aircraft_type.crew_count} |
                                   route.__dict__))
                if calc_name not in result_dict:
                    result_dict[calc_name] = calc_result
                else:
                    result_dict[calc_name] += calc_result
                if calc_name == 'Сбор за пользование аэровокзала':
                    print()
                print(calc_name, tax_value, calc_result, flight.passengers_count)
                result += calc_result

    return result, result_dict

def make_all_tests():
    for test_case in test_data:
        result = test(test_case)
        save_results_to_file(result)
    
def save_results_to_file(text):
    with open('output.json', 'a') as file:
        json.dump(text, file, indent=4, ensure_ascii=False)
        
if __name__ == '__main__':
    make_all_tests()
    