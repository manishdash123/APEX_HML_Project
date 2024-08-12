#!/bin/bash

# Path to the base directory containing the subdirectories
BASE_DIR="Mesh2D"

# Path to the output directory
OUTPUT_DIR="ET"

# Iterate over each subdirectory in the base directory
for SUBDIR in "$BASE_DIR"/*/; do
    # Remove trailing slash from the subdirectory path
    SUBDIR=${SUBDIR%/}

    # Iterate over each XML file in the current subdirectory
    for INPUT_XML_FILE in "$SUBDIR"/*.xml; do
        # Extract the base filename without the extension
        BASE_FILENAME=$(basename "$INPUT_XML_FILE" .xml)

        # Construct the input and output filenames
        INPUT_XML_FILENAME="$BASE_FILENAME.xml"
        OUTPUT_ET_FILENAME="$OUTPUT_DIR/$BASE_FILENAME"

        # Call the et_converter.py with the dynamically constructed filenames
        python3 -m chakra.et_converter.et_converter \
          --input_type msccl \
          --input_filename "$INPUT_XML_FILE" \
          --output_filename "$OUTPUT_ET_FILENAME" \
          --num_dims 2

        echo "Processed $INPUT_XML_FILE -> $OUTPUT_ET_FILENAME"
    done
done
