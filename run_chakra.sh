# <---------------------------------------------------------- CALL 3: CHAKRA -------------------------------------------------------->

# Construct the input filename
# INPUT_XML_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}.xml"
# OUTPUT_ET_FILENAME="gpu_${DIM}_link_${LINK}_bw_${BW}_chunk_${CHUNK}_chunk_coll_${CHUNK_PER_COLL}"

# # Call the et_converter.py with the dynamically constructed filenames
# python3 -m et_converter.et_converter --input_type msccl \
# --input_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.xml \
# --output_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2 --num_dims 2

# python -m et_visualizer.et_visualizer\
#     --input_filename  /home/karthike4/Desktop/apex/APEX_HML_Project/gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.et \
#     --output_filename gpu_2_link_500_bw_50_chunk_1024_chunk_coll_2.1.pdf