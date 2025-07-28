import socket # Import socket module for raw TCP connections
import threading
import time
import sys # Import sys module to access command-line arguments

# Author: Emran Kamal (@ITManiac)

# --- Disclaimer ---
# This script is provided for educational and ethical testing purposes ONLY.
# It is designed to help assess the connection throttling of your OWN SSH servers
# against a simulated DHEat DoS attack.
#
# DO NOT use this script against any system or network that you do not own
# or do not have explicit, written permission to test. Unauthorized use of
# this script may be illegal and could lead to severe consequences.
#
# By using this script, you acknowledge and agree that you are solely responsible
# for any and all actions taken and their consequences. The creator of this script
# is not responsible for any misuse or damage caused by its use.
# ------------------

# --- Configuration ---
# Default values if no command-line arguments are provided
DEFAULT_TARGET_HOST = "127.0.0.1" # Default to localhost if no IP is given
DEFAULT_TARGET_PORT = 22        # Default SSH port
NUM_CONNECTIONS = 50            # Number of connections to attempt

# -------------------

# --- Argument Parsing ---
# Check if enough command-line arguments are provided
if len(sys.argv) < 3:
    print("Usage: python3 dheat_dos_attack_poc.py <target_ip_address> <target_port>")
    print(f"Example: python3 dheat_dos_attack_poc.py {DEFAULT_TARGET_HOST} {DEFAULT_TARGET_PORT}")
    print(f"Using default values: {DEFAULT_TARGET_HOST}:{DEFAULT_TARGET_PORT}")
    TARGET_HOST = DEFAULT_TARGET_HOST
    TARGET_PORT = DEFAULT_TARGET_PORT
else:
    TARGET_HOST = sys.argv[1] # First argument after script name is the IP address
    try:
        TARGET_PORT = int(sys.argv[2]) # Second argument is the port, convert to integer
    except ValueError:
        print(f"Error: Invalid port number '{sys.argv[2]}'. Port must be an integer.")
        sys.exit(1) # Exit if port is not a valid number

# --- Global Variables for Tracking ---
successful_connections = 0
failed_connections = 0
start_time = None
lock = threading.Lock() # A lock to safely update shared counters from multiple threads

# --- Function to Establish TCP Connection ---
def connect_ssh():
    """
    Attempts to establish a single TCP connection to the target host:port.
    This function is designed to be run concurrently by multiple threads.
    It simulates connection attempts to trigger server-side throttling,
    without performing a full SSH handshake or authentication.
    """
    global successful_connections, failed_connections, start_time

    sock = None # Initialize sock to None
    try:
        # Create a new socket using IPv4 and TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout for the connection attempt
        sock.settimeout(5) # 5 seconds timeout

        # Attempt to connect to the target host and port
        sock.connect((TARGET_HOST, TARGET_PORT))

        # If connection is successful, increment the counter.
        # The 'with lock:' statement ensures thread-safe access to the global variable.
        with lock:
            successful_connections += 1
        
    except Exception as e:
        # If any error occurs during connection (e.g., connection refused, timeout),
        # increment the failed connections counter.
        with lock:
            failed_connections += 1
        # Uncomment the line below for detailed error messages during debugging:
        # print(f"Connection failed: {e}")
    finally:
        # Ensure the socket is closed whether connection succeeded or failed
        if sock:
            sock.close()

# --- Main Execution Logic ---
# Disclaimer message displayed before starting the test
print("\n--- Ethical Hacking Tool for DHeat DOS Attack POC ---")
print("This script is for authorized testing ONLY. Ensure you have explicit permission.")
print("----------------------------\n")

print(f"Attempting to establish {NUM_CONNECTIONS} connections to {TARGET_HOST}:{TARGET_PORT}...")

threads = [] # List to hold all thread objects
start_time = time.time() # Record the start time of the test

# Create and start multiple threads to initiate connections concurrently
for _ in range(NUM_CONNECTIONS):
    thread = threading.Thread(target=connect_ssh) # Create a new thread for each connection attempt
    threads.append(thread) # Add the thread to our list
    thread.start() # Start the thread (it will call connect_ssh())

    # Optional: Add a small delay between starting threads.
    # This can sometimes make the test more realistic if your client machine
    # has limitations on how quickly it can spawn new network connections.
    # time.sleep(0.01)

# Wait for all threads to complete their execution
for thread in threads:
    thread.join() # Blocks until the thread terminates

end_time = time.time() # Record the end time of the test
duration = end_time - start_time # Calculate the total duration

# Calculate the connection rate
total_attempts = successful_connections + failed_connections
rate = total_attempts / duration if duration > 0 else 0 # Avoid division by zero

# --- Display Test Results ---
print(f"\n--- Test Results ---")
print(f"Target: {TARGET_HOST}:{TARGET_PORT}")
print(f"Total connection attempts: {total_attempts}")
print(f"Successful connections: {successful_connections}")
print(f"Failed connections: {failed_connections}")
print(f"Total duration: {duration:.3f} seconds")
print(f"Connection rate: {rate:.2f} connections/sec")

# --- Interpret Results based on ssh-audit guidance ---
if rate > 20.0:
    print("\nWarning: Connection rate is still high (greater than 20.0 conns/sec). "
          "Potentially vulnerable to DHEat DoS.")
    print("Remember: If 'PerSourceMaxStartups 1' is set on the server, this might be a false positive,")
    print("as the server is protected from a single source, even if it can process many unique connections.")
else:
    print("\nGood: Connection rate is within acceptable limits (less than 20.0 conns/sec). "
          "Mitigation appears effective.")