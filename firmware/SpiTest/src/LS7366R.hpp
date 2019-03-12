// Copyright 2016 Joseph Riesen

// Implements a SPI-accessible LS7366R quadrature encoder buffer.

#ifndef ls7366r_h
#define ls7366r_h

#include <Arduino.h>
#include <SPI.h>

class LS7366R {
 public:
  enum CounterMode {
    BITS_32 = 0,
    // BITS_24 = 1,
    BITS_16 = 2,
    // BITS_8 = 3,
  };

 private:
  uint8_t ss;
  CounterMode mode;
  float multiplier;
  uint32_t range;
  bool reverse;

  // Note that the datasheet shows a 240ns minimum period for SCLK, or 4.16MHz
  const SPISettings spiSettings { 4000000, MSBFIRST, SPI_MODE0 };
  int16_t Read16();
  int32_t Read32();
  int32_t Format(int32_t value);

 public:
  LS7366R(
    uint8_t slaveSelectPin,
    CounterMode mode = BITS_32,
    float multiplier = 1.0,
    uint32_t range = 0,
    bool reverse = false);
  void Initialize();
  void Zero();

  int32_t Read();
};
#endif
