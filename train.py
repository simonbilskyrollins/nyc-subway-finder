import time
import calendar

class Train:
    """Creates a train object that represents one subway train we have data for. The methods
    contained in this class interpret information we get from the MTA's feed, such as route number,
    direction, arrival time, and upcoming stops.
    """

    def __init__(self, trip_update, stops, position_in_list):
        """Initializes one train object with a 'trip_update' object from the MTA data, a
        dictionary of all the stop IDs and names in the subway system, and the index of the
        train in the master list of train objects.
        """
        self.trip_update = trip_update
        self.stops = stops
        self.routeID = str(self.trip_update.trip.route_id)
        # A minor quirk in the MTA's data is fixed here. S trains were listed as GS for some reason
        if self.routeID == "GS":
            self.routeID = "S"
        self.index = position_in_list
        
    def showInfo(self, stop_number):
        """Given the stop number (the nth stop on the train's remaining route) as an
        argument, this method prints out a message containing the train's direction,
        route number, station, and arrival time.
        """
        if self.arrivalTime == '': # At origin terminals, there will only be a departure time listed
            if self.getArrivalTime(stop_number) == '00':
                print "There is a", self.getDirection(), self.routeID, "train departing from", self.getStop(stop_number), "now."
            elif self.getArrivalTime(stop_number) == '01':
                print "There is a", self.getDirection(), self.routeID, "train departing from", self.getStop(stop_number), "in 1 minute."
            else:
                print "There is a", self.getDirection(), self.routeID, "train departing from", self.getStop(stop_number), "in", int(self.getArrivalTime(stop_number)), "minutes."
        elif self.getArrivalTime(stop_number) == '01':
            print "There is a", self.getDirection(), self.routeID, "train arriving at", self.getStop(stop_number), "in 1 minute."
        elif self.getArrivalTime(stop_number) == '00':
            print "There is a", self.getDirection(), self.routeID, "train arriving at", self.getStop(stop_number), "now."
        else:
            print "There is a", self.getDirection(), self.routeID, "train arriving at", self.getStop(stop_number), "in", int(self.getArrivalTime(stop_number)), "minutes."

    def getArrivalTime(self, stop_number):
        """This method, given a stop number, returns the number of minutes it will take
        for the train to arrive at the specified station.
        """
        # Get absolute POSIX time from MTA data
        self.arrivalTime = str(self.trip_update.stop_time_update[stop_number].arrival)
        departureTime = str(self.trip_update.stop_time_update[stop_number].departure)
        if self.arrivalTime != '': # Some stops only have a departure time listed
            unix_time = float(self.arrivalTime.strip('time: '))
        else:
            unix_time = int(departureTime.strip('time: '))
        
        # Calculate difference, in POSIX time, between arrival time and current time
        # There is a 60-second offset here to account for delays in data transmission
        # that would otherwise produce negative differences (i.e. train arriving in
        # -1 minutes)
        difference = unix_time + 60 - calendar.timegm(time.gmtime())
        
        # Convert POSIX difference to struct_time difference, then return minutes
        utc_difference = time.gmtime(difference)
        readable_difference = time.strftime("%M", utc_difference)
        return readable_difference
    
    def getAllStops(self):
        """Gets all upcoming stops for the train.
        Returns a list of form [stop number, station name].
        """
        all_stops = []
        # Iterate through all the stop_time_update objects in trip_update
        for i in range(len(self.trip_update.stop_time_update)):
            stop = self.getStop(i)
            if stop not in all_stops:
                all_stops.append([i, stop])
        return all_stops    
    
    def getStop(self, i):
        """Gets the nth stop for the train given the stop number as an argument.
        """
        stopID = self.trip_update.stop_time_update[i].stop_id
        stop = self.stops[stopID]
        return stop
            
    def getDirection(self):
        """Gets the direction of the train. Returns 'N' or 'S'.
        """
        if 'N' in str(self.trip_update.trip.trip_id):
            direction = 'northbound'
        if 'S' in str(self.trip_update.trip.trip_id):
            direction = 'southbound'
        return direction
    
    def getIndex(self):
        """Gets the position of the train in the master train list.
        """
        return self.index
