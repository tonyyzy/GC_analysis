import argparse as ap
import os


def get_args():
    parser = ap.ArgumentParser()
    parser.add_argument("input_file", type=str, help="Name of the input file in FASTA format")
    parser.add_argument("-o", "--output_file", type=str, help="Name of the output file")
    parser.add_argument("window_size", type=int, help="Number of base pairs where the GC percentage is calculated for")
    parser.add_argument("shift", type=int, help="The shift increment")
    parser.add_argument("-ot", "--omit_tail", action="store_true", help="True: if the trailing sequence should be "
                                                                        "omitted. Default behaviour is to retain "
                                                                        "the leftover sequence.")
    parser.add_argument("-f", "--output_format", type=str, choices=["wig", "wiggle", "bigwig", "bw", "gzip"])
    args = parser.parse_args()

    return args.input_file, args.output_file, args.window_size, args.shift


def generate_wiggle(input_file, output_file, window_size, shift):
    """"""
    basepair_location = 1
    counter = 0
    total_percent = 0
    percentage_bp = 1 / window_size * 100

    def percentage(byte):
        if byte in ['G', 'C']:
            return percentage_bp
        return 0

    def open_results_file(input_file_name, output_file_name):
        head, tail = os.path.split(input_file_name)
        if output_file_name:
            file = open(os.path.join(head, output_file_name), "w+")
        else:
            wig_filename = tail.split(".")[0] + ".wig"
            file = open(os.path.join(head, wig_filename), "w+")
        return file

    with open(input_file, "rb") as genome:
        result = open_results_file(input_file, output_file)
        # read track line
        title = genome.readline().decode('utf-8')
        result.write(title)
        # add step info
        result.write("variableStep span=" + str(window_size) + "\n")
        while True:
            # read file one bp at a time
            base = genome.read(1).decode('utf-8')
            # if not EOF and not newline
            if base != "" and base != "\n":
                counter += 1
                total_percent += percentage(base)
                # if reached window size, write percentage
                if counter == window_size:
                    result.write(str(basepair_location) + "  " + str(int(total_percent)) + "\n")
                    basepair_location = basepair_location + shift
                    genome.seek(-(window_size - shift), 1)
                    counter = 0
                    total_percent = 0
            elif base == '':
                # if end of file and still bp remains
                if counter != 0:
                    result.write(str(basepair_location) + "  " + str(int(total_percent * window_size / counter)) + "\n")
                    basepair_location += shift
                    break
                else:
                    break
    result.close()


generate_wiggle(*get_args()[:])
