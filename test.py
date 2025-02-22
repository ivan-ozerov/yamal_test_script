import json
import math
import os
from pprint import pprint
from flight import Flight
from route import Route
from flight_calc import FlightCalc
from aircraft_type import AircraftType
from tests.test_data1 import test_data
from taxes_mapping import taxes_agregates_mapping
from taxes_mapping import taxes_groups_mapping


tests_path = "./tests"


def get_tax_value(calc_arr_or_dep, calc_name, data, business_taxes):
    if calc_arr_or_dep == "departure_calcs":
        tax_value = data["airport_taxes_departure"][calc_name]
    elif calc_arr_or_dep == "arrival_calcs":
        tax_value = data["airport_taxes_arrival"][calc_name]
    elif calc_arr_or_dep == "business_calcs":
        tax_value = business_taxes[calc_name]
    return tax_value


def calculate_taxes(flight, flight_params, route_params, aircraft_type):
    result_dict = {}

    for calc_group_name, calc_name in taxes_agregates_mapping.items():
        result_dict[calc_group_name] = {}
        calc_result = 0
        tax_value = get_tax_value(
            calc_group_name,
            calc_name,
            flight["flight_taxes"],
            aircraft_type.business_taxes,
        )
        for group, calc_names_in_groups in taxes_groups_mapping:
            if calc_name in calc_names_in_groups:
                group_name = group
            else:
                print("we cant find corrsponding group")
                exit(1)
        flight_calc = FlightCalc()
        method_name = getattr(flight_calc, group_name)
        calc_result = method_name(
            **(
                flight_params.__dict__
                | {"tax": tax_value}
                | {"max_load": aircraft_type.max_load}
                | {"crew_count": aircraft_type.crew_count}
                | {"taxes": flight["flight_taxes"]}
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

def make_flight_calcs(flight_taxes_calcs, flight_key, flight_params):
    arrival_calcs = round(sum(flight_taxes_calcs["arrival_calcs"].values()), 2)
    departure_calcs = round(sum(flight_taxes_calcs["departure_calcs"].values()), 2)
    fixed_calcs = round(sum(flight_taxes_calcs["business_calcs"].values()), 2)
    variable_calcs = arrival_calcs + departure_calcs
    contingency = round(variable_calcs * 0.05)
    flight_total_calcs = variable_calcs + fixed_calcs + contingency
    business_taxes_variables = [
        'Заработная плата  летного состава и бортпроводников (переменная часть)',
        'Технические резервы (переменная часть)',
        'Прочие переменные расходы (бортпитание, трансфер,гостиница, командировки, агенты)'
    ]
    flight_hour_cost_calc = 0
    for tax in business_taxes_variables:
        flight_hour_cost_calc += flight_taxes_calcs['departure_calcs'][tax]
    flight_hour_cost_calc += fixed_calcs
    flight_hour_cost_calc /= flight_params.flight_time
    result_dict = {
        "Переменные расходы": variable_calcs,
        "Постоянные расходы": fixed_calcs,
        "Непредвиденные расходы": contingency,
        "Итого плановые расходы": flight_total_calcs,
        "Ставка летного часа": flight_hour_cost_calc
    }
    return result_dict

def make_route_calcs(flights_results):
    route_results = {}
    for flight_results in flights_results:
        for tax, value in flight_results.items():
            if tax in route_results:
                route_results[tax] += value
            else:
                route_results[tax] = 0
                route_results[tax] = route_results[tax] + value
    return route_results["Ставка летного часа"]/len(flight_results)

def make_route_output(route_results, route_params):
    flight_hour_cost_total_calc = route_results["Ставка летного часа"]
    expenses_var_total_calc = route_results["Переменные расходы"]
    fixed_expenses_total_calc = route_results["Постоянные расходы"]
    contingency_total_calc = route_results["Непредвиденные расходы"]
    profitability_percent_arg = route_params.profitability_percent_arg
    coverage_fixed_min_costs_arg = route_params.coverage_fixed_min_costs_arg
    coverage_fixed_costs_arg = route_params.coverage_fixed_costs_arg
    total_expenses = expenses_var_total_calc + fixed_expenses_total_calc + contingency_total_calc
    total_expenses_excluding_vat_calc = total_expenses + total_expenses*profitability_percent_arg/100

    
    # route_parameters = {
    #     "Ставка летного часа, руб." : flight_hour_cost_total_calc,
    #     "Переменные расходы, руб." : expenses_var_total_calc,
    #     "Постоянные расходы, руб." : fixed_expenses_total_calc,
    #     "Непредвиденные расходы, руб." : contingency_total_calc,
    #     "Рентабельность %" : profitability_percent_arg,
    #     "Итого плановые расходы (без НДС), руб." : total_expenses_excluding_vat_calc,
    #     "% покрытия постоянных расходов (для расчета минимальной стоимости)" : coverage_fixed_min_costs_arg,
    #     "Минимальная стоимость для покрытия расходов без НДС" : min_cost_excluding_vat_calc,
    #     "% покрытия постоянных расходов" : coverage_fixed_costs_arg,
    #     "Рентабельность, руб." : profitability_calc,
    #     "Минимальная стоимость рейса с учетом рентабельности (без НДС, руб.)" :min_cost_excluding_vat_including_profitability,
    #     "Стоимость рейса без НДС, руб." : total_expenses_excluding_vat_calc,
    #     "Ставка НДС,%" : vat,
    #     "Сумма НДС, руб." : vat_sum,
    #     "Стоимость блок часа без НДС" : block_hour_cost_total_calc,
    #     "Стоимость блок часа с НДС" : block_hour_cost_total_excluding_vat_calc
    # }
    
    
    

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
        test_case_results = {}
        for route in test_case['routes'].values():
            flights_results = []
            route_results = {}
            route_params = Route(route["route_params"])
            flights_params = []
            for flight_key, flight_value in route["flights"].items():
                flight_params = Flight(flight_value["flight_params"])
                aircraft_type = AircraftType(flight_params.plane_type)
                flight_taxes_calcs = calculate_taxes(
                    flight_value,
                    flight_params,
                    route_params,
                    aircraft_type,
                )
                flights_params.append(flight_params)
                flight_calc_results = make_flight_calcs(flight_taxes_calcs, flight_key, flight_params)
                # flight_calc_output = {
                #     f"flight {flight_key}": {
                #     }
                # }
                # flight_calc_output[f"flight {flight_key}"].update(flight_calcs_results)
                # flight_results.update(flight_calc_output)
                flights_results.append(flight_calc_results)
            route_results = make_route_calcs(flights_results)
            route_output = make_route_output(route_results, route_params)
            save_results_to_file(flights_results, 'flight_results')
            save_results_to_file(route_results, 'route_results')
            # result = 0
        
            # pprint(flight_result)


def save_results_to_file(text, file_name):
    with open(f"{file_name}.json", "w", encoding='utf-8') as file:
        json.dump(text, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    make_all_tests()
