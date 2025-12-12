"""
FreshRoute Logistics - Main Application
Assigned to: ALLEN

Main application flow integrating all system modules.
"""

from database_packages import PackageDatabase
from database_routes import RouteDatabase
import package_manager
import route_manager
import tracking
import reports
import utils


def main():
    package_db = PackageDatabase()
    route_db = RouteDatabase()

    while True:
        utils.clear_screen()
        utils.print_header("FreshRoute Logistics System")

        print("Main Menu:")
        print("1. Package Management")
        print("2. Route Management")
        print("3. Delivery Tracking")
        print("4. Reports")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            package_manager.package_management_menu(package_db)

        elif choice == "2":
            route_manager.route_management_menu(route_db, package_db)

        elif choice == "3":
            tracking.tracking_menu(package_db, route_db)

        elif choice == "4":
            show_reports_menu(package_db, route_db)

        elif choice == "5":
            print("Exiting system...")
            break

        else:
            utils.print_error("Invalid choice. Try again.")
            utils.pause()


def show_reports_menu(package_db, route_db):
    while True:
        utils.clear_screen()
        utils.print_header("Reports Menu")

        print("1. Packages Delivered per Day")
        print("2. Driver Performance Report")
        print("3. Delayed Deliveries Report")
        print("4. Fuel Usage Estimates")
        print("5. Problematic Addresses Report")
        print("6. Summary Statistics")
        print("0. Back to Main Menu")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            reports.report_packages_delivered_per_day(package_db)

        elif choice == "2":
            reports.report_driver_performance(route_db, package_db)

        elif choice == "3":
            reports.report_delayed_deliveries(package_db)

        elif choice == "4":
            reports.report_fuel_usage_estimates(route_db)

        elif choice == "5":
            reports.report_problematic_addresses(package_db)

        elif choice == "6":
            reports.generate_summary_statistics(package_db, route_db)

        elif choice == "0":
            break

        else:
            utils.print_error("Invalid choice. Try again.")
            utils.pause()


if __name__ == "__main__":
    main()
