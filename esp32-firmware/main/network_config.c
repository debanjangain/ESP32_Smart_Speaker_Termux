#include "esp32_music.h"

#include <string.h>

#include "esp_wifi.h"
#include "esp_log.h"
#include "esp_event.h"
#include "esp_netif.h"

#include "freertos/FreeRTOS.h"
#include "freertos/event_groups.h"

static const char *TAG = "NETWORK";

// Event group to signal when connected
static EventGroupHandle_t wifi_event_group;

#define WIFI_CONNECTED_BIT BIT0

// =======================
// Wi-Fi Event Handler
// =======================
static void wifi_event_handler(
    void *arg,
    esp_event_base_t event_base,
    int32_t event_id,
    void *event_data)
{
    if (event_base == WIFI_EVENT &&
        event_id == WIFI_EVENT_STA_START)
    {
        ESP_LOGI(TAG, "Connecting to Wi-Fi...");
        esp_wifi_connect();
    }
    else if (event_base == WIFI_EVENT &&
             event_id == WIFI_EVENT_STA_DISCONNECTED)
    {
        ESP_LOGW(TAG, "Wi-Fi disconnected, retrying...");
        esp_wifi_connect();
    }
    else if (event_base == IP_EVENT &&
             event_id == IP_EVENT_STA_GOT_IP)
    {
        ip_event_got_ip_t *event =
            (ip_event_got_ip_t *)event_data;

        ESP_LOGI(
            TAG,
            "Got IP: %s",
            ip4addr_ntoa(&event->ip_info.ip));

        xEventGroupSetBits(
            wifi_event_group,
            WIFI_CONNECTED_BIT);
    }
}

// =======================
// Wi-Fi Init
// =======================
void wifi_init_sta(
    const char *ssid,
    const char *pass)
{
    wifi_event_group = xEventGroupCreate();

    if (wifi_event_group == NULL)
    {
        ESP_LOGE(
            TAG,
            "Failed to create event group");
        return;
    }

    ESP_ERROR_CHECK(
        esp_netif_init());

    ESP_ERROR_CHECK(
        esp_event_loop_create_default());

    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg =
        WIFI_INIT_CONFIG_DEFAULT();

    ESP_ERROR_CHECK(
        esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;

    ESP_ERROR_CHECK(
        esp_event_handler_instance_register(
            WIFI_EVENT,
            ESP_EVENT_ANY_ID,
            &wifi_event_handler,
            NULL,
            &instance_any_id));

    ESP_ERROR_CHECK(
        esp_event_handler_instance_register(
            IP_EVENT,
            IP_EVENT_STA_GOT_IP,
            &wifi_event_handler,
            NULL,
            &instance_got_ip));

    wifi_config_t wifi_config = {0};

    strlcpy(
        (char *)wifi_config.sta.ssid,
        ssid,
        sizeof(wifi_config.sta.ssid));

    strlcpy(
        (char *)wifi_config.sta.password,
        pass,
        sizeof(wifi_config.sta.password));

    ESP_ERROR_CHECK(
        esp_wifi_set_mode(WIFI_MODE_STA));

    ESP_ERROR_CHECK(
        esp_wifi_set_config(
            WIFI_IF_STA,
            &wifi_config));

    ESP_ERROR_CHECK(
        esp_wifi_start());

    ESP_LOGI(
        TAG,
        "Wi-Fi initialization complete");
}

// =======================
// Wait Until Connected
// =======================
void wifi_wait_connected(void)
{
    xEventGroupWaitBits(
        wifi_event_group,
        WIFI_CONNECTED_BIT,
        pdFALSE,
        pdTRUE,
        portMAX_DELAY);

    ESP_LOGI(
        TAG,
        "Wi-Fi connected");
}
