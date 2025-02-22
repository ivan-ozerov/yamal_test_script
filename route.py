class Route:
    
    def __init__(self, route_params):
        self.coefficient = route_params['coefficient']
        self.profitability_percent_arg = route_params["Рентабельность %"]
        self.coverage_fixed_costs_arg = route_params["% покрытия постоянных расходов"]
        self.coverage_fixed_min_costs_arg = route_params["% покрытия постоянных расходов (для расчета минимальной стоимости)"]