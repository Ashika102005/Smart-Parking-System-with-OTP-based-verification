# Smart-Parking-System-with-OTP-based-verification
This project presents the design and implementation of a smart parking system with OTP-based vehicle access control to enhance security, reliability, and efficiency in parking management.

# Overview

Traditional parking systems rely on manual verification or simple barriers, which are prone to:
Human error
Unauthorized access
Poor traffic handling
To overcome these challenges, this system integrates Arduino hardware, Python programming, and Twilio SMS services to create an automated, low-cost, and intelligent solution.

# Working

# Entry Gate:
IR sensor detects approaching vehicle.
Driver provides name + mobile number.
System generates a unique 6-digit OTP and sends via SMS (Twilio).
Entry gate opens immediately (servo + LCD feedback).

# Exit Gate:
Driver presses a push button.
System requests OTP received at entry.
If OTP matches → gate opens; otherwise → access denied.

# Key Features

Dual-layered authentication (prevents misuse/unauthorized exit)
Automated gate control (servo motor + LCD feedback)
Real-time OTP delivery using Twilio SMS
Smooth traffic handling with minimal human intervention

# Applications

Parking lots
Residential complexes
Office premises
Scalable for smart cities (future upgrades: mobile app, automated billing, cloud monitoring)
