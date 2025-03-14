import os
import subprocess
import signal
import sys
import time

# List of modules in the order they should be executed in automated mode
MODULES = [
    "database_importer.py",
    "case_sorter.py",
    "case_number_check.py",
    "timestamp_check.py",
    "ascii_name_check.py",
    "discord_user_check.py",
    "discord_rate_limit_check.py",
    "discord_invite_check.py",
    "url_check.py",
    "virustotal_check.py",
    "ipinfo_check.py"
]

# Path to the modules directory
MODULES_DIR = "modules"

# Global variable to track if a module is currently running
current_process = None


def run_module(module_name):
    """
    Run a specific module using subprocess.
    """
    global current_process
    module_path = os.path.join(MODULES_DIR, module_name)
    print(f"\nRunning module: {module_name}...")
    try:
        current_process = subprocess.Popen(["python", module_path])
        current_process.wait()  # Wait for the process to complete
    except KeyboardInterrupt:
        print(f"\nModule {module_name} interrupted by user.")
    finally:
        current_process = None
    print(f"\nModule {module_name} completed.")


def stop_current_module():
    """
    Stop the currently running module.
    """
    global current_process
    if current_process:
        print("\nStopping the current module...")
        current_process.terminate()
        current_process = None
        print("Module stopped.")
    else:
        print("\nNo module is currently running.")


def automated_mode():
    """
    Run all modules in automated mode.
    """
    print("\nRunning in automated mode...")
    for module in MODULES:
        run_module(module)
        print(f"Completed: {module}")
    print("\nAutomated mode completed all modules.")


def manual_mode():
    """
    Run modules in manual mode, allowing the user to choose which module to run.
    """
    while True:
        print("\nManual Mode - Available Modules:")
        for i, module in enumerate(MODULES, start=1):
            print(f"{i}. {module}")
        print("0. Return to main menu")

        try:
            choice = int(input("\nEnter the number of the module to run (or 0 to return to main menu): "))
            if choice == 0:
                break
            elif 1 <= choice <= len(MODULES):
                run_module(MODULES[choice - 1])
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main_menu():
    """
    Display the main menu and handle user input.
    """
    while True:
        print("\nMain Menu:")
        print("1. Run in Automated Mode")
        print("2. Run in Manual Mode")
        print("3. Exit")

        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice == 1:
                automated_mode()
            elif choice == 2:
                manual_mode()
            elif choice == 3:
                print("Exiting the controller script. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def signal_handler(sig, frame):
    """
    Handle keyboard interrupts (Ctrl+C) to stop the current module or exit.
    """
    print("\nCtrl+C detected.")
    if current_process:
        stop_current_module()
    else:
        print("Returning to main menu.")
        main_menu()


if __name__ == "__main__":
    # Set up signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    # Start the main menu
    main_menu()
