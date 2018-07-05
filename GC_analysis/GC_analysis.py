#!/usr/bin/env python3
"""
A command-line utility for calculating the GC percentage of a genomic sequence.
"""

import argparse as ap
import sys
import gzip
from Bio import SeqIO
import pyBigWig


def get_args():
    """
    Helper function uses ArgParser to handler all the command-line input options.
    All arguments are keyword arguments. The required arguments are grouped under "required named arguments" section in
    help (-h).

    required named arguments:

    -i INPUT_FILE, --input_file INPUT_FILE
    INPUTFILE: Name of the input file in FASTA format

    -w WINDOW_SIZE, --window_size WINDOW_SIZE
    WINDOW_SIZE: Number of base pairs that the GC percentage is calculated for

    -s SHIFT, --shift SHIFT
    SHIFT: The shift increment (step size)

    optional arguments:

    -h, --help
    Show the help message and exit

    -o OUTPUT_FILE, --output_file OUTPUT_FILE
    OUTPUT_FILE: Name of the output file

    -ot, --omit_tail
    Use if the trailing sequence should be omitted. Default behaviour is to retain the leftover sequence.

    -f {wiggle,bigwig,gzip}, --output_format {wiggle,bigwig,gzip}
    Choose output formats from wiggle, bigwig or gzip compressed wiggle file.

    :returns: str, str/None, int, int, Bool, str
    """
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
                                                                    "bigwig",
                                                                    "gzip"],
                        default="wiggle")
    args = parser.parse_args()

    return args.input_file, args.output_file, args.window_size, args.shift, args.omit_tail, args.output_format


def open_results_file():
    """
    A helper function to create the output file based on chosen output format and specified output filename.

    If output filename is given and output format is "wiggle", a text file called "OUTPUT_FILENAME.wig" will be opened
    with python's textIO wrapper, where OUTPUT_FILENAME is the string given after "-o" option in the commandline.

    If output filename is given and output format is "gzip", a compressed file called "OUTPUT_FILENAME.gz" will be
    opened with gzip library, where OUTPUT_FILENAME is the string given after "-o" option in the commandline.

    If output filename is given and output format is "bigwig", a binary file called "OUTPUT_FILENAME.bw" will be
    opened with pyBigWig, where OUTPUT_FILENAME is the string given after "-o" option in the commandline.

    If output filename is not specified, the result will be written to stdout following wiggle format.

    :return: file object
    """
    if output_file:
        if output_format == "wiggle":
            file = open(output_file + ".wig", "w+", newline="\n")
        elif output_format == "gzip":
            file = gzip.open(output_file + ".wig.gz", "w+")
        elif output_format == "bigwig":
            file = pyBigWig.open(output_file + ".bw", "w+")
    else:
        file = sys.stdout
    return file


def open_results_files():
    """
    A helper function to create the output file based on chosen output format and specified output filename. Used when
    multiple sequences present in one input file. "_seqNUM" will be added to the end of the output filename before the
    file extension.

    If output filename is given and output format is "wiggle", a text file called "OUTPUT_FILENAME_seqNUM.wig" will be
    opened with python's textIO wrapper, where OUTPUT_FILENAME is the string given after "-o" option in the commandline
    and NUM is the ordinal number of the sequence.

    If output filename is given and output format is "gzip", a compressed file called "OUTPUT_FILENAME_seqNUM.gz" will
    be opened with gzip library, where OUTPUT_FILENAME is the string given after "-o" option in the commandline
    and NUM is the ordinal number of the sequence.

    If output filename is given and output format is "bigwig", a binary file called "OUTPUT_FILENAME_seqNUM.bw" will be
    opened with pyBigWig, where OUTPUT_FILENAME is the string given after "-o" option in the commandline
    and NUM is the ordinal number of the sequence.

    If output filename is not specified, the result will be written to stdout following wiggle format.

    :return: file object
    """
    if output_file:
        if output_format == "wiggle":
            file = open(output_file + "_seq{}.wig".format(seq_num), "w+", newline="\n")
        elif output_format == "gzip":
            file = gzip.open(output_file + "_seq{}.wig.gz".format(seq_num), "w+")
        elif output_format == "bigwig":
            file = pyBigWig.open(output_file + "_seq{}.bw".format(seq_num), "w+")
    else:
        file = sys.stdout
    return file


