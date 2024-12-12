class AircraftType:
    
    AIRCRAFT_TYPES = {
        "RRJ-95": {
            "chairs": 100,
            "max_load": 49.45,
            "crew_count": 4
        },
        "A-320": {
            "chairs": 164,
            "max_load": 77,
            "crew_count": 6
        },
        "A-321": {
            "chairs": 220,
            "max_load": 93,
            "crew_count": 7
        },
        "CRJ-200": {
            "chairs": 50,
            "max_load": 23.995,
            "crew_count": 3
        },
        "CH-850": {
            "chairs": 50,
            "max_load": 23.995,
            "crew_count": 3
        }
    }
    
    def __init__(self, aircraft_type):
        self.chairs = self.AIRCRAFT_TYPES[aircraft_type]["chairs"]
        self.max_load = self.AIRCRAFT_TYPES[aircraft_type]["max_load"]
        self.crew_count = self.AIRCRAFT_TYPES[aircraft_type]["crew_count"]