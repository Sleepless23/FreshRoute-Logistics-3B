from database_packages import PackageDatabase
from database_routes import RouteDatabase
from models import Package
import utils


def update_package_status(package_db):
    """
    Update the status of a package.
    
    Args:
        package_db (PackageDatabase): Package database instance
    """
    utils.print_header("Update Package Status")
    
    package_id = utils.get_input("Enter package ID")
    package = package_db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    print(f"\nCurrent status: {package.status}")
    print("Available statuses: Pending, Out for Delivery, Delivered")
    
    new_status = utils.get_choice("Select status", ["Pending", "Out for Delivery", "Delivered"])
    package.update_status(new_status)
    
    if package_db.update_package(package):
        utils.print_success(f"Status updated to {new_status}")
    else:
        utils.print_error("Failed to update status")
    
    utils.pause()


def mark_route_out_for_delivery(route_db, package_db):
    """
    Mark all packages in a route as "Out for Delivery".
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    """
    utils.print_header("Mark Route Out for Delivery")
    
    route_id = utils.get_input("Enter route ID")
    route = route_db.get_route_by_id(route_id)
    
    if not route:
        utils.print_error("Route not found")
        utils.pause()
        return
    
    count = 0
    for pkg_id in route.package_ids:
        pkg = package_db.get_package_by_id(pkg_id)
        if pkg:
            pkg.update_status("Out for Delivery")
            package_db.update_package(pkg)
            count += 1
    
    utils.print_success(f"{count} packages marked as Out for Delivery")
    utils.pause()


def mark_package_delivered(package_db):
    """
    Mark a package as delivered with proof.
    
    Args:
        package_db (PackageDatabase): Package database instance
    """
    utils.print_header("Mark Package Delivered")
    
    package_id = utils.get_input("Enter package ID")
    package = package_db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    package.update_status("Delivered")
    package.proof_of_delivery = utils.get_input("Proof of delivery (optional)", "Delivered successfully")
    
    if package_db.update_package(package):
        utils.print_success("Package marked as delivered!")
    else:
        utils.print_error("Failed to update package")
    
    utils.pause()


def view_packages_by_status(package_db):
    """
    View packages filtered by status.
    
    Args:
        package_db (PackageDatabase): Package database instance
    """
    utils.print_header("View Packages by Status")
    
    print("Available statuses:")
    print("1. Pending")
    print("2. Out for Delivery")
    print("3. Delivered")
    
    choice = input("\nSelect status: ")
    status_map = {"1": "Pending", "2": "Out for Delivery", "3": "Delivered"}
    status = status_map.get(choice)
    
    if not status:
        utils.print_error("Invalid choice")
        utils.pause()
        return
    
    packages = package_db.get_packages_by_status(status)
    
    print(f"\n{status} Packages:")
    if not packages:
        print("No packages found.")
    else:
        widths = [12, 20, 20, 15]
        utils.print_table_row(["ID", "Recipient", "Address", "Status"], widths)
        print("-" * 70)
        
        for pkg in packages:
            utils.print_table_row([
                pkg.package_id,
                utils.truncate_string(pkg.recipient_name, 18),
                utils.truncate_string(pkg.recipient_address, 18),
                pkg.status
            ], widths)
        
        print(f"\nTotal: {len(packages)} packages")
    
    utils.pause()


def track_package(package_db, route_db):
    """
    Display full tracking information for a package.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    """
    utils.print_header("Track Package")
    
    package_id = utils.get_input("Enter package ID")
    package = package_db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    print(f"\nPackage ID: {package.package_id}")
    print(f"Recipient: {package.recipient_name}")
    print(f"Address: {package.recipient_address}")
    print(f"Status: {package.status}")
    print(f"\nTimeline:")
    print(f"  Created: {utils.format_date(package.created_at)}")
    print(f"  Updated: {utils.format_date(package.updated_at)}")
    if package.delivered_at:
        print(f"  Delivered: {utils.format_date(package.delivered_at)}")
    
    if package.route_id:
        route = route_db.get_route_by_id(package.route_id)
        if route:
            print(f"\nRoute: {route.route_name}")
            print(f"Driver: {route.driver_name}")
            print(f"Phone: {route.driver_phone}")
    
    if package.proof_of_delivery:
        print(f"\nProof of Delivery: {package.proof_of_delivery}")
    
    utils.pause()


def view_delivery_timeline(package_db):
    """
    View timeline of package status changes.
    
    Args:
        package_db (PackageDatabase): Package database instance
    """
    utils.print_header("Delivery Timeline")
    
    package_id = utils.get_input("Enter package ID")
    package = package_db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    print(f"\nPackage {package_id} Timeline:")
    print(f"  Created:   {utils.format_date(package.created_at)}")
    print(f"  Updated:   {utils.format_date(package.updated_at)}")
    if package.delivered_at:
        print(f"  Delivered: {utils.format_date(package.delivered_at)}")
    print(f"\nCurrent Status: {package.status}")
    
    utils.pause()


def tracking_menu(package_db, route_db):
    """
    Display delivery tracking menu and handle user choices.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    """
    while True:
        utils.clear_screen()
        utils.print_header("Delivery Tracking")
        print("1. Update Package Status")
        print("2. Mark Route Out for Delivery")
        print("3. Mark Package Delivered")
        print("4. View Packages by Status")
        print("5. Track Package")
        print("6. View Delivery Timeline")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            update_package_status(package_db)
        elif choice == '2':
            mark_route_out_for_delivery(route_db, package_db)
        elif choice == '3':
            mark_package_delivered(package_db)
        elif choice == '4':
            view_packages_by_status(package_db)
        elif choice == '5':
            track_package(package_db, route_db)
        elif choice == '6':
            view_delivery_timeline(package_db)
        elif choice == '0':
            break