def write_title():
    """Write information to the track definition line of the wiggle file.
    :return: None
    """

    trackline = "track type=wiggle_0 name=\"GC percentage\" description=\"{}\"\n".format(record.description)
    variablestep = "variableStep chrom={} span={}\n".format(record.id, str(window_size))
    if output_format == "wiggle":
        result.write(trackline)
        result.write(variablestep)
    elif output_format == "gzip":
        result.write(bytes(trackline, "utf-8"))
        result.write(bytes(variablestep, "utf-8"))
    elif output_format == "bigwig":
        result.addHeader([(record.id, len(record))])


def generate_write_content():
    """
    Generate a write_content function to handle writing results to output file.
    :return: function
    """
    if output_format == "wiggle":
        def content(loc, data):
            result.write(str(loc + 1) + "\t" + str(data) + "\n")
    elif output_format == "gzip":
        def content(loc, data):
            result.write(bytes(str(loc + 1) + "\t" + str(data) + "\n", "utf-8"))
    elif output_format == "bigwig":
        def content(loc, data):
            result.addEntries(record.id, [loc], values=[float(data)], span=window_size)
    return content


def generate_result():
    """
    Calculate GC percentage and write to output file.
    :return: None
    """
    seq_len = len(record)  # Get length of sequence
    for i in range((seq_len - window_size + shift) // shift):  # Iterate over the total number of shifts
        frag = record.seq[i * shift: i * shift + window_size]  # Extract the string for counting
        # Count number of C and G and convert to percentage
        percent = round((frag.count("C") + frag.count("G")) / window_size * 100)
        write_content(i * shift, percent)
    if (i + 1) * shift < seq_len and not omit_tail:
        # if trailing sequence exits and omit_tail is False
        frag = record.seq[(i + 1) * shift:]
        percent = round((frag.count("C") + frag.count("G")) / len(frag) * 100)
        write_content((i + 1) * shift, percent)
    result.close()


if __name__ == "__main__":
    error = []  # Store generated error message, and write to stderr at the end of stdout output
    input_file, output_file, window_size, shift, omit_tail, output_format = get_args()[:]
    new_output_format = output_format

    if output_format == "bigwig" and window_size > shift:
        sys.stderr.write("WARNING! BigWig file does not allow overlapped items. "
                         "A wiggle file will be generated instead.\n")
        error.append("WARNING! BigWig file does not allow overlapped items. A wiggle file was generated instead.\n")
        new_output_format = "wiggle"

    if output_format != "wiggle" and output_file is None:
        sys.stderr.write("WARNING! An output filename is needed to save output as {}. "
                         "The result is shown below:\n".format(output_format))
        error.append("WARNING! An output filename is needed to save output as {}. "
                     "The result is shown above.\n".format(output_format))
        new_output_format = "wiggle"

    output_format = new_output_format

    records = SeqIO.index(input_file, "fasta")
    records_num = len(records)
    write_content = generate_write_content()
    if records_num < 1:
        sys.stdout.write("WARNING! {} contains no sequence data.\n".format(input_file))
        raise TypeError
    elif records_num == 1:
        record = records[records.keys().__next__()]
        result = open_results_file()
        write_title()
        generate_result()
    else:
        seq_num = 0
        for key in records.keys():
            seq_num += 1
            record = records[key]
            result = open_results_files()
            write_title()
            generate_result()
    if output_file is None:
        for err in error:
            sys.stderr.write(err)
