import sys

class TextInterface:
    """Text-based interface that contains methods for getting input from the user and displaying search
    results.
    """
    
    def __init__(self, trains_list):
        """Initializes the TextInterface object with a list of all train objects in the simulation.
        """
        self.trains = trains_list
    
    def getUserInput(self):
        """This method prompts the user to specify a direction of travel and a station at which
        they want to find trains. If a user types a direction other than n or s, the program will
        ask them to provide a valid input before continuing.
        """
        print "\nWelcome! This program lets you search for New York City subway trains running on the 1, 2, 3, 4, 5, 6, or S lines."
        print "Note that for S trains, northbound is eastbound in real life and southbound is westbound in real life."
        print "\nFirst, choose a direction - northbound or southbound. Type n for northbound or s for southbound."
        # valid_input will remain False until either n or s is typed
        valid_input = False
        while valid_input == False:
            direction = raw_input()
            if direction == "n":
                valid_input = True
                direction = 'northbound'
            elif direction == 's':
                valid_input = True
                direction = 'southbound'
            # If you really don't like our program, you can quit by typing q
            elif direction == 'q':
                sys.exit()
            else:
                print "We didn't understand that. Please try again."
        print "\nNow, search for the station you want trains from."
        station = raw_input()
        return direction, station
    
    def showApproachingTrains(self, station, list_of_trains):
        """Takes 2 arguments, the station at which the user is looking for trains and a list of
        trains currently approaching that station, where each item in the list is formatted
        [train_index, stop_number, arrival_time]. If the list is empty, it informs the user that
        no trains are near the station. Otherwise, it looks up information about each train in
        the list and displays it to the user.
        """
        print "..."
        if len(list_of_trains) == 0:
            print "Sorry, there aren't any trains currently approaching", station
        else:
            print "Here is a list of trains arriving at or departing from", station, "in the next 30 minutes:\n"
            for train_list in list_of_trains:
                train_number = train_list[0] # Used to look up train object in the master list of trains
                stop_number = train_list[1]
                if int(self.trains[train_number].getArrivalTime(stop_number)) <= 30:
                    self.trains[train_number].showInfo(stop_number)
        print ""
    
    def showStationSearchResults(self, results_list):
        """Takes 1 argument, a list of possible station results. If there is only one possible
        result, this function will never be called, so it only has to handle list of length 0 or >1.
        If the length of the list is 0, the program will ask the user whether they want to do
        another search or quit. Otherwise, all possible results will be displayed next to a unique
        integer, and the user will be asked to type in an integer to choose the station they want.
        """
        print "..."
        if len(results_list) == 0:
            print "Sorry, we couldn't find a station with that name.\n"
            self.againOrQuit()
        else:
            print "We found several stations with that name. Please choose one from the list below."
            for i in range(len(results_list)):
                print (i+1), ': ', results_list[i]
            choice = int(raw_input("Type the number of the station you want: "))
            return results_list[choice-1]
    
    def againOrQuit(self):
        """Asks the user whether they want to perform a new search or quit the program.
        """
        print "Type n to do a new search or q to exit the program."
        choice = raw_input()
        if choice == "n":
            return True
        if choice == "q":
            return False
        else:
            print "We didn't understand that. Please try again."
            return self.againOrQuit()
