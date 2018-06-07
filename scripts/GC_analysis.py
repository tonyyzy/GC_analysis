"""
A command-line utility for calculating the GC percentage of an input genomic sequence.
"""

import argparse as ap
import os, sys


def get_args():
    """Helper function to handler all the command-line input options"""
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
    """Main function for generating the output file"""
    basepair_location = 1
    counter = 0
    total_percent = 0
    percentage_bp = (1.0 / window_size) * 100
    prev_bps = [""] * (window_size - shift)

    def percentage(byte):
        """Test the if the byte is G or C"""
        if byte in ["G", "C"]:
            return percentage_bp
        return 0

    def open_results_file(input_file_name, output_file_name):
        """A helper function to create the output file in the input file location"""
        head, tail = os.path.split(input_file_name)
        if output_file_name:
            file = open(os.path.join(head, output_file_name), "w+", newline="\n")
        else:
            file = sys.stdout
        return file

    with open(input_file, "r") as genome:
        result = open_results_file(input_file, output_file)
        # read track line
        title = genome.readline()
        if title[0] != ">":
            print("WARNING! The input file is not in fasta format.")
            raise SystemError(1)
        result.write(title.split(" ")[0] + "\n")
        # add step info
        result.write("variableStep span=" + str(window_size) + "\n")
        for i in range(window_size):
            base = genome.read(1)
            # print(base)
            # if not EOF and not newline
            if base != "" and base != "\n":
                counter += 1
                total_percent += percentage(base)
                # print(total_percent)
                # print(total_percent)
                if counter > shift:
                    prev_bps[counter - shift - 1] = base
                if counter == window_size:
                    result.write(str(basepair_location) + "  " + str(int(total_percent)) + "\n")
                    basepair_location = basepair_location + shift
                    counter = window_size - shift
                    total_percent = sum(percentage(x) for x in prev_bps)
        while True:
            # read file one bp at a time
            base = genome.read(1)
            # if not EOF and not newline
            if base not in ["", " ", "\n", "\r"]:
                counter += 1
                total_percent += percentage(base)
                # print(total_percent)
                if counter > shift:
                    prev_bps[counter - shift - 1] = base
                # if reached window size, write percentage
                if counter == window_size:
                    result.write(str(basepair_location) + "  " + str(int(total_percent)) + "\n")
                    basepair_location = basepair_location + shift
                    # genome.seek(-(window_size - shift), 1)
                    counter = window_size - shift
                    total_percent = sum(percentage(x) for x in prev_bps)
            elif base == '':
                # if end of file and still bp remains
                if counter != 0:
                    result.write(str(basepair_location) + "  " + str(int(total_percent * window_size / counter)) + "\n")
                    break
                break
    result.close()


if __name__ == "__main__":
    generate_wiggle(*get_args()[:])
