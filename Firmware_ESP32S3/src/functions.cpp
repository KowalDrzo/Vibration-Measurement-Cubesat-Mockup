#include "functions.h"

Globals glob;

/*************************************************************************************************/

void measureData() {

    adc1_config_width(ADC_WIDTH_BIT_12);
    adc1_config_channel_atten(ADC_X_CHANNEL, ADC_ATTEN_DB_12);
    adc1_config_channel_atten(ADC_Y_CHANNEL, ADC_ATTEN_DB_12);
    adc1_config_channel_atten(ADC_Z_CHANNEL, ADC_ATTEN_DB_12);

    Frame frame;
    uint32_t timer2;

    while(1) {

        // Measure data:
        for (uint16_t i = 0; i < DATA_IN_FRAME; i++) {

            timer2 = micros();

            frame.adcX[i] = adc1_get_raw(ADC_X_CHANNEL) >> 4;
            frame.adcY[i] = adc1_get_raw(ADC_Y_CHANNEL) >> 4;
            frame.adcZ[i] = adc1_get_raw(ADC_Z_CHANNEL) >> 4;

            while (micros() - timer2 < 100);
        }

        // Send the data (no que seems faster):
        digitalWrite(LED_PIN, 0);
        Serial.write((uint8_t*) &frame, sizeof(frame));
        digitalWrite(LED_PIN, 1);

        vTaskDelay(1);
    }
}

/*************************************************************************************************/

void blinkNTimes(uint8_t n) {

    for (uint8_t i = 0; i < n; i++) {

        digitalWrite(LED_PIN, 0);
        vTaskDelay(100);
        digitalWrite(LED_PIN, 1);
        vTaskDelay(200);
    }
}