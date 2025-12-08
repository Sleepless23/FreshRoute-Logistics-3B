"""
FreshRoute Logistics - Route Database Operations
Author: Nathaniel

JSON-based storage for all route-related data.
Handles creating, reading, updating, and deleting routes.
"""

import json
import os
from models import Route


class RouteDatabase:
    """Manages all route data using a simple JSON file."""

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.routes_file = os.path.join(self.data_dir, "routes.json")
        self._setup_storage()

    def _setup_storage(self):
        """Make sure the data folder and JSON file exist."""
        os.makedirs(self.data_dir, exist_ok=True)

        if not os.path.exists(self.routes_file):
            with open(self.routes_file, "w") as file:
                json.dump([], file, indent=4)

    def _read_routes(self):
        """Load routes from the JSON file."""
        try:
            with open(self.routes_file, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_routes(self, routes):
        """Write updated route data back to the file."""
        try:
            with open(self.routes_file, "w") as file:
                json.dump(routes, file, indent=4)
        except Exception as err:
            print("Error saving route data:", err)


    # CRUD FUNCTIONS

    def get_all_routes(self):
        """Return all saved routes as Route objects."""
        data = self._read_routes()
        return [Route(**r) for r in data]

    def get_route_by_id(self, route_id):
        """Find a route by ID. Returns None if not found."""
        data = self._read_routes()
        for r in data:
            if str(r.get("route_id")) == str(route_id):
                return Route(**r)
        return None

    def add_route(self, route):
        """Add a new route.
        Returns True if successful, False if the ID already exists.
        """
        data = self._read_routes()

        # avoid duplicates
        if any(str(r.get("route_id")) == str(route.route_id) for r in data):
            return False

        data.append(route.to_dict())
        self._write_routes(data)
        return True

    def update_route(self, route):
        """Update an existing route using its route_id."""
        data = self._read_routes()

        for index, r in enumerate(data):
            if str(r.get("route_id")) == str(route.route_id):
                data[index] = route.to_dict()
                self._write_routes(data)
                return True

        return False

    def delete_route(self, route_id):
        """Delete a route by ID."""
        data = self._read_routes()
        new_data = [r for r in data if str(r.get("route_id")) != str(route_id)]

        if len(new_data) == len(data):
            return False  # nothing removed

        self._write_routes(new_data)
        return True


    # FILTERS / SEARCH HELPERS

    def get_routes_by_date(self, date):
        """Get all routes scheduled on a specific date."""
        data = self._read_routes()
        return [Route(**r) for r in data if r.get("date") == date]

    def get_routes_by_driver(self, driver_name):
        """Get all routes assigned to a given driver."""
        data = self._read_routes()
        return [
            Route(**r)
            for r in data
            if r.get("driver", "").lower() == driver_name.lower()
        ]
