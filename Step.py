class Step():

    def __init__(self,distance,duration,latitude,longitude):
        self.distance = distance
        self.duration = duration
        self.latitude = latitude
        self.longitude = longitude
        self.time = None
        self.zipcode = None
        self.city = None
        self.weather = None