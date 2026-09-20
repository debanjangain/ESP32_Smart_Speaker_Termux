#include "audio_codec.h"
#include "esp32_music.h"
#include "driver/i2s.h"
#include "esp_log.h"

static const char *TAG = "AUDIO_CODEC";

void audio_codec_init(void) {
    // 🎤 INMP441 Mic (I2S RX)
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
        .bck_io_num = MIC_SCK,   // GPIO9
        .ws_io_num  = MIC_WS,    // GPIO46
        .data_out_num = I2S_PIN_NO_CHANGE,
        .data_in_num  = MIC_SD   // GPIO8
    };

    i2s_driver_install(I2S_NUM_0, &i2s_config_rx, 0, NULL);
    i2s_set_pin(I2S_NUM_0, &pin_config_rx);

    // 🔊 MAX98357A Amp (I2S TX)
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
        .bck_io_num = AMP_BCLK,  // GPIO11
        .ws_io_num  = AMP_LRC,   // GPIO10
        .data_out_num = AMP_DIN, // GPIO3
        .data_in_num  = I2S_PIN_NO_CHANGE
    };

    i2s_driver_install(I2S_NUM_1, &i2s_config_tx, 0, NULL);
    i2s_set_pin(I2S_NUM_1, &pin_config_tx);

    ESP_LOGI(TAG, "Audio codec initialized (INMP441 mic + MAX98357A amp).");
}

int audio_codec_read(uint8_t* buffer, size_t len) {
    size_t bytes_read;
    esp_err_t ret = i2s_read(I2S_NUM_0, buffer, len, &bytes_read, portMAX_DELAY);
    return (ret == ESP_OK) ? bytes_read : 0;
}

int audio_codec_write(const uint8_t* buffer, size_t len) {
    size_t bytes_written;
    esp_err_t ret = i2s_write(I2S_NUM_1, buffer, len, &bytes_written, portMAX_DELAY);
    return (ret == ESP_OK) ? bytes_written : 0;
}
