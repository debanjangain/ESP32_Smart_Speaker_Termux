#include "esp32_music.h"
#include "network_config.c"
#include "esp_sr_wakenet.h"
#include "driver/i2s.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_wifi.h"

#include "websocket_client.h"   // from components/websocket_client
#include "audio_codec.h"        // from components/audio_codec

static const char *TAG = "ESP32_MUSIC";

// Global WakeNet handles
const esp_sr_wakenet_model_t *model;
model_iface_data_t *wakenet;

// =======================
// I2S Initialization
// =======================
void audio_codec_init() {
    // Mic (INMP441) - I2S RX
    i2s_config_t i2s_config_rx = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_I2S,
        .dma_buf_count = 4,
        .dma_buf_len = 1024,
        .use_apll = false,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1
    };

    i2s_pin_config_t pin_config_rx = {
        .bck_io_num = MIC_SCK,
        .ws_io_num = MIC_WS,
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num = MIC_SD
    };

    i2s_driver_install(I2S_NUM_0, &i2s_config_rx, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config_rx);

    // Amp (MAX98357A) - I2S TX
    i2s_config_t i2s_config_tx = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
        .sample_rate = 16000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
        .communication_format = I2S_COMM_FORMAT_I2S,
        .dma_buf_count = 4,
        .dma_buf_len = 1024,
        .use_apll = false,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1
    };

    i2s_pin_config_t pin_config_tx = {
        .bck_io_num = AMP_BCLK,
        .ws_io_num = AMP_LRC,
        .data_out_num = AMP_DIN,
        .data_in_num = I2S_PIN_NO_CHANGE
    };

    i2s_driver_install(I2S_NUM_1, &i2s_config_tx, 0, NULL);
    i2s_set_pin(I2S_NUM_1, &pin_config_tx);

    ESP_LOGI(TAG, "INMP441 mic + MAX98357A amp initialized.");
}

// =======================
// Task: Wake Word Detection
// =======================
void wake_word_task(void *param) {
    uint8_t buffer[1024];
    size_t bytes_read;

    while (true) {
        i2s_read(I2S_NUM_0, buffer, sizeof(buffer), &bytes_read, portMAX_DELAY);
        int detected = model->detect(wakenet, (int16_t *)buffer);
        if (detected) {
            ESP_LOGI(TAG, "Wake word 'Alexa' detected!");
            websocket_client_send("WAKE: Alexa", strlen("WAKE: Alexa"));
        }
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// =======================
// Task: Backend Streaming
// =======================
void streaming_task(void *param) {
    uint8_t buffer[1024];
    size_t bytes_read, bytes_written;

    while (true) {
        // Capture audio from mic and send upstream
        i2s_read(I2S_NUM_0, buffer, sizeof(buffer), &bytes_read, portMAX_DELAY);
        if (bytes_read > 0) {
            websocket_client_send(buffer, bytes_read);
        }

        // Receive audio from backend and play
        int recv_len = websocket_client_receive(buffer, sizeof(buffer));
        if (recv_len > 0) {
            i2s_write(I2S_NUM_1, buffer, recv_len, &bytes_written, portMAX_DELAY);
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

// =======================
// Main Application
// =======================
extern "C" void app_main(void) {
    // Initialize NVS (needed for Wi-Fi)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_LOGI(TAG, "Starting ESP32 Smart Speaker...");

    // Step 1: Connect to Wi-Fi
    ESP_LOGI(TAG, "Connecting to Wi-Fi SSID: %s", WIFI_SSID);
    wifi_init_sta(WIFI_SSID, WIFI_PASS);

    // Step 2: Initialize audio codec (mic + amp)
    audio_codec_init();

    // Step 3: Load WakeNet model (Alexa)
    model = esp_sr_wakenet_get_model("wn9");
    wakenet = model->create(model);
    ESP_LOGI(TAG, "WakeNet Alexa model initialized.");

    // Step 4: Connect to backend via WebSocket
    ESP_LOGI(TAG, "Connecting to backend server: %s", SERVER_URI);
    websocket_client_start(SERVER_URI);

    // Step 5: Create tasks
    xTaskCreatePinnedToCore(
    wake_word_task,
    "wake_word_task",
    CONFIG_WAKE_TASK_STACK,
    NULL,
    CONFIG_WAKE_TASK_PRIORITY,
    NULL,
    0);

    xTaskCreatePinnedToCore(
    streaming_task,
    "streaming_task",
    CONFIG_STREAM_TASK_STACK,
    NULL,
    CONFIG_STREAM_TASK_PRIORITY,
    NULL,
    1);
}
