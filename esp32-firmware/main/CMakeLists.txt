idf_component_register(
    SRCS
        "esp32_music.cc"
        "network_config.c"

    INCLUDE_DIRS
        "."

    REQUIRES
        audio_codec
        websocket_client
        wakenet
)
