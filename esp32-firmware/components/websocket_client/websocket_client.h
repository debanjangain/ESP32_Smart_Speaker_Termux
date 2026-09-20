#pragma once

#include <stdint.h>
#include <stddef.h>

void websocket_client_start(const char *uri);

void websocket_client_send(
    const uint8_t *data,
    size_t len);

int websocket_client_receive(
    uint8_t *buffer,
    size_t max_len);
