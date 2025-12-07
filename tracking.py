from database_packages import PackageDatabase
from database_routes import RouteDatabase
from models import Package
import utils


def update_package_status(package_db):
    print("\n --Update Package Status-- ")
    package_id = input("Enter package ID: ")

    pkg = package_db.get(package_id)
    if not pkg:
        print(" Package not found")
        return
    
    print(f"Current Status: {pkg.status}")
    print("Choose new status:")
    print("1. Pending")
    print("2. Out for Delivery")
    print("3. Delivered")

    choice = input("Enter choice: ")

    if choice == "1":
        pkg.status = "Pending"
        
    elif choice == "2":
        pkg.status = "Out for Delivery"

    elif choice == "3":
        pkg.status = "Delivered"
        pkg.delivered_at = utils.get_current_time()
        proof = input("Enter proof of delivery: ")
        pkg.proof = proof
    else:
        print("Invalid Choice")
        return

    pkg.updated_at = utils.get_current_time()
    package_db.update(pkg)
    print("Status Updated Successfully")
    


def mark_route_out_for_delivery(route_db, package_db):
    print("\n --Mark Route as Out for Delivery-- ")
    route_id = input("Enter Route ID: ")

    pkgs = route_db.get_packages(route_id)
    if not pkgs:
        print("No packages found for this route!")
        return
    
    for pkg in pkgs:
        pkg.status = "Out for Delivery"
        pkg.updated_at = utils.get_current_time()
        package_db.update(pkg)

        print("All packages are out for delivery")

def mark_package_delivered(package_db):
    print("\n -- Mark Package as Delivered -- ")
    pkg_id = input("Enter Package ID: ")

    package = package_db.get(pkg_id)
    if not package:
        print("Package not found")
        return
    
    package.status = "Delivered"
    package.delivered_at = utils.get_current_time()
    package.updated_at = utils.get_current_time()
    package.proof = input("Enter proof of delivery ")

    package_db.update(package)
    print("Package delivered succesfully")
   


def view_packages_by_status(package_db):
    print("/n -- View Packages by Status --")
    print("Filter by: ")
    print("1. Pending")
    print("2. Out for Delivery")
    print("3. Delivered")

    chois = input("Enter Choice: ")
    stat_map = {"1": "Pending", "2": "Out for Delivery", "3": "Delivered"}

    if chois not in stat_map:
        print("Invalid Choice")
        return
    stats = stat_map[chois]
    packages = package_db.filter_by_status(stats)

    print(f" - {packages.package_id} -> Receiver: {packages.receiver}")

    print("Done")

def track_package(package_db, route_db):
    print("\n --Track Package--")
    package_id = input("Enter Package ID: ")

    package = package_db.get(package_id)
    if not package:
        print("Package not found")
        return
        
    print(f"\n Package ID: {package.package_id}")
    print(f"Sender: {package.sender}")
    print(f"Receiver: {package.receiver}")
    print(f"Status: {package.status}")

    if package.route_id:
        route = route_db.get(package.route_id)
        print(f"Assigned Route: {route.route_name} ({package.route_id})")

        print("\n Tracking Timeline:")
        print(f" -Created At: {package.created_at}")
        print(f" - Last Updated: {package.updated_at}")
        if package.status == "Delivered":
            print(f" - Delivered At: {package.delivered_at}")
            print(f" - Proof {package.proof}")

       
    
        
def view_delivery_timeline(package_db):
    print("\n -- Package Delivery Timeline --")
    package_id = input("Enter Package ID: ")

    package = package_db.get(package.id)
    if not package:
        print("Package not Found")
        return
    
    print(f"\n Timeline for Package {package.package_id}:")
    print(f" - Created At: {package.delivered_at}")
    print(f" - Updated At: {package.updated_at}")
    if package.delivered_at:
        print(f" - Delivered At: {package.delivered_at}")
        print(f" - Proof: {package.proof}")

    print(f"Current Status: {package.status}")
   
def tracking_menu(package_db, route_db):
    while True:
        print("\n ==== Delivery Tracking Menu ==== ")
        print("1. Update Package Status")
        print("2. Mark Route as Out for Delivery")
        print("3. Mark Package as Delivered")
        print("4. View Packaged as Delivered")
        print("5. Track Package")
        print("6. View Delivery Timeline")
        print("7. Exit")

        chois = input("Choose an Option: ")

        if chois == "1":
            update_package_status(package_db)
        elif chois == "2":
            mark_route_out_for_delivery(route_db, package_db)
        elif chois == "3":
            mark_package_delivered(package_db)
        elif chois == "4":
            view_packages_by_status(package_db)
        elif chois == "5":
            track_package(package_db, route_db)
        elif chois == "6":
            view_delivery_timeline(package_db)
        elif chois == "7":
            print("Exiting Menu")
            break
        else:
            print("Invalid Choice. Try again.")
