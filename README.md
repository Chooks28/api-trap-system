# Activating Attack Traps for Suspicious IPs

A deception-based REST API security system that detects abnormal IP behavior and redirects suspicious clients to decoy APIs for monitoring.

## Features
- Behavioral IP detection
- Decoy endpoints with fake data
- Trap activity logging
- Real-time dashboard
- Reset & Export trap logs

## Requirements
- Python 3
- Flask

## Setup
```bash
git clone https://github.com/your-username/api-trap-system.git
cd api-trap-system
python3 -m venv venv
source venv/bin/activate
pip install flask

## Terminal 1 (Real API)
- python3 main_server.py

## Terminal 2 (Trap + Dashboard)
- python3 trap_server.py

## Usage
- Visit http://localhost:5000/api/data (real API)
- After 6 rapid requests, you'll be redirected to http://localhost:5001/trap
- View http://localhost:5001/dashboard to monitor attacker IPs
- Use buttons to reset or export logs
