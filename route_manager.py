"""
FreshRoute Logistics - Route Management
Assigned to: JOHN KERBY

TODO: Implement all route management functions.
"""

from database_packages import PackageDatabase
from database_routes import RouteDatabase
from models import Route
import utils


def create_route(route_db):
    """
    Create a new delivery route.
    
    Args:
        route_db (RouteDatabase): Route database instance
    
    TODO:
    1. Generate route ID
    2. Get route details (name, driver, date)
    3. Validate input
    4. Create Route object
    5. Save to database
    """
    utils.print_header("Create New Route")
    
    routes = route_db.get_all_routes()
    route_id = utils.generate_id("RT", [r.route_id for r in routes])
    
    route_name = utils.get_input("Route name")
    driver_name = utils.get_input("Driver name")
    driver_phone = utils.get_input("Driver phone")
    date = utils.get_date_input("Route date")
    
    route = Route(route_id, route_name, driver_name, driver_phone, date)
    
    if route_db.add_route(route):
        utils.print_success(f"Route {route_id} created successfully!")
    else:
        utils.print_error("Failed to create route")
    
    utils.pause()


def view_all_routes(route_db):
    """
    Display all routes in a table format.
    
    Args:
        route_db (RouteDatabase): Route database instance
    
    TODO: Get all routes and display in formatted table
    """
    utils.print_header("All Routes")
    
    routes = route_db.get_all_routes()
    
    if not routes:
        print("No routes found.")
    else:
        widths = [10, 15, 15, 12, 8]
        utils.print_table_row(["ID", "Name", "Driver", "Date", "Packages"], widths)
        print("-" * 65)
        
        for route in routes:
            utils.print_table_row([
                route.route_id,
                utils.truncate_string(route.route_name, 13),
                utils.truncate_string(route.driver_name, 13),
                route.date,
                len(route.package_ids)
            ], widths)
        
        print(f"\nTotal: {len(routes)} routes")
    
    utils.pause()


def view_route_details(route_db, package_db):
    """
    View detailed information about a specific route.
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get route ID from user
    2. Load route details
    3. Load packages in this route
    4. Display route and package information
    """
    utils.print_header("Route Details")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    print(f"\nRoute ID: {route.route_id}")
    print(f"Route Name: {route.route_name}")
    print(f"Driver: {route.driver_name}")
    print(f"Driver Phone: {route.driver_phone}")
    print(f"Date: {route.date}")
    print(f"Status: {route.status}")
    print(f"\nPackages ({len(route.package_ids)}):")
    
    if route.package_ids:
        for pkg_id in route.package_ids:
            pkg = package_db.get_package_by_id(pkg_id)
            if pkg:
                print(f"  - {pkg_id}: {pkg.recipient_name} ({pkg.status})")
    else:
        print("  No packages assigned")
    
    utils.pause()


def assign_packages_to_route(route_db, package_db):
    """
    Assign packages to a route.
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get route ID
    2. Show unassigned packages
    3. Let user select packages
    4. Update package route_id
    5. Update route package_ids list
    """
    utils.print_header("Assign Packages to Route")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    packages = package_db.get_unassigned_packages()
    
    if not packages:
        print("\nNo unassigned packages available.")
        utils.pause()
        return
    
    print(f"\nUnassigned packages:")
    for pkg in packages:
        print(f"  {pkg.package_id}: {pkg.recipient_name} - {pkg.recipient_address}")
    
    package_id = utils.get_input("\nEnter package ID to assign (or 'done')")
    
    while package_id != 'done':
        pkg = package_db.get_package_by_id(package_id)
        if pkg and pkg.route_id is None:
            pkg.route_id = route_id
            route.add_package(package_id)
            package_db.update_package(pkg)
            route_db.update_route(route)
            utils.print_success(f"Package {package_id} assigned to route {route_id}")
        else:
            utils.print_error("Invalid package ID or already assigned")
        
        package_id = utils.get_input("\nEnter another package ID (or 'done')")
    
    utils.pause()


def assign_driver_to_route(route_db):
    """
    Assign or change driver for a route.
    
    Args:
        route_db (RouteDatabase): Route database instance
    
    TODO:
    1. Get route ID
    2. Get new driver details
    3. Update route
    """
    utils.print_header("Assign Driver to Route")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    print(f"\nCurrent driver: {route.driver_name}")
    route.driver_name = utils.get_input("New driver name", route.driver_name)
    route.driver_phone = utils.get_input("New driver phone", route.driver_phone)
    
    if route_db.update_route(route):
        utils.print_success("Driver updated successfully!")
    else:
        utils.print_error("Failed to update driver")
    
    utils.pause()


def edit_route(route_db):
    """
    Edit route details.
    
    Args:
        route_db (RouteDatabase): Route database instance
    
    TODO:
    1. Get route ID
    2. Show current details
    3. Get new details
    4. Update database
    """
    utils.print_header("Edit Route")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    print(f"\nEditing route {route_id}")
    route.route_name = utils.get_input("Route name", route.route_name)
    route.date = utils.get_date_input("Route date") if utils.confirm_action("Change date?") else route.date
    
    if route_db.update_route(route):
        utils.print_success("Route updated successfully!")
    else:
        utils.print_error("Failed to update route")
    
    utils.pause()


def delete_route(route_db, package_db):
    """
    Delete a route from the system.
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get route ID
    2. Show route details
    3. Confirm deletion
    4. Unassign packages from this route
    5. Delete route
    """
    utils.print_header("Delete Route")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    print(f"\nRoute: {route.route_name} - {route.driver_name}")
    print(f"Packages: {len(route.package_ids)}")
    
    if utils.confirm_action("Are you sure you want to delete this route?"):
        for pkg_id in route.package_ids:
            pkg = package_db.get_package_by_id(pkg_id)
            if pkg:
                pkg.route_id = None
                package_db.update_package(pkg)
        
        if route_db.delete_route(route_id):
            utils.print_success("Route deleted successfully!")
        else:
            utils.print_error("Failed to delete route")
    
    utils.pause()


def route_management_menu(route_db, package_db):
    """
    Display route management menu and handle user choices.
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO: Create menu loop with all route operations
    """
    while True:
        utils.clear_screen()
        utils.print_header("Route Management")
        print("1. Create New Route")
        print("2. View All Routes")
        print("3. View Route Details")
        print("4. Assign Packages to Route")
        print("5. Assign Driver to Route")
        print("6. Edit Route")
        print("7. Delete Route")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            create_route(route_db)
        elif choice == '2':
            view_all_routes(route_db)
        elif choice == '3':
            view_route_details(route_db, package_db)
        elif choice == '4':
            assign_packages_to_route(route_db, package_db)
        elif choice == '5':
            assign_driver_to_route(route_db)
        elif choice == '6':
            edit_route(route_db)
        elif choice == '7':
            delete_route(route_db, package_db)
        elif choice == '0':
            break