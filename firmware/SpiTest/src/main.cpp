#include <Arduino.h>
#include "LS7366R.hpp"

const uint8_t SPI_MISO = 50;
const uint8_t SPI_MOSI = 51;
const uint8_t SPI_SCK = 52;
const uint8_t SPI_SS = 53;

LS7366R LeftEncoder = LS7366R(SPI_SS);

void setup() {
  pinMode(SPI_MISO, INPUT);
  pinMode(SPI_MOSI, OUTPUT);
  pinMode(SPI_SCK, OUTPUT);
  pinMode(SPI_SS, OUTPUT);

  Serial.begin(115200);

  LeftEncoder.Initialize();
}

void loop() {
  Serial.println(LeftEncoder.Read());
  delay(250);
}
