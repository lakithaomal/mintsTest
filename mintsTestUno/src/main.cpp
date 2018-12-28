#include <Arduino.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  delay(1000);
  Serial.print("#mintsO!HTU21D>21.9:28.9-");
  delay(1000);
  Serial.print("#mintsO!BMP280>1000.5:22.9-");
  delay(1000);
  Serial.print("#mintsO!GAS1>21.9:28.9:45.9:78.89-");

}
