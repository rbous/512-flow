def reconstruct_file(chunk_ids, output_file):
    with open(output_file, 'wb') as f_out:
        for chunk_id in chunk_ids:
            with open(f'chunk_{chunk_id}.part', 'rb') as f_in:
                f_out.write(f_in.read())
    print(f"File {output_file} reconstructed successfully.")