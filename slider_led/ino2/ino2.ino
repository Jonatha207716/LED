// 4 LEDs con sliders (0-255) por Serial
// Comandos: LED1:0-255, LED2:0-255, LED3:0-255, LED4:0-255

const byte NLEDS = 4;
const byte LED_PINS[NLEDS] = {3, 5, 6, 9};  // PWM UNO/Nano
char buf[40];

void setup() {
  Serial.begin(9600);
  Serial.setTimeout(25);

  for (byte i = 0; i < NLEDS; i++) {
    pinMode(LED_PINS[i], OUTPUT);
    analogWrite(LED_PINS[i], 0);
  }

  Serial.println("OK:READY");
}

void loop() {
  if (!Serial.available()) return;

  int n = Serial.readBytesUntil('\n', buf, sizeof(buf) - 1);
  buf[n] = '\0';

  while (n > 0 && (buf[n-1] == '\r' || buf[n-1] == ' ' || buf[n-1] == '\t')) {
    buf[n-1] = '\0';
    n--;
  }

  if (strncmp(buf, "LED", 3) == 0) {
    int idx = buf[3] - '1';      // '1'..'4' -> 0..3
    char *p = strchr(buf, ':');  // busca ':'

    if (idx >= 0 && idx < NLEDS && p) {
      int val = atoi(p + 1);
      if (val < 0) val = 0;
      if (val > 255) val = 255;

      analogWrite(LED_PINS[idx], val);

      Serial.print("OK:LED");
      Serial.print(idx + 1);
      Serial.print(":");
      Serial.println(val);
      return;
    }
  }

  Serial.println("ERR:CMD");
}
