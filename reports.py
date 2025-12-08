import csv
from datetime import datetime
from database_packages import PackageDatabase
from database_routes import RouteDatabase
import utils


def report_packages_delivered_per_day(package_db):
    """
    Generate report of packages delivered on a specific day.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get date from user
    2. Filter delivered packages for that date
    3. Display summary and list
    4. Option to export to CSV
    """
    utils.print_header("Packages Delivered Per Day")
    
    date = utils.get_date_input("Enter date")
    packages = package_db.get_packages_by_status("Delivered")
    
    delivered_on_date = [p for p in packages if p.delivered_at and p.delivered_at.startswith(date)]
    
    print(f"\nPackages delivered on {date}:")
    if not delivered_on_date:
        print("No packages delivered on this date.")
    else:
        widths = [12, 20, 20]
        utils.print_table_row(["ID", "Recipient", "Address"], widths)
        print("-" * 55)
        
        for pkg in delivered_on_date:
            utils.print_table_row([
                pkg.package_id,
                utils.truncate_string(pkg.recipient_name, 18),
                utils.truncate_string(pkg.recipient_address, 18)
            ], widths)
        
        print(f"\nTotal delivered: {len(delivered_on_date)} packages")
        
        if utils.confirm_action("Export to CSV?"):
            filename = f"delivered_packages_{date}.csv"
            data = [{"ID": p.package_id, "Recipient": p.recipient_name, "Address": p.recipient_address} for p in delivered_on_date]
            export_to_csv(data, filename, ["ID", "Recipient", "Address"])
    
    utils.pause()


def report_driver_performance(route_db, package_db):
    """
    Generate driver performance report.
    
    Args:
        route_db (RouteDatabase): Route database instance
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get all routes
    2. Group by driver
    3. Calculate:
       - Total packages assigned
       - Total delivered
       - Delivery success rate
    4. Display in table
    5. Option to export
    """
    utils.print_header("Driver Performance Report")
    
    routes = route_db.get_all_routes()
    driver_stats = {}
    
    for route in routes:
        driver = route.driver_name
        if driver not in driver_stats:
            driver_stats[driver] = {"assigned": 0, "delivered": 0}
        
        for pkg_id in route.package_ids:
            pkg = package_db.get_package_by_id(pkg_id)
            if pkg:
                driver_stats[driver]["assigned"] += 1
                if pkg.status == "Delivered":
                    driver_stats[driver]["delivered"] += 1
    
    print("\nDriver Performance:")
    if not driver_stats:
        print("No driver data available.")
    else:
        widths = [20, 10, 10, 10]
        utils.print_table_row(["Driver", "Assigned", "Delivered", "Rate %"], widths)
        print("-" * 52)
        
        for driver, stats in driver_stats.items():
            rate = (stats["delivered"] / stats["assigned"] * 100) if stats["assigned"] > 0 else 0
            utils.print_table_row([
                utils.truncate_string(driver, 18),
                stats["assigned"],
                stats["delivered"],
                f"{rate:.1f}%"
            ], widths)
        
        if utils.confirm_action("Export to CSV?"):
            data = [{"Driver": d, "Assigned": s["assigned"], "Delivered": s["delivered"], "Rate": f"{(s['delivered']/s['assigned']*100) if s['assigned'] > 0 else 0:.1f}%"} for d, s in driver_stats.items()]
            export_to_csv(data, f"driver_performance_{utils.get_today_date()}.csv", ["Driver", "Assigned", "Delivered", "Rate"])
    
    utils.pause()


def report_delayed_deliveries(package_db):
    """
    Generate report of delayed or pending deliveries.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Get packages with "Pending" or "Out for Delivery" status
    2. Show package details and how long pending
    3. Sort by creation date
    4. Option to export
    """
    utils.print_header("Delayed Deliveries Report")
    
    pending = package_db.get_packages_by_status("Pending")
    out_for_delivery = package_db.get_packages_by_status("Out for Delivery")
    delayed = pending + out_for_delivery
    
    print("\nDelayed/Pending Deliveries:")
    if not delayed:
        print("No delayed deliveries.")
    else:
        widths = [12, 20, 15, 20]
        utils.print_table_row(["ID", "Recipient", "Status", "Created"], widths)
        print("-" * 70)
        
        for pkg in delayed:
            utils.print_table_row([
                pkg.package_id,
                utils.truncate_string(pkg.recipient_name, 18),
                pkg.status,
                utils.format_date(pkg.created_at)
            ], widths)
        
        print(f"\nTotal delayed: {len(delayed)} packages")
        
        if utils.confirm_action("Export to CSV?"):
            data = [{"ID": p.package_id, "Recipient": p.recipient_name, "Status": p.status, "Created": p.created_at} for p in delayed]
            export_to_csv(data, f"delayed_deliveries_{utils.get_today_date()}.csv", ["ID", "Recipient", "Status", "Created"])
    
    utils.pause()


