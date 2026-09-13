# Minimum required CMake version
cmake_minimum_required(VERSION 3.5)

# Set project name
set(PROJECT_NAME "esp32_music")

# Include ESP-IDF build system
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

# Register main source files
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

# Define project
project(${PROJECT_NAME})
