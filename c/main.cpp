// change this to the GPIO that your board maps to D3
const int PIN_BUZZER = 27/* e.g. 27 */;

void setup() {
  ledcAttachPin(PIN_BUZZER, 0);      // channel 0
  ledcWriteTone(0, 1000);            // 1 kHz
  delay(500);
  ledcWriteTone(0, 0);               // stop
}

void loop() {}