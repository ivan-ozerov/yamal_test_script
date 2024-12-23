import json
import math
import os
from pprint import pprint
from flight import Flight
from route import Route
from flight_calc import FlightCalc
from aircraft_type import AircraftType
from tests.test_data1 import test_data


tests_path = "./tests"


def get_tax_value(calc_arr_or_dep, calc_name, data, business_taxes):
    if calc_arr_or_dep == "departure_calcs":
        tax_value = data["airport_taxes_departure"][calc_name]
    elif calc_arr_or_dep == "arrival_calcs":
        tax_value = data["airport_taxes_arrival"][calc_name]
    elif calc_arr_or_dep == "business_calcs":
        tax_value = business_taxes[calc_name]
    return tax_value


def calculate_taxes(flight, groups_calcs, flight_params, route_params, aircraft_type):
    result_dict = {}

    for calc_group_name, groups in groups_calcs.items():
        result_dict[calc_group_name] = {}
        for group_name, calc_names in groups.items():
            for calc_name in calc_names:
                calc_result = 0
                tax_value = get_tax_value(
                    calc_group_name,
                    calc_name,
                    flight["flight_taxes"],
                    aircraft_type.business_taxes,
                )

                flight_calc = FlightCalc()
                method_name = getattr(flight_calc, group_name)
                calc_result = method_name(
                    **(
                        flight_params.__dict__
                        | {"tax": tax_value}
                        | {"max_load": aircraft_type.max_load}
                        | {"crew_count": aircraft_type.crew_count}
                        | route_params.__dict__
                    )
                )
                calc_result = round(calc_result, 2)
                if calc_name not in result_dict[calc_group_name]:
                    result_dict[calc_group_name][calc_name] = calc_result
                else:
                    result_dict[calc_group_name][calc_name] += calc_result
                # if calc_name == 'Сбор за пользование аэровокзала':
                #     print(calc_name, calc_name, data)

    return result_dict


# def variable_calcs(data, flight_params, route_params, aircraft_type):
#     # print(calc_name, tax_value, calc_result, flight.passengers_count)
#     calculate_taxes
#     return result, result_dict

# def business_calcs(data):
#     flight = Flight(data['flights']['1']['flight_params'])
#     route = Route(data['route_params'])
#     aircraft_type = AircraftType(flight.plane_type)
#     result = 0
#     result_dict = {}


# def calc_all_


def make_all_tests():
    all_tests_results = {}
    for test_case in test_data:
        for route in test_data['routes']:
        test_case_results = {}
        flight_results = {}
        route_params = Route(test_case["route_params"])
        for flight_key, flight_value in test_case["flights"].items():
            flight_params = Flight(flight_value["flight_params"])
            aircraft_type = AircraftType(flight_params.plane_type)
            flight_result = calculate_taxes(
                flight_value,
                test_case["groups"],
                flight_params,
                route_params,
                aircraft_type,
            )
            arrival_calcs = round(sum(flight_result["arrival_calcs"].values()), 2)
            departure_calcs = round(sum(flight_result["departure_calcs"].values()), 2)
            fixed_calcs = round(sum(flight_result["business_calcs"].values()), 2)
            variable_calcs = arrival_calcs + departure_calcs
            contingency = round(variable_calcs * 0.05)
            flight_total_calcs = variable_calcs + fixed_calcs + contingency
            flight_calcs_results = {
                f"flight {flight_key}": {
                    "var_result": variable_calcs,
                    "fix_result": fixed_calcs,
                    "contingency": contingency,
                    "total": flight_total_calcs,
                    "flight": flight_result,
                }
            }
            flight_results.append(flight_calcs_results)
            route_results[] = flight_results
        
            # pprint(flight_result)
        # result = 0
        save_results_to_file(flight_results)


def save_results_to_file(text):
    with open("output.json", "w") as file:
        json.dump(text, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    make_all_tests()
