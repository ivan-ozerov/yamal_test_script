class Flight:
    def __init__(self, flight_params):
        self.race_date = flight_params["Дата выполнения рейса"]
        self.race_type = flight_params["Тип рейса"]
        self.plane_type = flight_params["Тип ВС"]
        self.airport_dep = flight_params["Аэропорт вылета"]
        self.airport_arr = flight_params["Аэропорт прилета"]
        self.fuel = flight_params["Расход топлива, тонн"]
        self.flight_time = flight_params["Налет, часов"]
        self.passengers_count = flight_params["Загрузка пассажиров, чел."]
        self.distance_total = flight_params["Итого расстояние, км"]
        self.distance_abroad = flight_params["Расстояние за границей, км"]
        self.wait_in_airport_days = flight_params["Ожидание в аэропорте прилета, дней"]
        self.wait_in_airport_hours = flight_params["Ожидание в аэропорте прилета, часов"]
        self.catering = flight_params["Борт. Питание"]
        self.business_class = flight_params["Бизнес зал"]
        