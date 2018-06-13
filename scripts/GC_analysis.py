"""
A command-line utility for calculating the GC percentage of a genomic sequence.
"""

import argparse as ap
import sys
import gzip
from Bio import SeqIO
import pyBigWig


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
                                                                    "bigwig",
                                                                    "gzip"],
                        default="wiggle")
    args = parser.parse_args()

    return args.input_file, args.output_file, args.window_size, args.shift, args.omit_tail, args.output_format


def open_results_file():
    """A helper function to create the output file in the input file location"""
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
    """A helper function to create the output file in the input file location"""
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
    """Parse the title from the fasta file and write the relevant information to the track definition line of the
    wiggle file."""
    trackline = "track type=wiggle_0 name=\"GC percentage\" description=\"{}\"\n".format(record.description)
    variablestep = "variableStep span={} chrom={}\n".format(str(window_size), record.id)
    if output_format == "wiggle":
        result.write(trackline)
        result.write(variablestep)
    elif output_format == "gzip":
        result.write(bytes(trackline, "utf-8"))
        result.write(bytes(variablestep, "utf-8"))
    elif output_format == "bigwig":
        result.addHeader([(record.id, len(record))])


def write_content(loc, data):
    if output_format == "wiggle":
        result.write(str(loc + 1) + "  " + str(data) + "\n")
    elif output_format == "gzip":
        result.write(bytes(str(loc + 1) + "  " + str(data) + "\n", "utf-8"))
    elif output_format == "bigwig":
        result.addEntries(record.id, [loc], values=[float(data)], span=window_size)


def generate_result():
    seq_len = len(record)
    for i in range((seq_len - window_size + shift) // shift):
        frag = record.seq[i * shift: i * shift + window_size]
        percent = round((frag.count("C") + frag.count("G")) / window_size * 100)
        write_content(i * shift, percent)
    if (i + 1) * shift < seq_len and not omit_tail:
        frag = record.seq[(i + 1) * shift:]
        percent = round((frag.count("C") + frag.count("G")) / len(frag) * 100)
        write_content((i + 1) * shift, percent)
    result.close()


if __name__ == "__main__":
    error = []
    input_file, output_file, window_size, shift, omit_tail, output_format = get_args()[:]
    new_output_format = output_format
    if output_format != "wiggle" and output_file is None:
        sys.stderr.write("WARNING! An output filename is needed to save output as {}. "
                         "The result is shown below:\n".format(output_format))
        error.append("WARNING! An output filename is needed to save output as {}. "
                     "The result is shown above.\n".format(output_format))
        new_output_format = "wiggle"

    if output_format == "bigwig" and window_size > shift:
        sys.stderr.write("WARNING! BigWig file does not allow overlapped items. "
                         "A wiggle file will be generated instead.\n")
        error.append("WARNING! BigWig file does not allow overlapped items. A wiggle file was generated instead.\n")
        new_output_format = "wiggle"

    output_format = new_output_format

    records = SeqIO.index(input_file, "fasta")
    records_num = len(records)
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
