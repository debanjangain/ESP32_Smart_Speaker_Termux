#include "websocket_client.h"
#include "esp_websocket_client.h"
#include "esp_log.h"

static const char *TAG = "WS_CLIENT";
static esp_websocket_client_handle_t client;

// =======================
// Start WebSocket Client
// =======================
void websocket_client_start(const char* uri) {
    esp_websocket_client_config_t websocket_cfg = {
        .uri = uri,
    };

    client = esp_websocket_client_init(&websocket_cfg);
    esp_websocket_client_start(client);

    ESP_LOGI(TAG, "WebSocket client started, URI: %s", uri);
}

// =======================
// Send Data
// =======================
void websocket_client_send(
    const uint8_t *data,
    size_t len)
{
    if (client == NULL)
    {
        return;
    }

    if (esp_websocket_client_is_connected(client))
    {
        esp_websocket_client_send_bin(
            client,
            (const char *)data,
            len,
            portMAX_DELAY);
    }
}


// =======================
// Receive Data
// =======================
int websocket_client_receive(uint8_t* buffer, size_t max_len) {
    if (esp_websocket_client_is_connected(client)) {
        int len = esp_websocket_client_recv_bin(client, (char*)buffer, max_len, portMAX_DELAY);
        return len;
    }
    return 0;
}
