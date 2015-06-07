from google.transit import gtfs_realtime_pb2
import urllib
import re
from train import *
from interfaces import *

def main():
    keepGoing = True
    stops = createStopsDict()
    trains = getData(stops)
    interface = TextInterface(trains)
    while keepGoing == True:
        direction, station_query = interface.getUserInput()
        station = matchInput2Station(station_query, stops, interface)
        approaching_trains = findTrains(direction, station, trains)
        interface.showApproachingTrains(station, approaching_trains)
        keepGoing = interface.againOrQuit()
    interface.closeMap()

def findTrains(direction, station, trains):
    """Given a desired direction of travel, station, and the master train list, this
    function finds all of the trains going in the given direction that will stop at that
    station. It returns a list of lists. Each sub-list represents one train approaching
    the given station, and contains that train's index, the stop number of the desired
    station for the train, and the arrival time of the train at the station. The list of
    lists is sorted in ascending order by the arrival time of each train.
    """
    results = []
    # Iterate through each train object in the trains list
    for train in trains:
        stopNames = train.getAllStops()
        whichWay = train.getDirection()
        if whichWay == direction:
            # Iterate through each upcoming stop for the train
            for stopName in stopNames:
                # Check to see if the station name is the same as the desired station
                if stopName[1] == station:
                    train_index = train.getIndex()
                    stop_number = stopName[0]
                    arrival_time = int(train.getArrivalTime(stop_number))
                    results.append([train_index, stop_number, arrival_time])
    # Once nested list is complete, sort by the third element, arrival time, in each sub-list
    results.sort(lambda x,y: cmp(x[2], y[2]))
    return results

def matchInput2Station(input, stops, interface):
    """Given a text input, stops dictionary, and interface name, this function uses
    regular expression search to match the input to a station name and returns the
    station name as a string.
    """
    searchTerm = re.compile(input, re.IGNORECASE) # Create an RE object from the input
    values = stops.values() # Get all the station names from the stops dictionary
    results_set = set()
    # Iterate through all station names
    for item in values:
        # If the station name matches the input, add it to a set of possible stations
        stationFinal = re.search(searchTerm, item)
        if stationFinal:
            results_set.add(item)
    results = list(results_set)
    # If there is only one possible station, we can go ahead and return it
    if len(results) == 1:
        return results[0]
    # Otherwise, we ask showStationSearchResults() to prompt the user to choose
    # from multiple possible stations or display an error message if len(results) = 0 
    else:
        return interface.showStationSearchResults(results)
    
def getData(stops):
    """Retrieves data from the MTA's realtime feed, then creates a train object for each
    train described in the feed and stores each train object in a master list.
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=af9eed62023f1c5b57ef97020c0db1c6&feed_id=1')
    feed.ParseFromString(response.read())
    
    trains = []
    # Iterate through all trains in the feed
    for entity in feed.entity:
        # Ignore trains that don't have useful data
        if entity.HasField('trip_update'):
            thomas = Train(entity.trip_update, stops, len(trains))
            trains.append(thomas)
    return trains

def createStopsDict():
    """Creates a dictionary of subway stops with stop IDs as keys and station names
    as values.
    """
    # Get stop information from stops.txt file provided by MTA
    stops_file = open('stops.txt', 'r')
    stops_str = stops_file.read()
    stops_list = stops_str.split('\n')
    stops_file.close()
    
    # Grab stop ID and station name from text file and organize them into a dictionary
    stops = {}
    for line in stops_list:
        line = line.split(',')
        id = line[0]
        name = line[2]
        stops[id] = name
    return stops

if __name__ == "__main__":
    main()
