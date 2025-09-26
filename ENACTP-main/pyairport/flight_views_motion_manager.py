##@namespace flight_views_motion_manager
"""
    This module creates the FlightView collection and manages their movements
    (FlightViewsMotionManager class).
    Maintains a scene graph in order to be able to update flight views
    instead of having to clear and recreate all of them at each update.
"""
##\privatesection

from flight_view import FlightView


class FlightViewsMotionManager:
    """ Collection of flight views and their motion management """

    def __init__(self, radar):
        # Reference to the radar view
        self.radar_view = radar
        # List of the current flights
        self.current_flights = []
        # Dictionary of the corresponding flight views in the scene
        self.flight_views_dict = {}

        # Create and update the initial flight views
        self.update_flight_views()

        # Connect to the time manager's time_changed signal
        # in order to update flight views when the time changes
        self.radar_view.time_manager.time_changed.connect(self.update_flight_views)

    def update_flight_views(self):
        """ Create/update aircraft items in the QGraphicsScene """
        new_flights = self.radar_view.simulation.current_flights
        # Add new flight views for flights who have just joined
        for flight in set(new_flights) - set(self.current_flights):
            flight_view = FlightView(flight, self.radar_view)  # create a flight view
            self.radar_view.add_flight_view(flight_view)       # add it into radar view's scene
            self.flight_views_dict[flight] = flight_view       # add it to item dict
        # Remove flight views for flights who have just left
        for flight in set(self.current_flights) - set(new_flights):
            flight_view = self.flight_views_dict.pop(flight)   # remove flight view from the dictionary
            self.radar_view.remove_flight_view(flight_view)    # and remove it from the radar view's scene
        # Refresh current flights list
        self.current_flights = new_flights
        # Get conflicting flights
        conf = self.radar_view.simulation.conflicts
        # Update positions of the current flight views
        for flight_view in self.flight_views_dict.values():
            flight_view.update_position(flight_view.flight in conf)

##\endprivatesection
