#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "FS.h"
#include <LittleFS.h>
#include "driver/adc.h"
#include "esp_adc_cal.h"

#include "pinout.h"
#include "dataStructs.h"

void measureData();
void blinkNTimes(uint8_t n);

#endif
