[![Build Status](https://travis-ci.org/tonyyzy/GC_analysis.svg?branch=master)](https://travis-ci.org/tonyyzy/GC_analysis)
# GC-analysis
A command-line utility for calculating GC percentages of genome sequences

# Quick starter
```
~ $ GC_analysis -h
usage: GC_analysis [-h] -i INPUT_FILE -w WINDOW_SIZE -s SHIFT [-o OUTPUT_FILE]
                   [-ot] [-f {wiggle,gzip}]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Name of the output file
  -ot, --omit_tail      True: if the trailing sequence should be omitted.
                        Default behaviour is to retain the leftover sequence.
  -f {wiggle,gzip}, --output_format {wiggle,gzip}

required named arguments:
  -i INPUT_FILE, --input_file INPUT_FILE
                        Name of the input file in FASTA format
  -w WINDOW_SIZE, --window_size WINDOW_SIZE
                        Number of base pairs where the GC percentage is
                        calculated for
  -s SHIFT, --shift SHIFT
                        The shift increment

```
## Example usage
1. Calculate the GC content of chromosome 17 of the human reference genome, the percentage is calculated over five base pairs (window_size), and the window is shifted by five base pairs every time (i.e. there is no overlapping base paires in each entry).
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o CRCh38-Chrom17.wig
```
