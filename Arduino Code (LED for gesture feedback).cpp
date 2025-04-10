char command;

void setup() {
  Serial.begin(9600);
  pinMode(8, OUTPUT); // Use pin 8 for LED or relay
  digitalWrite(8, LOW);
}

void loop() {
  if (Serial.available()) {
    command = Serial.read();

    if (command == 'P') {
      // Play/Pause feedback
      digitalWrite(8, HIGH);
      delay(500);
      digitalWrite(8, LOW);
      Serial.println("Play/Pause triggered");
    }

    else if (command == 'N') {
      // Next Track feedback
      for (int i = 0; i < 3; i++) {
        digitalWrite(8, HIGH);
        delay(100);
        digitalWrite(8, LOW);
        delay(100);
      }
      Serial.println("Next Track triggered");
    }
  }
}
