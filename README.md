# nyc-subway-finder
Text-based interface for finding real-time data about New York City subway train
arrivals on the 1, 2, 3, 4, 5, 6, and S lines

# Requirements:
cImage module

google.transit module - can be installed using pip:

> pip install --upgrade gtfs-realtime-bindings

# Description:
Subway Finder is a program that takes real-time information from the Metro
Transit Authority (MTA) of New York City and converts it into a user-friendly
format. The MTA uses the GTFS-realtime protocol to transmit data on train times
and stops. To launch the program, run the nyc-subway-finder.py file.

# Features:
- Allows you to search in real time for New York City subway trains on the
1, 2, 3, 4, 5, 6, and S lines
- Simple prompts to help the user find which train they are looking for
- When the user input matches more than one station, the user can pick from a
list of possible stations
- Displays a map of the subway system in Manhattan for quick reference
- Provides the option to search again or quit after each search

# Detailed program breakdown:
Our program is based on the Model-View-Controller system. Our model, contained
mostly in train.py, is the back end of our program, and contains a class called
Train that has all the properties we want the "trains" to have: direction,
stops, and arrival time. Each of those abilites is contained inside a method of
the class.

Our controller is the function that calls our other programs and holds the
information until it is displayed to the user. The controller is the program
that accesses the real-time feed, passes it onto the model, and coordinates the
exchange of information between the model and the view program. The controller
contains the functions that allow user input to be non-specific, using regular
expression methods to match user inputs to official station names.

Finally, our view is the interfaces.py program that puts all of the information
out there for the user to see. It consists of a TextInterface class, which
contains code that aks for and receives user input and passes it back to the
controller. This class also has methods for displaying a map of the subway
system and asking the user whether they want to do another search or exit the
program.
