"""
FreshRoute Logistics - Route Database Operations
Assigned to: NATHANIEL

TODO: Implement all route database operations (CRUD).
"""

import json
import os
from models import Route


class RouteDatabase:
    """Handles route data storage and retrieval using JSON file."""
    
    def __init__(self, data_dir="data"):
        """
        Initialize route database.
        
        Args:
            data_dir (str): Directory for data files
        
        TODO: Set up database file path and initialize
        """
        self.data_dir = data_dir
        self.routes_file = os.path.join(data_dir, "routes.json")
        self._initialize()
    
    def _initialize(self):
        """
        Create data directory and file if they don't exist.
        
        TODO: Create directory and empty routes.json file
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.routes_file):
            with open(self.routes_file, 'w') as f:
                json.dump([], f)
    
    def _read_routes(self):
        """
        Read routes from JSON file.
        
        Returns:
            list: List of route dictionaries
        
        TODO: Read and parse JSON file
        """
        with open(self.routes_file, 'r') as f:
            return json.load(f)
    
    def _write_routes(self, routes_data):
        """
        Write routes to JSON file.
        
        Args:
            routes_data (list): List of route dictionaries
        
        TODO: Write data to JSON file with proper formatting
        """
        with open(self.routes_file, 'w') as f:
            json.dump(routes_data, f, indent=2)
    
    def get_all_routes(self):
        """
        Get all routes from database.
        
        Returns:
            List[Route]: List of Route objects
        
        TODO: Read JSON and convert to Route objects
        """
        data = self._read_routes()
        return [Route.from_dict(route) for route in data]
    
    def get_route_by_id(self, route_id):
        """
        Get a specific route by ID.
        
        Args:
            route_id: Route ID to search for
        
        Returns:
            Route object if found, None otherwise
        
        TODO: Search for route by ID
        """
        routes = self.get_all_routes()
        for route in routes:
            if route.route_id == route_id:
                return route
        return None
    
    def add_route(self, route):
        """
        Add a new route to database.
        
        Args:
            route: Route object to add
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Add route to JSON file (check for duplicates)
        """
        data = self._read_routes()
        for r in data:
            if r['route_id'] == route.route_id:
                return False
        data.append(route.to_dict())
        self._write_routes(data)
        return True
    
    def update_route(self, route):
        """
        Update an existing route.
        
        Args:
            route: Route object with updated data
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Update route in JSON file
        """
        data = self._read_routes()
        for i, r in enumerate(data):
            if r['route_id'] == route.route_id:
                data[i] = route.to_dict()
                self._write_routes(data)
                return True
        return False
    
    def delete_route(self, route_id):
        """
        Delete a route by ID.
        
        Args:
            route_id: Route ID to delete
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Remove route from JSON file
        """
        data = self._read_routes()
        for i, r in enumerate(data):
            if r['route_id'] == route_id:
                data.pop(i)
                self._write_routes(data)
                return True
        return False
    
    def get_routes_by_date(self, date):
        """
        Get all routes for a specific date.
        
        Args:
            date: Date to filter by (YYYY-MM-DD)
        
        Returns:
            List of matching routes
        
        TODO: Filter routes by date
        """
        routes = self.get_all_routes()
        return [route for route in routes if route.date == date]
    
    def get_routes_by_driver(self, driver_name):
        """
        Get all routes assigned to a specific driver.
        
        Args:
            driver_name: Driver name to filter by
        
        Returns:
            List of matching routes
        
        TODO: Filter routes by driver
        """
        routes = self.get_all_routes()
        return [route for route in routes if route.driver_name == driver_name]