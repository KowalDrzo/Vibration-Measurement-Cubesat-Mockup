#include "functions.h"

void setup() {

    Serial.begin();
    Serial.setTimeout(10);
    vTaskDelay(1000);

    pinMode(LED_PIN, OUTPUT);
    blinkNTimes(3);

    while (!Serial) {
        vTaskDelay(500);
    }

    // RTOS ques and tasks:
    xTaskCreate((TaskFunction_t) measureData, "Measure Data Task",  65536, NULL, 20, NULL);
}

void loop() {
    vTaskDelay(10);
}
