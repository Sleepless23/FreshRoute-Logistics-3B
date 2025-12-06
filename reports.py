"""
Reporting Module for FreshRoute Logistics System
Generate reports on deliveries, driver performance, and delays
"""

import csv
from datetime import datetime
from typing import List
from models import Package, Route
from database import Database
import utils


class ReportGenerator:
    """Generate various reports for the logistics system"""
    
    def __init__(self, db: Database):
        self.db = db
    
    def print_packages_delivered_per_day(self, date: str = None):
        """Print report of packages delivered on a specific day"""
        utils.print_header("PACKAGES DELIVERED PER DAY REPORT")
        
        if not date:
            date = utils.get_date_input("Enter date")
        
        packages = self.db.get_all_packages()
        
        # Find packages delivered on this date
        delivered = []
        for p in packages:
            # Check if package is delivered
            if p.status == "Delivered":
                # Check if it has a delivery date
                if p.delivered_at:
                    # Check if delivery date matches
                    if p.delivered_at.startswith(date):
                        delivered.append(p)
        
        print(f"\nDate: {date}")
        print(f"Total Packages Delivered: {len(delivered)}")
        
        if delivered:
            print("\nDelivered Packages:")
            utils.print_table_separator([15, 20, 25, 15])
            utils.print_table_row(["Package ID", "Recipient", "Address", "Delivered At"], 
                                [15, 20, 25, 15])
            utils.print_table_separator([15, 20, 25, 15])
            
            for p in delivered:
                time = utils.format_date(p.delivered_at) if p.delivered_at else "N/A"
                utils.print_table_row([
                    p.package_id,
                    utils.truncate_string(p.recipient_name, 20),
                    utils.truncate_string(p.recipient_address, 25),
                    time
                ], [15, 20, 25, 15])
        else:
            print("\nNo packages delivered on this date.")
        
        # Export option
        if delivered and utils.confirm_action("\nExport to CSV?"):
            self._export_delivered_packages(delivered, date)
    
    def print_driver_performance(self):
        """Print report of driver delivery performance"""
        utils.print_header("DRIVER PERFORMANCE REPORT")
        
        routes = self.db.get_all_routes()
        packages = self.db.get_all_packages()
        
        if not routes:
            print("\nNo routes found.")
            return
        
        # Calculate performance per driver
        driver_stats = {}
        
        for route in routes:
            driver = route.driver_name
            if driver not in driver_stats:
                driver_stats[driver] = {
                    'total_packages': 0,
                    'delivered': 0,
                    'pending': 0,
                    'out_for_delivery': 0,
                    'routes_count': 0
                }
            
            driver_stats[driver]['routes_count'] += 1
            # Find packages for this route
            route_packages = []
            for p in packages:
                if p.route_id == route.route_id:
                    route_packages.append(p)
            
            for p in route_packages:
                driver_stats[driver]['total_packages'] += 1
                if p.status == "Delivered":
                    driver_stats[driver]['delivered'] += 1
                elif p.status == "Pending":
                    driver_stats[driver]['pending'] += 1
                elif p.status == "Out for Delivery":
                    driver_stats[driver]['out_for_delivery'] += 1
        
        # Display results
        print(f"\nTotal Drivers: {len(driver_stats)}")
        print("\nDriver Performance:")
        utils.print_table_separator([20, 10, 12, 12, 12, 15])
        utils.print_table_row(["Driver Name", "Routes", "Total Pkgs", "Delivered", "Pending", "Success Rate"], 
                            [20, 10, 12, 12, 12, 15])
        utils.print_table_separator([20, 10, 12, 12, 12, 15])
        
        for driver, stats in sorted(driver_stats.items()):
            success_rate = (stats['delivered'] / stats['total_packages'] * 100) if stats['total_packages'] > 0 else 0
            utils.print_table_row([
                utils.truncate_string(driver, 20),
                stats['routes_count'],
                stats['total_packages'],
                stats['delivered'],
                stats['pending'],
                f"{success_rate:.1f}%"
            ], [20, 10, 12, 12, 12, 15])
        
        # Export option
        if utils.confirm_action("\nExport to CSV?"):
            self._export_driver_performance(driver_stats)
    
    def print_delayed_deliveries(self):
        """Print report of packages with delays or pending status"""
        utils.print_header("DELAYED DELIVERIES REPORT")
        
        packages = self.db.get_all_packages()
        
        # Consider packages pending or out for delivery as potentially delayed
        delayed = []
        for p in packages:
            if p.status == "Pending":
                delayed.append(p)
            elif p.status == "Out for Delivery":
                delayed.append(p)
        
        print(f"\nTotal Potentially Delayed Packages: {len(delayed)}")
        
        if delayed:
            print("\nPackage Status:")
            utils.print_table_separator([15, 20, 25, 15, 20])
            utils.print_table_row(["Package ID", "Recipient", "Address", "Status", "Created At"], 
                                [15, 20, 25, 15, 20])
            utils.print_table_separator([15, 20, 25, 15, 20])
            
            for p in delayed:
                utils.print_table_row([
                    p.package_id,
                    utils.truncate_string(p.recipient_name, 20),
                    utils.truncate_string(p.recipient_address, 25),
                    p.status,
                    utils.format_date(p.created_at)
                ], [15, 20, 25, 15, 20])
        else:
            print("\nNo delayed deliveries found. All packages are delivered!")
        
        # Export option
        if delayed and utils.confirm_action("\nExport to CSV?"):
            self._export_delayed_deliveries(delayed)
    
    def print_fuel_usage_estimates(self):
        """Print report of fuel usage estimates per route"""
        utils.print_header("FUEL USAGE ESTIMATES REPORT")
        
        routes = self.db.get_all_routes()
        
        if not routes:
            print("\nNo routes found.")
            return
        
        print(f"\nTotal Routes: {len(routes)}")
        
        # Display fuel estimates
        print("\nFuel Usage by Route:")
        utils.print_table_separator([15, 25, 15, 15, 15])
        utils.print_table_row(["Route ID", "Route Name", "Driver", "Packages", "Est. Fuel (L)"], 
                            [15, 25, 15, 15, 15])
        utils.print_table_separator([15, 25, 15, 15, 15])
        
        total_fuel = 0
        for route in routes:
            packages_count = len(route.package_ids)
            fuel = route.estimated_fuel
            total_fuel += fuel
            
            utils.print_table_row([
                route.route_id,
                utils.truncate_string(route.route_name, 25),
                utils.truncate_string(route.driver_name, 15),
                packages_count,
                f"{fuel:.2f}"
            ], [15, 25, 15, 15, 15])
        
        print(f"\nTotal Estimated Fuel Usage: {total_fuel:.2f} liters")
        
        # Export option
        if utils.confirm_action("\nExport to CSV?"):
            self._export_fuel_usage(routes)
    
    def print_problematic_addresses(self):
        """Print report of delivery addresses with multiple issues"""
        utils.print_header("PROBLEMATIC ADDRESSES REPORT")
        
        packages = self.db.get_all_packages()
        
        # Count delivery attempts per address
        address_stats = {}
        
        for p in packages:
            addr = p.recipient_address.lower().strip()
            if addr not in address_stats:
                address_stats[addr] = {
                    'address': p.recipient_address,
                    'total': 0,
                    'delivered': 0,
                    'pending': 0,
                    'packages': []
                }
            
            address_stats[addr]['total'] += 1
            address_stats[addr]['packages'].append(p.package_id)
            
            if p.status == "Delivered":
                address_stats[addr]['delivered'] += 1
            elif p.status in ["Pending", "Out for Delivery"]:
                address_stats[addr]['pending'] += 1
        
        # Find problematic addresses (multiple packages, high pending rate)
        problematic = []
        for addr, stats in address_stats.items():
            if stats['total'] >= 2 and stats['pending'] > 0:
                failure_rate = (stats['pending'] / stats['total']) * 100
                problematic.append({
                    'address': stats['address'],
                    'total': stats['total'],
                    'pending': stats['pending'],
                    'failure_rate': failure_rate
                })
        
        # Sort by failure rate (bubble sort for simplicity)
        # Bubble sort - easier to understand for beginners
        for i in range(len(problematic)):
            for j in range(len(problematic) - 1 - i):
                if problematic[j]['failure_rate'] < problematic[j + 1]['failure_rate']:
                    # Swap them
                    temp = problematic[j]
                    problematic[j] = problematic[j + 1]
                    problematic[j + 1] = temp
        
        print(f"\nProblematic Addresses Found: {len(problematic)}")
        
        if problematic:
            print("\nAddresses with Issues:")
            utils.print_table_separator([35, 12, 12, 15])
            utils.print_table_row(["Address", "Total Pkgs", "Pending", "Issue Rate"], 
                                [35, 12, 12, 15])
            utils.print_table_separator([35, 12, 12, 15])
            
            for item in problematic:
                utils.print_table_row([
                    utils.truncate_string(item['address'], 35),
                    item['total'],
                    item['pending'],
                    f"{item['failure_rate']:.1f}%"
                ], [35, 12, 12, 15])
        else:
            print("\nNo problematic addresses found.")
        
        # Export option
        if problematic and utils.confirm_action("\nExport to CSV?"):
            self._export_problematic_addresses(problematic)
    
    # === EXPORT FUNCTIONS ===
    
    def _export_delivered_packages(self, packages: List[Package], date: str):
        """Export delivered packages to CSV"""
        filename = f"delivered_packages_{date}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Package ID', 'Sender', 'Recipient', 'Address', 'Phone', 
                               'Weight', 'Category', 'Delivered At', 'Proof of Delivery'])
                
                for p in packages:
                    writer.writerow([
                        p.package_id, p.sender, p.recipient_name, p.recipient_address,
                        p.recipient_phone, p.weight, p.category, p.delivered_at or '',
                        p.proof_of_delivery or ''
                    ])
            
            utils.print_success(f"Report exported to {filename}")
        except Exception as e:
            utils.print_error(f"Failed to export report: {e}")
    
    def _export_driver_performance(self, driver_stats: dict):
        """Export driver performance to CSV"""
        filename = f"driver_performance_{utils.get_today_date()}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Driver Name', 'Routes Count', 'Total Packages', 
                               'Delivered', 'Pending', 'Success Rate'])
                
                for driver, stats in sorted(driver_stats.items()):
                    success_rate = (stats['delivered'] / stats['total_packages'] * 100) if stats['total_packages'] > 0 else 0
                    writer.writerow([
                        driver, stats['routes_count'], stats['total_packages'],
                        stats['delivered'], stats['pending'], f"{success_rate:.2f}%"
                    ])
            
            utils.print_success(f"Report exported to {filename}")
        except Exception as e:
            utils.print_error(f"Failed to export report: {e}")
    
    def _export_delayed_deliveries(self, packages: List[Package]):
        """Export delayed deliveries to CSV"""
        filename = f"delayed_deliveries_{utils.get_today_date()}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Package ID', 'Recipient', 'Address', 'Phone', 
                               'Status', 'Route ID', 'Created At'])
                
                for p in packages:
                    writer.writerow([
                        p.package_id, p.recipient_name, p.recipient_address,
                        p.recipient_phone, p.status, p.route_id or 'Not Assigned',
                        p.created_at
                    ])
            
            utils.print_success(f"Report exported to {filename}")
        except Exception as e:
            utils.print_error(f"Failed to export report: {e}")
    
    def _export_fuel_usage(self, routes: List[Route]):
        """Export fuel usage to CSV"""
        filename = f"fuel_usage_{utils.get_today_date()}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Route ID', 'Route Name', 'Driver', 'Driver Phone', 
                               'Date', 'Packages Count', 'Estimated Fuel (L)'])
                
                for route in routes:
                    writer.writerow([
                        route.route_id, route.route_name, route.driver_name,
                        route.driver_phone, route.date, len(route.package_ids),
                        f"{route.estimated_fuel:.2f}"
                    ])
            
            utils.print_success(f"Report exported to {filename}")
        except Exception as e:
            utils.print_error(f"Failed to export report: {e}")
    
    def _export_problematic_addresses(self, addresses: list):
        """Export problematic addresses to CSV"""
        filename = f"problematic_addresses_{utils.get_today_date()}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Address', 'Total Packages', 'Pending Packages', 'Issue Rate'])
                
                for item in addresses:
                    writer.writerow([
                        item['address'], item['total'], item['pending'],
                        f"{item['failure_rate']:.2f}%"
                    ])
            
            utils.print_success(f"Report exported to {filename}")
        except Exception as e:
            utils.print_error(f"Failed to export report: {e}")
