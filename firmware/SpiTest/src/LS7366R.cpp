// Copyright 2016 Joseph Riesen

#include "LS7366R.hpp"

// Datasheet: http://cdn.usdigital.com/assets/general/LS7366R.pdf

LS7366R::LS7366R(uint8_t slaveSelectPin, CounterMode mode,
                 float multiplier, uint32_t range, bool reverse) :
                 ss(slaveSelectPin), mode(mode),
                 multiplier(multiplier), range(range), reverse(reverse) {
  digitalWrite(ss, HIGH);
  pinMode(ss, OUTPUT);
}

void LS7366R::Initialize() {
  SPI.beginTransaction(spiSettings);
  digitalWrite(ss, LOW);
  // Write to MDR0
  SPI.transfer(0b10001000);

  // Quadrature 1x, free-running count, index resets CNTR, asynchronous index
  // SPI.transfer(0b00100001);
  // Quadrature 1x, free-running count, index ignored, asynchronous index
  SPI.transfer(0b00000001);

  digitalWrite(ss, HIGH);
  delayMicroseconds(1);

  digitalWrite(ss, LOW);
  // Write to MDR1
  SPI.transfer(0b10010000);
  // Bits 4-7 are not implemented at present:
  SPI.transfer(mode);
  digitalWrite(ss, HIGH);
  delayMicroseconds(1);
  SPI.endTransaction();
}

// Given that the Arduino is a 16-bit platform, it's not so great in terms of
// performance to return a double-word, but it does cover all cases.
int32_t LS7366R::Read() {
  if (mode == BITS_32) {
    return Format(Read32());
  } else if (mode == BITS_16) {
    return Format(Read16());
  }
  return 0;
}

// Multiplies value by the scaling multiplier then clamps it to the provided
// range (i.e. if range = 200, a value of -125 is converted to +75).  Does not
// clamp if range = 0.
int32_t LS7366R::Format(int32_t value) {
  value = round(multiplier * value);
  if (range <= 0) return value;

  // modulus is counterintuitive with negative numbers!
  if (value >= 0) {
    return value % range;
  } else {
    return range - (abs(value) % range);
  }
}

int16_t LS7366R::Read16() {
  int16_t retval = 0;

  SPI.beginTransaction(spiSettings);
  digitalWrite(ss, LOW);
  SPI.transfer(0x60);  // Request count
  retval += SPI.transfer(0x00);  // MSB
  retval <<= 8;
  retval += SPI.transfer(0x00);  // LSB
  digitalWrite(ss, HIGH);
  SPI.endTransaction();
  delayMicroseconds(1);

  return reverse ? -retval : retval;
}

int32_t LS7366R::Read32() {
  int32_t retval = 0;

  SPI.beginTransaction(spiSettings);
  digitalWrite(ss, LOW);
  SPI.transfer(0x60);  // Request count
  retval += SPI.transfer(0x00);  // MSB
  retval <<= 8;
  retval += SPI.transfer(0x00);
  retval <<= 8;
  retval += SPI.transfer(0x00);
  retval <<= 8;
  retval += SPI.transfer(0x00);  // LSB
  digitalWrite(ss, HIGH);
  SPI.endTransaction();
  delayMicroseconds(1);

  return reverse ? -retval : retval;
}

void LS7366R::Zero() {
  SPI.beginTransaction(spiSettings);
  digitalWrite(ss, LOW);
  // Write to DTR
  SPI.transfer(0x98);
  // Load data
  SPI.transfer(0x00);  // MSB
  SPI.transfer(0x00);
  SPI.transfer(0x00);
  SPI.transfer(0x00);  // LSB
  digitalWrite(ss, HIGH);

  delayMicroseconds(1);

  digitalWrite(ss, LOW);
  SPI.transfer(0xE0);  // Set current data register to "center"
  digitalWrite(ss, HIGH);
  SPI.endTransaction();

  delayMicroseconds(1);
}
