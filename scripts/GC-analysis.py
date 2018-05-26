import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument("input_file", type=str, help="Name of the input file in FASTA format")
parser.add_argument("-o", "--output_file", type=str, help="Name of the output file")
parser.add_argument("window_size", type=int, help="Number of base pairs where the GC percentage is calculated for")
parser.add_argument("shift", type=int, help="The shift increment")
parser.add_argument("-ot", "--omit_tail", action="store_true", help="True: if the trailing sequence should be omitted. "
                                                                    "Default behaviour is to retain the leftover"
                                                                    "sequence.")
parser.add_argument("-f", "--output_format", type=str, choices=["wig", "wiggle", "bigwig", "bw", "gzip"])
args = parser.parse_args()


def percentage(byte):
    if byte in ['G', 'C']:
        return percentage_bp
    return 0


def generate_wiggle(input_file, output_file, window_size, shift):
    """"""
    basepair_location = 1
    counter = 0
    total_percent = 0
    global percentage_bp
    percentage_bp = 1 / window_size * 100

    if output_file:
        result = open(output_file, "w+")
    else:
        result = open(input_file.split(".")[0] + ".wig", "w+")

    with open(input_file, "rb") as f:
        # read track line
        title = f.readline().decode('utf-8')
        result.write(title)
        # add step info
        result.write("variableStep span=" + str(window_size) + "\n")
        while True:
            # read file one bp at a time
            a = f.read(1).decode('utf-8')
            # if not EOF and not newline
            if a != "" and a != "\n":
                counter += 1
                total_percent += percentage(a)
                # if reached window size, write percentage
                if counter == window_size:
                    result.write(str(basepair_location) + "  " + str(int(total_percent)) + "\n")
                    basepair_location = basepair_location + shift
                    f.seek(-(window_size - shift), 1)
                    counter = 0
                    total_percent = 0
            elif a == '':
                # if end of file and still bp remains
                if counter != 0:
                    result.write(str(basepair_location) + "  " + str(int(total_percent * window_size / counter)) + "\n")
                    basepair_location += shift
                    break
                else:
                    break
    result.close()


generate_wiggle(args.input_file, args.output_file, args.window_size, args.shift)
