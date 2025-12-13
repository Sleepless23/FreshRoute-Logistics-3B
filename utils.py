import re
import os
from datetime import datetime


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
        value = input(f"{prompt}: ")
        if not value:
            return None
        try:
            num = float(value)
            if min_val <= num <= max_val:
                return num
            print(f"Please enter a number between {min_val} and {max_val}")
        except:
            print("Invalid number")


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
        print(f"Invalid choice. Choose from {valid_choices}")


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
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except:
            print("Invalid date format. Use YYYY-MM-DD")


def confirm_action(message):
    """
    Ask user to confirm an action (yes/no).
    
    Args:
        message (str): Confirmation message
    
    Returns:
        bool: True if confirmed, False otherwise
    
    TODO: Implement yes/no confirmation
    """
    choice = input(f"{message} (y/n): ").lower()
    return choice == 'y'


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
    digits = re.sub(r'\D', '', phone)
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
    digits = re.sub(r'\D', '', phone)
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
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return date_str


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
    if len(text) > max_length:
        return text[:max_length-3] + "..."
    return text


# ===== DISPLAY FUNCTIONS =====

def clear_screen():
    """
    Clear the terminal screen.
    
    TODO: Clear screen (use 'clear' for Mac/Linux, 'cls' for Windows)
    """
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title):
    """
    Print a formatted header.
    
    Args:
        title (str): Header title
    
    TODO: Print nice header with borders
    """
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_table_row(columns, widths):
    """
    Print a formatted table row.
    
    Args:
        columns (list): Column values
        widths (list): Column widths
    
    TODO: Print row with fixed column widths
    """
    row = ""
    for col, width in zip(columns, widths):
        row += str(col)[:width].ljust(width) + " "
    print(row)


def pause():
    """
    Pause and wait for user to press Enter.
    
    TODO: Wait for Enter key
    """
    input("\nPress Enter to continue...")


# ===== MESSAGE FUNCTIONS =====

def print_success(message):
    """Print success message with checkmark."""
    print(f"✓ {message}")


def print_error(message):
    """Print error message with X mark."""
    print(f"✗ {message}")


def print_warning(message):
    """Print warning message with warning symbol."""
    print(f"⚠ {message}")


# ===== UTILITY FUNCTIONS =====

def get_today_date():
    """
    Get today's date in YYYY-MM-DD format.
    
    Returns:
        str: Today's date
    
    TODO: Return current date as string
    """
    return datetime.now().strftime('%Y-%m-%d')


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
    if not existing_ids:
        return f"{prefix}0001"
    nums = []
    for id in existing_ids:
        try:
            num = int(id.replace(prefix, ''))
            nums.append(num)
        except:
            pass
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}{next_num:04d}"