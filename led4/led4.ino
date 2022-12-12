#define led 3
void setup() {
  pinMode(led, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while (Serial.available() > 0){
    int value = Serial.read();
    if (value == '0'){
      digitalWrite(led, LOW);
    }
    else if (value == '1'){
      digitalWrite(led, HIGH);
    }
  }
}
