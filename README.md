# D(H)eat DoS Attack POC (CVE-2002-20001)
POC for Testing the Existence of D(HE)at DOS Attack for (CVE-2002-20001)


# Usage
command: python3 dheat_dos_attack_poc.py <IP_Address> <Port_Number>

<IP_Address>: Replace with the actual IP address or hostname of the SSH server you have permission to test.

<Port_Number>: Target Port number running SSH services.

Steps to execute:
To install Python 3 on Ubuntu, Kali, etc the basic command is:

$ sudo apt update

$ sudo apt install python3

Download & Changing file Permission:

$ git clone https://github.com/itmaniac/dheat_dos_attack_poc.git

$ cd dheat_dos_attack_poc

$ chmod +x dheat_dos_attack_poc.py

D(HE)at DOS Attack POC Test:

$ python3 dheat_dos_attack_poc.py 22 10.0.0.1

# Successful Execution Results:
Attempting to establish 50 connections to 10.0.0.1:22...

--- Test Results ---

Target: 10.0.0.1:22

Total connection attempts: 50

Successful connections: 50

Failed connections: 0

Total duration: 0.025 seconds

Connection rate: 1981.66 connections/sec

Warning: Connection rate is still high (greater than 20.0 conns/sec). Potentially vulnerable to DHEat DoS.
Remember: If 'PerSourceMaxStartups 1' is set on the server, this might be a false positive,
as the server is protected from a single source, even if it can process many unique connections.


# VirusTotal Scan Results:
<img width="1589" height="242" alt="image" src="https://github.com/user-attachments/assets/92c61c27-b21d-4f91-bb90-9bedeef7f49c" />


# DISCLAIMER:
This script is provided for EDUCATIONAL and LEGAL PENETRATION TESTING PURPOSES ONLY. The author does not condone or support any illegal or unauthorized use of this tool.

USAGE CONDITIONS:

You must have EXPLICIT WRITTEN PERMISSION from the system owner before testing any SSH service
Use only on systems you own or are legally authorized to test
Comply with all applicable local, national, and international laws
Never use this tool against production systems without proper authorization
Any credentials used must be test accounts or dummy credentials
By using this script, you agree that:

You are solely responsible for any consequences of its use
The author bears no liability for misuse or damages
You will not use this tool for any malicious purposes
This tool simulates brute-force attempts and may trigger security alerts or account lockouts. Use with caution and proper authorization at all times.


# Acknowledgements / References

This Proof-of-Concept (PoC) script for the D(HE)at Denial-of-Service (DoS) vulnerability (CVE-2002-20001) was inspired by the excellent research conducted by Szilárd Pfeiffer. His detailed work on this vulnerability can be found at: https://dheatattack.com/

While this script is an independent implementation for educational and testing purposes, it directly addresses the attack vector identified and documented by their valuable contributions to the cybersecurity community.

