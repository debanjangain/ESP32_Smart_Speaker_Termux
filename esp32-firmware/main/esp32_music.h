#pragma once

#include "driver/gpio.h"

// =======================
// Wi-Fi + Backend Config
// =======================
// Values supplied by menuconfig
#define WIFI_SSID      CONFIG_WIFI_SSID
#define WIFI_PASS      CONFIG_WIFI_PASS
#define SERVER_URI     CONFIG_SERVER_URI

// =======================
// INMP441 I2S Microphone
// =======================
// VDD -> 3.3V
// GND -> GND
// L/R -> GND

#define MIC_SD         GPIO_NUM_8
#define MIC_WS         GPIO_NUM_46
#define MIC_SCK        GPIO_NUM_9

// =======================
// MAX98357A I2S Amplifier
// =======================
// VIN  -> 5V
// GND  -> GND
// GAIN -> GND

#define AMP_DIN        GPIO_NUM_3
#define AMP_LRC        GPIO_NUM_10
#define AMP_BCLK       GPIO_NUM_11

// =======================
// Task Configuration
// =======================

#define CONFIG_WAKE_TASK_STACK      8192
#define CONFIG_STREAM_TASK_STACK    6144

#define CONFIG_WAKE_TASK_PRIORITY   5
#define CONFIG_STREAM_TASK_PRIORITY 4
