"""
TODO: Implement all package management functions.
"""

from database_packages import PackageDatabase
from models import Package
import utils


def register_package(db):
    """
    Register a new package in the system.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO: 
    1. Generate package ID
    2. Get package details from user
    3. Validate input
    4. Create Package object
    5. Save to database
    """
    utils.print_header("Register New Package")
    
    packages = db.get_all_packages()
    package_id = utils.generate_id("PKG", [p.package_id for p in packages])
    
    sender = utils.get_input("Sender name")
    recipient_name = utils.get_input("Recipient name")
    recipient_address = utils.get_input("Recipient address")
    recipient_phone = utils.get_input("Recipient phone")
    weight = utils.get_number_input("Package weight (kg)", 0.1, 1000)
    
    print("\\nCategories: Electronics, Documents, Food, Clothing, Other")
    category = utils.get_input("Package category", "Other")
    
    package = Package(package_id, sender, recipient_name, recipient_address, 
                     recipient_phone, weight, category)
    
    if db.add_package(package):
        utils.print_success(f"Package {package_id} registered successfully!")
    else:
        utils.print_error("Failed to register package")
    
    utils.pause()


def view_all_packages(db):
    """
    Display all packages in a table format.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO: Get all packages and display in formatted table
    """
    utils.print_header("All Packages")
    
    packages = db.get_all_packages()
    
    if not packages:
        print("No packages found.")
    else:
        widths = [12, 20, 20, 15, 10]
        utils.print_table_row(["ID", "Recipient", "Address", "Status", "Weight"], widths)
        print("-" * 80)
        
        for pkg in packages:
            utils.print_table_row([
                pkg.package_id,
                utils.truncate_string(pkg.recipient_name, 18),
                utils.truncate_string(pkg.recipient_address, 18),
                pkg.status,
                f"{pkg.weight} kg"
            ], widths)
        
        print(f"\\nTotal: {len(packages)} packages")
    
    utils.pause()


def search_package(db):
    """
    Search for a package by ID and display details.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO: 
    1. Get package ID from user
    2. Search in database
    3. Display package details
    """
    utils.print_header("Search Package")
    
    package_id = utils.get_input("Enter package ID")
    package = db.get_package_by_id(package_id)
    
    if package:
        print(f"\nPackage ID: {package.package_id}")
        print(f"Sender: {package.sender}")
        print(f"Recipient: {package.recipient_name}")
        print(f"Address: {package.recipient_address}")
        print(f"Phone: {package.recipient_phone}")
        print(f"Weight: {package.weight} kg")
        print(f"Category: {package.category}")
        print(f"Status: {package.status}")
        print(f"Route ID: {package.route_id or 'Not assigned'}")
    else:
        utils.print_error("Package not found")
    
    utils.pause()


def edit_package(db):
    """
    Edit package details.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO:
    1. Get package ID
    2. Load package data
    3. Show current details
    4. Get new details from user
    5. Update database
    """
    utils.print_header("Edit Package")
    
    package_id = utils.get_input("Enter package ID")
    package = db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    print(f"\nEditing package {package_id}")
    package.recipient_name = utils.get_input("Recipient name", package.recipient_name)
    package.recipient_address = utils.get_input("Recipient address", package.recipient_address)
    package.recipient_phone = utils.get_input("Recipient phone", package.recipient_phone)
    package.category = utils.get_input("Category", package.category)
    
    if db.update_package(package):
        utils.print_success("Package updated successfully!")
    else:
        utils.print_error("Failed to update package")
    
    utils.pause()


def delete_package(db):
    """
    Delete a package from the system.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO:
    1. Get package ID
    2. Show package details
    3. Confirm deletion
    4. Delete from database
    """
    utils.print_header("Delete Package")
    
    package_id = utils.get_input("Enter package ID")
    package = db.get_package_by_id(package_id)
    
    if not package:
        utils.print_error("Package not found")
        utils.pause()
        return
    
    print(f"\nPackage: {package.recipient_name} - {package.recipient_address}")
    
    if utils.confirm_action("Are you sure you want to delete this package?"):
        if db.delete_package(package_id):
            utils.print_success("Package deleted successfully!")
        else:
            utils.print_error("Failed to delete package")
    
    utils.pause()


def view_unassigned_packages(db):
    """
    View packages not assigned to any route.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO: Get and display unassigned packages
    """
    utils.print_header("Unassigned Packages")
    
    packages = db.get_unassigned_packages()
    
    if not packages:
        print("No unassigned packages found.")
    else:
        widths = [12, 20, 20, 10]
        utils.print_table_row(["ID", "Recipient", "Address", "Weight"], widths)
        print("-" * 65)
        
        for pkg in packages:
            utils.print_table_row([
                pkg.package_id,
                utils.truncate_string(pkg.recipient_name, 18),
                utils.truncate_string(pkg.recipient_address, 18),
                f"{pkg.weight} kg"
            ], widths)
        
        print(f"\nTotal: {len(packages)} packages")
    
    utils.pause()


def package_management_menu(db):
    """
    Display package management menu and handle user choices.
    
    Args:
        db (PackageDatabase): Package database instance
    
    TODO: Create menu loop with all package operations
    """
    while True:
        utils.clear_screen()
        utils.print_header("Package Management")
        print("1. Register New Package")
        print("2. View All Packages")
        print("3. Search Package")
        print("4. Edit Package")
        print("5. Delete Package")
        print("6. View Unassigned Packages")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            register_package(db)
        elif choice == '2':
            view_all_packages(db)
        elif choice == '3':
            search_package(db)
        elif choice == '4':
            edit_package(db)
        elif choice == '5':
            delete_package(db)
        elif choice == '6':
            view_unassigned_packages(db)
        elif choice == '0':
            break