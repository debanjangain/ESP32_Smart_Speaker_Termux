#pragma once
#include <stdint.h>
#include <stddef.h>

// Initialize mic (INMP441) and amp (MAX98357A)
void audio_codec_init(void);

// Read audio samples from mic
int audio_codec_read(uint8_t* buffer, size_t len);

// Write audio samples to amp
int audio_codec_write(const uint8_t* buffer, size_t len);
