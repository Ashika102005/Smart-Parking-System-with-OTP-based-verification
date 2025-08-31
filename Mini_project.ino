#include <Servo.h>
#include <LiquidCrystal.h>

// LCD pin configuration: (RS, E, D4, D5, D6, D7)
LiquidCrystal lcd(12, 13, 5, 4, 3, 2);

Servo gateServo;
#define servoPin 9
#define irEntryPin A0       // IR sensor for entry
#define exitButtonPin 7     // Push button for exit

void setup() {
  Serial.begin(9600);
  gateServo.attach(servoPin);
  gateServo.write(0); // Gate closed initially

  pinMode(irEntryPin, INPUT);
  pinMode(exitButtonPin, INPUT_PULLUP);

  lcd.begin(16, 2);
  lcd.setCursor(0,0);
  lcd.print(" Smart Parking ");
  lcd.setCursor(0,1);
  lcd.print("   System   ");
  delay(2000);
  showIdle();
}

void loop() {
  // ===== ENTRY FLOW =====
  if (digitalRead(irEntryPin) == LOW) {
    Serial.println("car_entry_request");
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Car Detected");
    lcd.setCursor(0,1);
    lcd.print("Check SMS OTP");
    delay(3000);
    showIdle();
  }

  // ===== EXIT FLOW =====
  if (digitalRead(exitButtonPin) == LOW) {
    Serial.println("car_exit_request");
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Exit Requested");
    lcd.setCursor(0,1);
    lcd.print("Enter OTP");
    delay(2000);
    showIdle();
  }

  // ===== Listen for Python commands =====
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "open_entry_gate") {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("OTP Verified");
      lcd.setCursor(0,1);
      lcd.print("Gate Opening");
      gateServo.write(90);
      delay(2000);
      gateServo.write(0);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Gate Closed");
      delay(2000);
      showIdle();
    }
    else if (cmd == "open_exit_gate") {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Exit Granted");
      lcd.setCursor(0,1);
      lcd.print("Gate Opening");
      gateServo.write(90);
      delay(2000);
      gateServo.write(0);
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Gate Closed");
      delay(2000);
      showIdle();
    }
    else if (cmd == "deny") {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Access Denied");
      lcd.setCursor(0,1);
      lcd.print("Try Again");
      delay(2000);
      showIdle();
    }
  }
}

// ===== Idle Screen Function =====
void showIdle() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Waiting Cars..");
}