def report_fuel_usage_estimates(route_db):
    """
    Generate fuel usage estimate report by route.
    
    Args:
        route_db (RouteDatabase): Route database instance
    
    TODO:
    1. Get all routes
    2. Show estimated fuel per route
    3. Calculate total fuel
    4. Option to export
    """
    utils.print_header("Fuel Usage Estimates")
    
    routes = route_db.get_all_routes()
    
    print("\nFuel Usage by Route:")
    if not routes:
        print("No routes found.")
    else:
        widths = [10, 20, 12, 12]
        utils.print_table_row(["Route ID", "Name", "Packages", "Fuel (L)"], widths)
        print("-" * 57)
        
        total_fuel = 0
        for route in routes:
            fuel = len(route.package_ids) * 2.5
            route.estimated_fuel = fuel
            total_fuel += fuel
            
            utils.print_table_row([
                route.route_id,
                utils.truncate_string(route.route_name, 18),
                len(route.package_ids),
                f"{fuel:.2f}"
            ], widths)
        
        print(f"\nTotal estimated fuel: {total_fuel:.2f} liters")
        
        if utils.confirm_action("Export to CSV?"):
            data = [{"RouteID": r.route_id, "Name": r.route_name, "Packages": len(r.package_ids), "Fuel": f"{len(r.package_ids)*2.5:.2f}"} for r in routes]
            export_to_csv(data, f"fuel_usage_{utils.get_today_date()}.csv", ["RouteID", "Name", "Packages", "Fuel"])
    
    utils.pause()


def report_problematic_addresses(package_db):
    """
    Generate report of addresses with repeated delivery issues.
    
    Args:
        package_db (PackageDatabase): Package database instance
    
    TODO:
    1. Group packages by address
    2. Find addresses with multiple pending/delayed deliveries
    3. Display problematic addresses
    4. Option to export
    """
    utils.print_header("Problematic Addresses Report")
    
    packages = package_db.get_all_packages()
    address_issues = {}
    
    for pkg in packages:
        if pkg.status != "Delivered":
            addr = pkg.recipient_address
            if addr not in address_issues:
                address_issues[addr] = 0
            address_issues[addr] += 1
    
    problematic = {addr: count for addr, count in address_issues.items() if count > 1}
    
    print("\nAddresses with Multiple Pending Deliveries:")
    if not problematic:
        print("No problematic addresses found.")
    else:
        widths = [40, 10]
        utils.print_table_row(["Address", "Issues"], widths)
        print("-" * 52)
        
        for addr, count in sorted(problematic.items(), key=lambda x: x[1], reverse=True):
            utils.print_table_row([
                utils.truncate_string(addr, 38),
                count
            ], widths)
        
        print(f"\nTotal problematic addresses: {len(problematic)}")
    
    utils.pause()


def export_to_csv(data, filename, headers):
    """
    Export report data to CSV file.
    
    Args:
        data: List of dictionaries containing report data
        filename: Output filename
        headers: CSV column headers
    
    TODO:
    1. Create CSV file
    2. Write headers
    3. Write data rows
    4. Save file
    """
    try:
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        utils.print_success(f"Report exported to {filename}")
    except Exception as e:
        utils.print_error(f"Failed to export: {str(e)}")


def generate_summary_statistics(package_db, route_db):
    """
    Generate overall system statistics.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    
    TODO: Show overall stats:
    - Total packages
    - Total routes
    - Delivery completion rate
    - Average packages per route
    """
    utils.print_header("System Summary Statistics")
    
    packages = package_db.get_all_packages()
    routes = route_db.get_all_routes()
    
    total_packages = len(packages)
    total_routes = len(routes)
    delivered = len([p for p in packages if p.status == "Delivered"])
    completion_rate = (delivered / total_packages * 100) if total_packages > 0 else 0
    
    total_assigned = sum([len(r.package_ids) for r in routes])
    avg_packages = (total_assigned / total_routes) if total_routes > 0 else 0
    
    print(f"\nTotal Packages: {total_packages}")
    print(f"Total Routes: {total_routes}")
    print(f"Delivered Packages: {delivered}")
    print(f"Delivery Completion Rate: {completion_rate:.1f}%")
    print(f"Average Packages per Route: {avg_packages:.1f}")
    print(f"Pending Packages: {len([p for p in packages if p.status == 'Pending'])}")
    print(f"Out for Delivery: {len([p for p in packages if p.status == 'Out for Delivery'])}")
    
    utils.pause()


def reports_menu(package_db, route_db):
    """
    Display reports menu and handle user choices.
    
    Args:
        package_db (PackageDatabase): Package database instance
        route_db (RouteDatabase): Route database instance
    
    TODO: Create menu loop with all reporting options
    """
    while True:
        utils.clear_screen()
        utils.print_header("Reports & Analytics")
        print("1. Packages Delivered Per Day")
        print("2. Driver Performance Report")
        print("3. Delayed Deliveries Report")
        print("4. Fuel Usage Estimates")
        print("5. Problematic Addresses")
        print("6. System Summary Statistics")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            report_packages_delivered_per_day(package_db)
        elif choice == '2':
            report_driver_performance(route_db, package_db)
        elif choice == '3':
            report_delayed_deliveries(package_db)
        elif choice == '4':
            report_fuel_usage_estimates(route_db)
        elif choice == '5':
            report_problematic_addresses(package_db)
        elif choice == '6':
            generate_summary_statistics(package_db, route_db)
        elif choice == '0':
            break
