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
        self.package_id = package_id
        self.sender = sender
        self.recipient_name = recipient_name
        self.recipient_address = recipient_address
        self.recipient_phone = recipient_phone
        self.weight = weight
        self.category = category
        self.status = status
        self.route_id = route_id
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.delivered_at = None
        self.proof_of_delivery = None
    
    def to_dict(self):
        """
        Convert package to dictionary for JSON storage.
        
        Returns:
            dict: Package data as dictionary
        
        TODO: Convert all attributes to a dictionary
        """
        return {
            'package_id': self.package_id,
            'sender': self.sender,
            'recipient_name': self.recipient_name,
            'recipient_address': self.recipient_address,
            'recipient_phone': self.recipient_phone,
            'weight': self.weight,
            'category': self.category,
            'status': self.status,
            'route_id': self.route_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'delivered_at': self.delivered_at,
            'proof_of_delivery': self.proof_of_delivery
        }
    
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
        pkg = Package(
            data['package_id'],
            data['sender'],
            data['recipient_name'],
            data['recipient_address'],
            data['recipient_phone'],
            data['weight'],
            data['category'],
            data.get('status', 'Pending'),
            data.get('route_id')
        )
        pkg.created_at = data.get('created_at', pkg.created_at)
        pkg.updated_at = data.get('updated_at', pkg.updated_at)
        pkg.delivered_at = data.get('delivered_at')
        pkg.proof_of_delivery = data.get('proof_of_delivery')
        return pkg
    
    def update_status(self, new_status):
        """
        Update package status.
        
        Args:
            new_status: New status value
        
        TODO: Update status and timestamp
        """
        self.status = new_status
        self.updated_at = datetime.now().isoformat()
        if new_status == "Delivered":
            self.delivered_at = datetime.now().isoformat()


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
        self.route_id = route_id
        self.route_name = route_name
        self.driver_name = driver_name
        self.driver_phone = driver_phone
        self.date = date
        self.package_ids = []
        self.status = "Active"
        self.created_at = datetime.now().isoformat()
        self.estimated_fuel = 0.0
    
    def to_dict(self):
        """
        Convert route to dictionary for JSON storage.
        
        Returns:
            dict: Route data as dictionary
        
        TODO: Convert all attributes to a dictionary
        """
        return {
            'route_id': self.route_id,
            'route_name': self.route_name,
            'driver_name': self.driver_name,
            'driver_phone': self.driver_phone,
            'date': self.date,
            'package_ids': self.package_ids,
            'status': self.status,
            'created_at': self.created_at,
            'estimated_fuel': self.estimated_fuel
        }
    
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
        route = Route(
            data['route_id'],
            data['route_name'],
            data['driver_name'],
            data['driver_phone'],
            data['date']
        )
        route.package_ids = data.get('package_ids', [])
        route.status = data.get('status', 'Active')
        route.created_at = data.get('created_at', route.created_at)
        route.estimated_fuel = data.get('estimated_fuel', 0.0)
        return route
    
    def add_package(self, package_id):
        """
        Add a package to this route.
        
        Args:
            package_id: Package ID to add
        
        TODO: Add package ID to the route's package list
        """
        if package_id not in self.package_ids:
            self.package_ids.append(package_id)
    
    def remove_package(self, package_id):
        """
        Remove a package from this route.
        
        Args:
            package_id: Package ID to remove
        
        TODO: Remove package ID from the route's package list
        """
        if package_id in self.package_ids:
            self.package_ids.remove(package_id)