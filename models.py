"""
FreshRoute Logistics - Data Models
Assigned to: DANIEL

TODO: Implement the Package and Route classes with all required attributes.
"""

from datetime import datetime


class Package:
    """
    Represents a delivery package.
    
    Attributes:
        package_id (str): Unique identifier for the package
        sender (str): Name of the sender
        recipient_name (str): Name of the recipient
        recipient_address (str): Delivery address
        recipient_phone (str): Contact phone number
        weight (float): Package weight in kg
        category (str): Package category (Electronics, Documents, Food, etc.)
        status (str): Current status (Pending, Out for Delivery, Delivered)
        route_id (str): Assigned route ID (optional)
        created_at (str): Creation timestamp
        updated_at (str): Last update timestamp
        delivered_at (str): Delivery timestamp (optional)
        proof_of_delivery (str): Proof note (optional)
    """
    
    def __init__(self, package_id, sender, recipient_name,
                 recipient_address, recipient_phone, weight,
                 category, status="Pending", route_id=None):
        """
        Initialize a new Package.
        
        TODO: Set all package attributes
        """
        # TODO: Implement initialization
        pass
    
    def to_dict(self):
        """
        Convert package to dictionary for JSON storage.
        
        Returns:
            dict: Package data as dictionary
        
        TODO: Convert all attributes to a dictionary
        """
        # TODO: Implement conversion to dictionary
        pass
    
    @staticmethod
    def from_dict(data):
        """
        Create Package object from dictionary.
        
        Args:
            data (dict): Package data
        
        Returns:
            Package: Package object
        
        TODO: Create Package from dictionary data
        """
        # TODO: Implement creation from dictionary
        pass
    
    def update_status(self, new_status):
        """
        Update package status.
        
        Args:
            new_status: New status value
        
        TODO: Update status and timestamp
        """
        # TODO: Implement status update
        pass


class Route:
    """
    Represents a delivery route.
    
    Attributes:
        route_id (str): Unique identifier for the route
        route_name (str): Name of the route
        driver_name (str): Assigned driver name
        driver_phone (str): Driver's phone number
        date (str): Route date
        package_ids (list): List of package IDs in this route
        status (str): Route status (Active, Completed)
        created_at (str): Creation timestamp
        estimated_fuel (float): Estimated fuel usage in liters
    """
    
    def __init__(self, route_id, route_name, driver_name,
                 driver_phone, date):
        """
        Initialize a new Route.
        
        TODO: Set all route attributes
        """
        # TODO: Implement initialization
        pass
    
    def to_dict(self):
        """
        Convert route to dictionary for JSON storage.
        
        Returns:
            dict: Route data as dictionary
        
        TODO: Convert all attributes to a dictionary
        """
        # TODO: Implement conversion to dictionary
        pass
    
    @staticmethod
    def from_dict(data):
        """
        Create Route object from dictionary.
        
        Args:
            data (dict): Route data
        
        Returns:
            Route: Route object
        
        TODO: Create Route from dictionary data
        """
        # TODO: Implement creation from dictionary
        pass
    
    def add_package(self, package_id):
        """
        Add a package to this route.
        
        Args:
            package_id: Package ID to add
        
        TODO: Add package ID to the route's package list
        """
        # TODO: Implement adding package
        pass
    
    def remove_package(self, package_id):
        """
        Remove a package from this route.
        
        Args:
            package_id: Package ID to remove
        
        TODO: Remove package ID from the route's package list
        """
        # TODO: Implement removing package
        pass
