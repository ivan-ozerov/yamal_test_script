class FlightCalc:
    
    @staticmethod
    def group_1(tax, fuel, coefficient, **kwargs):
        return tax * fuel * coefficient
    
    @staticmethod
    def group_2(tax, max_load, coefficient, **kwargs):
        return tax * max_load * coefficient
    
    @staticmethod
    def group_3(tax, distance_total, distance_abroad, coefficient, **kwargs):
        return tax * (distance_total - distance_abroad) * coefficient / 100
    
    @staticmethod
    def group_4_1(tax, wait_in_airport_hours, coefficient, **kwargs):
        return tax * wait_in_airport_hours
    
    @staticmethod
    def group_4_2(tax, wait_in_airport_days, coefficient, **kwargs):
        return tax * wait_in_airport_days
    
    @staticmethod
    def group_5(tax, wait_in_airport_days, **kwargs):
        return tax * wait_in_airport_days
    
    @staticmethod
    def group_6(tax, passengers_count, **kwargs):
        return tax * passengers_count
    
    @staticmethod
    def group_7(tax, crew_count, **kwargs):
        return tax * crew_count
    
    @staticmethod
    def group_8(tax, **kwargs):
        return tax * 30
    
    @staticmethod
    def group_9(tax, **kwargs):
        return tax
    
    @staticmethod
    def group_10(tax, passengers_count, **kwargs):
        if passengers_count <= 70:
            return tax
        elif passengers_count > 70 and passengers_count <= 140:
            return tax * 2
        elif passengers_count > 140:
            return tax * 3

    @staticmethod
    def business_taxes(tax, flight_time, total_plan_hours, **kwargs):
        return tax * flight_time / total_plan_hours
    