#pragma once

#include <stdint.h>
#include <stddef.h>

// Initialize INMP441 microphone and MAX98357A amplifier
void audio_codec_init(void);

// Read audio from microphone
int audio_codec_read(
    uint8_t *buffer,
    size_t len);

// Write audio to speaker amplifier
int audio_codec_write(
    const uint8_t *buffer,
    size_t len);
