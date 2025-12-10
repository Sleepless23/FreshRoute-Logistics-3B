"""
FreshRoute Logistics - Package Database Operations
Assigned to: JOHN BRETT

TODO: Implement all package database operations (CRUD).
"""

import json
import os
from models import Package


class PackageDatabase:
    """Handles package data storage and retrieval using JSON file."""
    
    def __init__(self, data_dir="data"):
        """
        Initialize package database.
        
        Args:
            data_dir (str): Directory for data files
        
        TODO: Set up database file path and initialize
        """
        self.data_dir = data_dir
        self.packages_file = os.path.join(data_dir, "packages.json")
        self._initialize()
    
    def _initialize(self):
        """
        Create data directory and file if they don't exist.
        
        TODO: Create directory and empty packages.json file
        """
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        if not os.path.exists(self.packages_file):
            with open(self.packages_file, 'w') as f:
                json.dump([], f)
    
    def _read_packages(self):
        """
        Read packages from JSON file.
        
        Returns:
            list: List of package dictionaries
        
        TODO: Read and parse JSON file
        """
        with open(self.packages_file, 'r') as f:
            return json.load(f)
    
    def _write_packages(self, packages_data):
        """
        Write packages to JSON file.
        
        Args:
            packages_data (list): List of package dictionaries
        
        TODO: Write data to JSON file with proper formatting
        """
        with open(self.packages_file, 'w') as f:
            json.dump(packages_data, f, indent=2)
    
    def get_all_packages(self):
        """
        Get all packages from database.
        
        Returns:
            List of Package objects
        
        TODO: Read JSON and convert to Package objects
        """
        data = self._read_packages()
        return [Package.from_dict(pkg) for pkg in data]
    
    def get_package_by_id(self, package_id):
        """
        Get a specific package by ID.
        
        Args:
            package_id: Package ID to search for
        
        Returns:
            Package object if found, None otherwise
        
        TODO: Search for package by ID
        """
        packages = self.get_all_packages()
        for pkg in packages:
            if pkg.package_id == package_id:
                return pkg
        return None
    
    def add_package(self, package):
        """
        Add a new package to database.
        
        Args:
            package: Package object to add
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Add package to JSON file (check for duplicates)
        """
        data = self._read_packages()
        for pkg in data:
            if pkg['package_id'] == package.package_id:
                return False
        data.append(package.to_dict())
        self._write_packages(data)
        return True
    
    def update_package(self, package):
        """
        Update an existing package.
        
        Args:
            package: Package object with updated data
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Update package in JSON file
        """
        data = self._read_packages()
        for i, pkg in enumerate(data):
            if pkg['package_id'] == package.package_id:
                data[i] = package.to_dict()
                self._write_packages(data)
                return True
        return False
    
    def delete_package(self, package_id):
        """
        Delete a package by ID.
        
        Args:
            package_id: Package ID to delete
        
        Returns:
            bool: True if successful, False otherwise
        
        TODO: Remove package from JSON file
        """
        data = self._read_packages()
        for i, pkg in enumerate(data):
            if pkg['package_id'] == package_id:
                data.pop(i)
                self._write_packages(data)
                return True
        return False
    
    def get_packages_by_status(self, status):
        """
        Get all packages with a specific status.
        
        Args:
            status: Status to filter by
        
        Returns:
            List of matching packages
        
        TODO: Filter packages by status
        """
        packages = self.get_all_packages()
        return [pkg for pkg in packages if pkg.status == status]
    
    def get_packages_by_route(self, route_id):
        """
        Get all packages assigned to a specific route.
        
        Args:
            route_id: Route ID to filter by
        
        Returns:
            List of matching packages
        
        TODO: Filter packages by route ID
        """
        packages = self.get_all_packages()
        return [pkg for pkg in packages if pkg.route_id == route_id]
    
    def get_unassigned_packages(self):
        """
        Get all packages not assigned to any route.
        
        Returns:
            List[Package]: List of unassigned packages
        
        TODO: Filter packages without route assignment
        """
        packages = self.get_all_packages()
        return [pkg for pkg in packages if pkg.route_id is None]