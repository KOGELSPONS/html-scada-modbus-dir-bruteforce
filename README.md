# HTML SCADA Modbus Directory Bruteforce
This Python script is designed to brute-force directories and files for CTF challenges. It supports login authentication and customizable directories and filenames.

## Installation

### Install dependencies
```bash
sudo apt install python3-requests
```

### Clone the repository:
```bash
git clone https://github.com/KOGELSPONS/html-scada-modbus-dir-bruteforce
```

### Navigate into the project folder:
```bash
cd html-scada-modbus-dir-bruteforce
```

## Configuration

### Installing the dependencies
Instead of installing dependencies manually, you can install all required dependencies from the `requirements.txt` file:
```bash
pip3 install -r requirements.txt
```

### Edit the config
```bash
nano config.json
```

### Modify the fields
Do not copy this JSON directly. Edit the downloaded file to avoid breaking the code, example `config.json`:
```json
{
  "ip": "192.168.56.0", // IP of the webpage
  "port": 80, //Standard HTTP port is 80, and standard HTTPS port is 443, but they can be configured to use different ports
  "username": "admin", // Login username
  "password": "admin123", // Login password
  "readability": true //Set to true if you want a .html summary instead of the full .html output of the found directory
}
```
### Save the file:
After editing, press CTRL + X to exit nano.
Press Y to confirm saving.
Press Enter to save the file.

### Edit directories/filenames in directories_filenames.json:
```bash 
nano directories_filenames.json
```
w
Add or remove directories and filenames you want to test in the lists, or use the default ones:

```json
{
  "directories": ["/etc/", "/home/", "/var/log/"],
  "filenames": ["passwd", "shadow", "nginx.conf"]
}
```
Save the file the same way (CTRL + X, Y, Enter).

## Running the Script
Once the configuration is complete, run the Python script:

## Run the script:
```bash 
python3 login_bruteforce.py
```
The script will log in, brute-force directories, and output results based on your configuration.

# Troubleshooting

If the script doesn't work as expected, the code is easily modifiable. You can make adjustments by using ChatGPT or similar tools to help with any customizations or fixes needed. Alternatively, you can use this code as a base/example for your own projects.

