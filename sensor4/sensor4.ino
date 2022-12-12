#define sensor_pin A0

long interval = 1000;
long prev;

void setup() {
  pinMode(sensor_pin, INPUT);
  Serial.begin(9600);
  prev = millis();
}

void loop() {
  if (Serial.available() >= 2){
    if (Serial.read() == 'I'){
      interval = long(Serial.read());
    }
  }
  if (millis() - prev >= interval){
    char value = analogRead(sensor_pin) / 1024.0 * 101;
    Serial.write(value);
    prev = millis();
  }
}
