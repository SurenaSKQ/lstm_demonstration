import os

def split_into_chunks(args):
    chunk_size = args.chunk_size # lines

    def write_chunk(part, lines):
        with open('./data/data_part_'+ str(part) +'.csv', 'w') as f_out:
            f_out.write(header)
            f_out.writelines(lines)

    with open(args.source, 'r') as f:
        count = 0
        header = f.readline()
        lines = []
        for line in f:
            count += 1
            lines.append(line)
            if count % chunk_size == 0:
                write_chunk(count // chunk_size, lines)
                lines = []
        # write remainder
        if len(lines) > 0:
            write_chunk((count // chunk_size) + 1, lines)

def clean_data_dir():
    # Clean the data directory before splitting again
    for filename in os.listdir("./data/"):
        file_path = os.path.join("./data/", filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def check_flag(args):
    if args.no_create_chunks:
        return True
    if (not os.path.isfile("checkfile") or args.no_prepared_data or args.no_create_chunks):
        return False
    else:
        with open("checkfile", 'r') as file:
            size = str(args.chunk_size)
            if (file.readline() == size):
                file.close()
                return True
            else:
                file.close
                return False

def write_flag(args):
    with open("checkfile", 'w') as file:
        file.write(str(args.chunk_size))
        file.close()