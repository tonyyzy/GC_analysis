"""
A command-line utility for calculating the GC percentage of a genomic sequence.
"""

import argparse as ap
import os
import sys
import gzip


def get_args():
    """Helper function to handler all the command-line input options"""
    parser = ap.ArgumentParser()
    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument("-i", "--input_file", type=str, help="Name of the input file in FASTA format",
                               required=True)
    requiredNamed.add_argument("-w", "--window_size", type=int,
                               help="Number of base pairs where the GC percentage is calculated for",
                               required=True)
    requiredNamed.add_argument("-s", "--shift", type=int, help="The shift increment", required=True)
    parser.add_argument("-o", "--output_file", type=str, help="Name of the output file")
    parser.add_argument("-ot", "--omit_tail", action="store_true", help="True: if the trailing sequence should be "
                                                                        "omitted. Default behaviour is to retain "
                                                                        "the leftover sequence.",
                        default=False)
    parser.add_argument("-f", "--output_format", type=str, choices=["wiggle",
                                                                    # "bigwig",
                                                                    "gzip"],
                        default="wiggle")
    args = parser.parse_args()

    return args.input_file, args.output_file, args.window_size, args.shift, args.omit_tail, args.output_format


def generate_wiggle(input_file, output_file, window_size, shift, omit_tail, output_format):
    """Main function for generating the output file"""
    basepair_location = 1
    counter = 0
    total_percent = 0
    percentage_bp = (1.0 / window_size) * 100
    prev_bps = [""] * (window_size - shift)

    if output_format == "wiggle":
        def write_content(string):
            result.write(string)
    elif output_format == "gzip":
        def write_content(string):
            result.write(bytes(string, "utf-8"))

    def percentage(byte):
        """Test the if the byte is G or C"""
        if byte in ["G", "C"]:
            return percentage_bp
        return 0

    def open_results_file(input_file_name, output_file_name):
        """A helper function to create the output file in the input file location"""
        if output_file_name:
            if output_format == "wiggle":
                file = open(output_file_name, "w+", newline="\n")
            elif output_format == "gzip":
                file = gzip.open(os.path.join(head, output_file_name), "w+")
        else:
            file = sys.stdout
        return file

    def write_title(title):
        """Parse the title from the fasta file and write the relevant information to the track definition line of the
        wiggle file."""

        # Check if the input file is in fasta format
        if title[0][0] != ">":
            sys.stdout.write("WARNING! The input file is not in fasta format.\n")
            raise TypeError()

        # Check if the input fasta file contains chromosome information
        if "chromosome" in title:
            chrom_index = title.index("chromosome")
            chrom = title[chrom_index + 1][:-1]
        else:
            sys.stderr.write("WARNING! This fasta file does not contain chromosome information.\n")
            chrom = "NA"

        write_content("track type=wiggle_0 name=\"{}\" description=\"{}\"\n".format(title[0],
                                                                                    " ".join(title[1:]).strip()))
        write_content("variableStep span={} chrom=chr{}\n".format(str(window_size), chrom))

    def base_test(counter_fun, total_percent_fun, basepair_location_fun):
        base = genome.read(1)
        # if not EOF and not newline
        if base not in ["", " ", "\n", "\r", ">"]:
            counter_fun += 1
            total_percent_fun += percentage(base)
            # print(total_percent)
            if counter_fun > shift:
                prev_bps[counter_fun - shift - 1] = base
            # if reached window size, write percentage
            if counter_fun == window_size:
                write_content(str(basepair_location_fun) + "  " + str(int(total_percent_fun)) + "\n")
                basepair_location_fun = basepair_location_fun + shift
                counter_fun = window_size - shift
                total_percent_fun = sum(percentage(x) for x in prev_bps)
        elif base == ">":
            sys.stderr.write("WARNING! This fasta file contains more than one sequence. Only the first sequence is "
                             "processed.")
            return 0
        elif base == "":
            # if end of file and still bp remains
            if counter_fun != 0 and not omit_tail:
                write_content(str(basepair_location_fun) + "  " + str(int(total_percent_fun * window_size /
                                                                          counter_fun)) + "\n")
            return 0
        return counter_fun, total_percent_fun, basepair_location_fun

    with open(input_file, "r") as genome:
        result = open_results_file(input_file, output_file)
        # read title line
        wiggle_title = genome.readline().split(" ")
        write_title(wiggle_title)

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
