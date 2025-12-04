"""
FreshRoute Logistics - Delivery Tracking
Assigned to: FRANCHESCA

TODO: Implement all delivery tracking functions.
"""

from database_packages import PackageDatabase
from database_routes import RouteDatabase
from models import Package
import utils


def update_package_status(package_db):
    """
    Update the status of a package.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get package ID
    2. Show current status
    3. Let user select new status (Pending, Out for Delivery, Delivered)
    4. Update package
    5. If delivered, set delivered_at timestamp
    """
    # TODO: Implement status update
    pass


def mark_route_out_for_delivery(route_db, package_db):
    """
    Mark all packages in a route as "Out for Delivery".
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get route ID
    2. Get all packages in route
    3. Update all to "Out for Delivery"
    """
    # TODO: Implement batch status update
    pass


def mark_package_delivered(package_db):
    """
    Mark a package as delivered with proof.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get package ID
    2. Set status to "Delivered"
    3. Set delivered_at timestamp
    4. Get proof of delivery (text note)
    5. Update package
    """
    # TODO: Implement mark as delivered
    pass


def view_packages_by_status(package_db):
    """
    View packages filtered by status.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Show status options
    2. Get user choice
    3. Filter and display packages
    """
    # TODO: Implement view by status
    pass


def track_package(package_db, route_db):
    """
    Display full tracking information for a package.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    
    TODO:
    1. Get package ID
    2. Load package details
    3. Load route details if assigned
    4. Display tracking timeline
    """
    # TODO: Implement package tracking
    pass


def view_delivery_timeline(package_db):
    """
    View timeline of package status changes.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get package ID
    2. Display created_at, updated_at, delivered_at
    3. Show current status
    """
    # TODO: Implement delivery timeline
    pass


def tracking_menu(package_db, route_db):
    """
    Display delivery tracking menu and handle user choices.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    
    TODO: Create menu loop with all tracking operations
    """
    # TODO: Implement tracking menu
    pass
