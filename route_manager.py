

from datetime import datetime

class RouteManager:
    def __init__(self):
        # Stores all routes
        # Format: {route_id: {"driver": str, "packages": [], "created_at": datetime}}
        self.routes = {}

    # 1. Create a new delivery route

    def create_route(self, route_id, driver_name):
        if route_id in self.routes:
            return f"Route {route_id} already exists."

        self.routes[route_id] = {
            "driver": driver_name,
            "packages": [],
            "created_at": datetime.now()
        }
        return f"Route {route_id} created successfully."

    # 2. Assign a package to a route

    def add_package_to_route(self, route_id, package_id):
        if route_id not in self.routes:
            return f"Route {route_id} does not exist."

        self.routes[route_id]["packages"].append(package_id)
        return f"Package {package_id} assigned to route {route_id}."

    # 3. Remove a package from a route

    def remove_package_from_route(self, route_id, package_id):
        if route_id not in self.routes:
            return f"Route {route_id} does not exist."

        if package_id not in self.routes[route_id]["packages"]:
            return f"Package {package_id} is not in this route."

        self.routes[route_id]["packages"].remove(package_id)
        return f"Package {package_id} removed from route {route_id}."

    # 4. Assign/Change driver for a route

    def assign_driver(self, route_id, driver_name):
        if route_id not in self.routes:
            return f"Route {route_id} does not exist."

        self.routes[route_id]["driver"] = driver_name
        return f"Driver updated for route {route_id}."

    # 5. View route details (driver + packages)
   
    def view_route(self, route_id):
        if route_id not in self.routes:
            return f"Route {route_id} does not exist."

        return self.routes[route_id]
  
    # 6. View all routes (summary)

    def list_routes(self):
        return self.routes

    # 7. Delete a route

    def delete_route(self, route_id):
        if route_id not in self.routes:
            return f"Route {route_id} does not exist."

        del self.routes[route_id]
        return f"Route {route_id} deleted successfully."
