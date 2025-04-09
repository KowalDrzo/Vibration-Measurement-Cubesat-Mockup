#ifndef DATA_STRUCTS_H
#define DATA_STRUCTS_H

#include <stdint.h>

struct Globals {

    QueueHandle_t dataFramesFifo;
};

#define DATA_IN_FRAME 10000


struct Frame {

    uint8_t adcX[DATA_IN_FRAME];
    uint8_t adcY[DATA_IN_FRAME];
    uint8_t adcZ[DATA_IN_FRAME];
};

extern Globals glob;

#endif
