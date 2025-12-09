"""
FreshRoute Logistics - Utility Functions
Assigned to: NIVAN and ADRIAN

TODO: Implement all utility and helper functions.
"""

import re
from datetime import datetime

# > ------------------------------------ NIVAN PART START HERE -------------------------------- <

# ===== INPUT FUNCTIONS =====

def get_input(prompt, default=None):
    """
    Get text input from user with optional default value.
    
    Args:
        prompt (str): Input prompt message
        default (str, optional): Default value if user enters nothing
    
    Returns:
        str: User input or default value
    
    TODO: Implement input with default value support
    """
    if default:
        value = input(f"{prompt} [{default}]: ")
        return value if value else default
    return input(f"{prompt}: ")

def get_number_input(prompt, min_val=0, max_val=float('inf')):
    """
    Get numeric input from user with validation.
    
    Args:
        prompt: Input prompt message
        min_val: Minimum allowed value
        max_val: Maximum allowed value
    
    Returns:
        Number if valid, None if user skips
    
    TODO: Implement numeric input with range validation
    """
    while True:
        value = input (f"{prompt}: ")
        if not value:
            return None
        try:
            num = float(value)
            if min_val <= num <= max_val:
                return num
            else:
                print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_choice(prompt, valid_choices):
    """
    Get a choice from user from a list of valid options.
    
    Args:
        prompt (str): Input prompt message
        valid_choices (list): List of valid choices
    
    Returns:
        str: Valid choice selected by user
    
    TODO: Implement choice selection with validation
    """
    while True:
        choice = input(f"{prompt} {valid_choices}: ")
        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice. Please try again.")


def get_date_input(prompt):
    """
    Get date input from user in YYYY-MM-DD format.
    
    Args:
        prompt (str): Input prompt message
    
    Returns:
        str: Date in YYYY-MM-DD format
    
    TODO: Implement date input with format validation
    """
    while True:
        date_str = input(f"{prompt} (YYYY-MM-DD): ")
        try:
            datetime.striptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format. Please enter date as YYYY-MM-DD.")


def confirm_action(message):
    """
    Ask user to confirm an action (yes/no).
    
    Args:
        message (str): Confirmation message
    
    Returns:
        bool: True if confirmed, False otherwise
    
    TODO: Implement yes/no confirmation
    """
    choose = input(f"{message} (y/n): ").lower()
    return choose == 'y'

# ===== VALIDATION FUNCTIONS =====

def validate_phone(phone):
    """
    Validate phone number format.
    
    Args:
        phone (str): Phone number to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    TODO: Check if phone has at least 10 digits
    """
    digits = re.sub (r'\D', '', phone)
    return len(digits) >= 10


def validate_package_id(package_id):
    """
    Validate package ID format.
    
    Args:
        package_id (str): Package ID to validate
    
    Returns:
        bool: True if valid, False otherwise
    
    TODO: Check if package ID format is correct
    """
    return len(package_id) > 0

# ===== FORMATTING FUNCTIONS =====

def format_phone(phone):
    """
    Format phone number for display.
    
    Args:
        phone (str): Phone number
    
    Returns:
        str: Formatted phone number (XXX) XXX-XXXX
    
    TODO: Format phone number nicely
    """
    digits = re.sub (r'\D', '', phone)
    if len(digits) >= 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:10]}"
    return phone

def format_weight(weight):
    """
    Format weight for display.
    
    Args:
        weight (float): Weight in kg
    
    Returns:
        str: Formatted weight with unit
    
    TODO: Format weight as "X.XX kg"
    """
    return f"{weight:.2f} kg"


def format_date(date_str):
    """
    Format ISO date string to readable format.
    
    Args:
        date_str (str): ISO format date string
    
    Returns:
        str: Readable date format
    
    TODO: Convert ISO date to readable format
    """
    if not date_str:
        return "N/A"
    try:
        date_obj = datetime.fromisoformat(date_str)
        return date_obj.strftime("%B %d, %Y %H:%M")
    except:
        return date_str
# > ------------------------------------ NIVAN PART ENDS HERE -------------------------------- <

# > --------------------------------- ADRIAN PART STARTS HERE -------------------------------- <


def truncate_string(text, max_length):
    """
    Truncate string to maximum length with ellipsis.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
    
    Returns:
        str: Truncated text
    
    TODO: Cut text and add "..." if too long
    """
    # TODO: Implement string truncation
    pass


# ===== DISPLAY FUNCTIONS =====

def clear_screen():
    """
    Clear the terminal screen.
    
    TODO: Clear screen (use 'clear' for Mac/Linux, 'cls' for Windows)
    """
    # TODO: Implement clear_screen
    pass


def print_header(title):
    """
    Print a formatted header.
    
    Args:
        title (str): Header title
    
    TODO: Print nice header with borders
    """
    # TODO: Implement print_header
    pass


def print_table_row(columns, widths):
    """
    Print a formatted table row.
    
    Args:
        columns (list): Column values
        widths (list): Column widths
    
    TODO: Print row with fixed column widths
    """
    # TODO: Implement print_table_row
    pass


def pause():
    """
    Pause and wait for user to press Enter.
    
    TODO: Wait for Enter key
    """
    # TODO: Implement pause
    pass


# ===== MESSAGE FUNCTIONS =====

def print_success(message):
    """Print success message with checkmark."""
    # TODO: Implement
    pass


def print_error(message):
    """Print error message with X mark."""
    # TODO: Implement
    pass


def print_warning(message):
    """Print warning message with warning symbol."""
    # TODO: Implement
    pass


# ===== UTILITY FUNCTIONS =====

def get_today_date():
    """
    Get today's date in YYYY-MM-DD format.
    
    Returns:
        str: Today's date
    
    TODO: Return current date as string
    """
    # TODO: Implement get_today_date
    pass


def generate_id(prefix, existing_ids):
    """
    Generate a unique ID with prefix.
    
    Args:
        prefix: ID prefix (e.g., "PKG" or "RT")
        existing_ids: List of existing IDs
    
    Returns:
        New unique ID (e.g., "PKG0001")
    
    TODO: Generate sequential ID number
    """
    # TODO: Implement generate_id
    pass


# > ------------------------------------ ADRIAN PART ENDS HERE -------------------------------- <