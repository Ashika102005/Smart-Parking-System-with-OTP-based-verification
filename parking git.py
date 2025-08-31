import serial
import time
import random
import sys
from datetime import datetime
from twilio.rest import Client

# ===== Twilio Config =====
ACCOUNT_SID = "*****"
AUTH_TOKEN = "*****"
TWILIO_PHONE = "+13**********"   # your Twilio trial number

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# ===== Serial Config =====
PORT = "COM3"   # change to match your Arduino port
BAUD = 9600
OTP_LENGTH = 6

# Track active OTPs
active_otps = {}
car_id_counter = 1

# ===== Helpers =====
def generate_otp(n=OTP_LENGTH):
    return ''.join(str(random.randint(0, 9)) for _ in range(n))

def send_sms(name, phone, otp, entry_time, car_id):
    message = f"""
Hello {name},
Your OTP for Smart Parking is: {otp}
Car ID: {car_id}
Entry Time: {entry_time}
"""
    client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=phone
    )
    print(f"[INFO] OTP sent to {phone}")

def read_line(ser, timeout=None):
    buf = bytearray()
    start = time.time()
    while True:
        if ser.in_waiting:
            ch = ser.read(1)
            if ch == b'\n':
                return buf.decode(errors='ignore').strip()
            elif ch == b'\r':
                continue
            else:
                buf += ch
        else:
            if timeout and (time.time() - start) > timeout:
                return None
            time.sleep(0.01)

# ===== Main Flow =====
def main():
    global car_id_counter
    print(f"Opening serial {PORT} @ {BAUD} …")
    try:
        ser = serial.Serial(PORT, BAUD, timeout=0)
    except Exception as e:
        print("Error opening serial:", e)
        sys.exit(1)

    time.sleep(2)
    print("Ready. Waiting for Arduino events…")

    while True:
        line = read_line(ser, timeout=0.1)
        if not line:
            continue

        # ===== ENTRY FLOW =====
        if line == "car_entry_request":
            car_id = f"car{car_id_counter}"
            car_id_counter += 1
            print(f"\n[ENTRY] {car_id} detected.")

            name = input("Enter driver's name: ").strip()
            phone = input("Enter phone number (+E.164 format, e.g., +1234567890): ").strip()
            otp = generate_otp()
            entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            active_otps[car_id] = {
                "otp": otp,
                "name": name,
                "phone": phone,
                "entry_time": entry_time
            }

            try:
                send_sms(name, phone, otp, entry_time, car_id)
                ser.write(b"open_entry_gate\n")
                print(f"[INFO] {car_id} assigned to {name}. Entry gate opened.")
            except Exception as e:
                print("[ERROR] Failed to send SMS:", e)
                ser.write(b"deny\n")

        # ===== EXIT FLOW =====
        elif line == "car_exit_request":
            print("\n[EXIT] Exit requested.")
            if not active_otps:
                print("[WARN] No active OTPs. Denying exit.")
                ser.write(b"deny\n")
                continue

            entered = input("Enter OTP to exit: ").strip()
            matched_car = None

            for car_id, details in active_otps.items():
                if entered == details["otp"]:
                    matched_car = car_id
                    break

            if matched_car:
                details = active_otps[matched_car]
                exit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                print(f"\n[OK] OTP verified for {matched_car}.")
                print(f"Name: {details['name']}")
                print(f"Phone: {details['phone']}")
                print(f"Entry Time: {details['entry_time']}")
                print(f"Exit Time: {exit_time}")
                print("-----------------------------")

                ser.write(b"open_exit_gate\n")
                del active_otps[matched_car]
            else:
                print("[DENY] Incorrect OTP. Exit denied.")
                ser.write(b"deny\n")

if __name__ == "__main__":
    main()
