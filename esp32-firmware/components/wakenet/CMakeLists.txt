idf_component_register()

foreach(model_file
    wn9_data
    wn9_index
    _MODEL_INFO_
)
    target_add_binary_data(
        ${COMPONENT_TARGET}
        "${model_file}"
        BINARY
    )
endforeach()
