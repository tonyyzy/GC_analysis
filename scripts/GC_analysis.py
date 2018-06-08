"""
A command-line utility for calculating the GC percentage of an input genomic sequence.
"""

import argparse as ap
import os, sys


def get_args():
    """Helper function to handler all the command-line input options"""
    parser = ap.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-i", "--input_file", type=str, help="Name of the input file in FASTA format", required=True)
    requiredNamed.add_argument("-w", "--window_size", type=int,
                        help="Number of base pairs where the GC percentage is calculated for",
                        required=True)
    requiredNamed.add_argument("-s", "--shift", type=int, help="The shift increment", required=True)
    parser.add_argument("-o", "--output_file", type=str, help="Name of the output file")
    parser.add_argument("-ot", "--omit_tail", action="store_true", help="True: if the trailing sequence should be "
                                                                        "omitted. Default behaviour is to retain "
                                                                        "the leftover sequence.",
                        default=False)
    # parser.add_argument("-f", "--output_format", type=str, choices=["wiggle", "bigwig", "gzip"])
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

    def write_title(title):
        """Parse the title from the fasta file and write the relevant information to the track definition line of the
        wiggle file."""

        # Check if the input file is in fasta format
        if title[0][0] != ">":
            # print("WARNING! The input file is not in fasta format.")
            raise TypeError("WARNING! The input file is not in fasta format.")

        # Check if the input fasta file contains chromosome information
        if "chromosome" in title:
            chrom_index = title.index("chromosome")
            chrom = title[chrom_index + 1][:-1]
            result.write(title[0] + "Chrom=" + str(chrom) + "\n")
        else:
            sys.stderr.write("WARNING! This fasta file does not contain chromosome information.")
            result.write(title[0] + "\n")

    def base_test(counter, total_percent, basepair_location):
        base = genome.read(1)
        # if not EOF and not newline
        if base not in ["", " ", "\n", "\r", ">"]:
            counter += 1
            total_percent += percentage(base)
            # print(total_percent)
            if counter > shift:
                prev_bps[counter - shift - 1] = base
            # if reached window size, write percentage
            if counter == window_size:
                result.write(str(basepair_location) + "  " + str(int(total_percent)) + "\n")
                basepair_location = basepair_location + shift
                counter = window_size - shift
                total_percent = sum(percentage(x) for x in prev_bps)
        elif base == ">":
            sys.stderr.write("WARNING! This fasta file contains more than one sequence. Only the first sequence is "
                             "processed.")
            return 0
        elif base == "":
            # if end of file and still bp remains
            if counter != 0:
                result.write(str(basepair_location) + "  " + str(int(total_percent * window_size / counter)) + "\n")
            return 0
        return counter, total_percent, basepair_location

    with open(input_file, "r") as genome:
        result = open_results_file(input_file, output_file)
        # read title line
        wiggle_title = genome.readline().split(" ")
        write_title(wiggle_title)

        # add step info
        result.write("variableStep span=" + str(window_size) + "\n")
        
        for i in range(window_size):
            try:
                counter, total_percent, basepair_location = base_test(counter, total_percent, basepair_location)
            except TypeError:
                break
        while True:
            try:
                counter, total_percent, basepair_location = base_test(counter, total_percent, basepair_location)
            except TypeError:
                break
    result.close()


if __name__ == "__main__":
    generate_wiggle(*get_args()[:])
