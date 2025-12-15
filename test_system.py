import unittest
from models import Package, Route

# How to run test: python -m unittest test_system.py -v

class TestPackageModel(unittest.TestCase):
    """Simple test cases for Package model."""
    
    def test_create_package(self):
        """Test 1: Create a package with basic information."""
        package = Package(
            package_id="PKG001",
            sender="Sender Name",
            recipient_name="Recipient Name",
            recipient_address="Address Line 1, Address Line 2",
            recipient_phone="09121231212",
            weight=5.5,
            category="Others"
        )
        
        self.assertEqual(package.package_id, "PKG001")
        self.assertEqual(package.sender, "Sender Name")
        self.assertEqual(package.status, "Pending")
    
    def test_update_package_status(self):
        """Test 2: Update package status to Delivered."""
        package = Package("PKG002", "Sender Name 2", "Recipient Name 2", 
                         "Address Line A, Address Line B", "09123456789", 2.5, "Documents")
        
        package.update_status("Delivered")
        
        self.assertEqual(package.status, "Delivered")
        self.assertIsNotNone(package.delivered_at)
    
    def test_package_to_dict(self):
        """Test 3: Convert package to dictionary."""
        package = Package("PKG003", "Sender Name 3", "Recipient Name 3", 
                         "Address Line X, Address Line Y", "09187654321", 3.0, "Food")
        
        pkg_dict = package.to_dict()
        
        self.assertIsInstance(pkg_dict, dict)
        self.assertEqual(pkg_dict['package_id'], "PKG003")
        self.assertEqual(pkg_dict['sender'], "Sender Name 3")


class TestRouteModel(unittest.TestCase):
    """Simple test cases for Route model."""
    
    def test_create_route(self):
        """Test 4: Create a delivery route."""
        route = Route(
            route_id="RT001",
            route_name="Route Name 1",
            driver_name="Driver Name 1",
            driver_phone="09111222333",
            date="2025-12-15"
        )
        
        self.assertEqual(route.route_id, "RT001")
        self.assertEqual(route.driver_name, "Driver Name 1")
        self.assertEqual(len(route.package_ids), 0)
    
    def test_add_package_to_route(self):
        """Test 5: Add packages to a route."""
        route = Route("RT002", "Route Name 2", "Driver Name 2", 
                     "09444555666", "2025-12-16")
        
        route.add_package("PKG001")
        route.add_package("PKG002")
        
        self.assertEqual(len(route.package_ids), 2)
        self.assertIn("PKG001", route.package_ids)
        self.assertIn("PKG002", route.package_ids)


if __name__ == "__main__":
    print("Running 5 Simple Unit Tests for FreshRoute Logistics\n")
    unittest.main(verbosity=2)
