import json
from pprint import pprint
from flight import Flight
from route import Route
from flight_calc import FlightCalc
from aircraft_type import AircraftType
from tests.test_data1 import test_data

def test():
    file_path = "./tests/test1.json"   

    # with open(file_path, 'rb') as file:
    #     data = json.load(file)
    
    data = test_data
    flight = Flight(data['flights']['1']['flight_params'])
    route = Route(data['route_params'])
    aircraft_type = AircraftType(flight.plane_type)
    result = 0
    result_dict = {}
    
    for group_name, taxes in data['flights']['1']['flight_taxes']["airport_taxes_departure"].items():
        for tax in taxes.items():
            tax_result = 0
            flight_calc = FlightCalc()
            method = getattr(flight_calc, group_name)
            tax_result = method(**(flight.__dict__ | 
                                   {"tax" : tax[1]} | 
                                   {"max_load" : aircraft_type.max_load} |
                                   {"crew_count" : aircraft_type.crew_count} | 
                                   route.__dict__))
            result_dict[tax[0]] = tax_result
            result += tax_result
    
    return result, result_dict


        
if __name__ == '__main__':
    # print("variable expenses: ")
    # pprint(test()[0])
    # print("variable expenses detailed: ")
    # pprint(test()[1])
    # print("fixed expenses detailed: ")
    text = test()[1]
    # with open('output.txt', 'w', encoding='utf-8') as file:
    #     file.write(text)
    with open('output.json', 'w') as file:
        json.dump(text, file, indent=4, ensure_ascii=False)