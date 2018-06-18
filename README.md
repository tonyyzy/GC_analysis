[![Build Status](https://travis-ci.org/tonyyzy/GC_analysis.svg?branch=master)](https://travis-ci.org/tonyyzy/GC_analysis)
# GC-analysis
A command-line utility for calculating GC percentages of genome sequences

# Quick starter
Calculate the GC content of chromosome 17 of the human reference genome with window size (or span) = 5 and shift (or step) = 5. Input fasta file is `GRCh38-Chrom17.fasta` and output wiggle file is `CRCh38-Chrom17.wig`. Note that the output file's extension is added by the program.
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o CRCh38-Chrom17
```

# Command-line options
```
~ $ GC_analysis -h
usage: GC_analysis [-h] -i INPUT_FILE -w WINDOW_SIZE -s SHIFT [-o OUTPUT_FILE]
                   [-ot] [-f {wiggle,gzip,bigwig}]

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

```
## Example usage
1. Calculate the GC content of chromosome 17 of the human reference genome, the percentage is calculated over five base pairs (window_size), and the window is shifted by five base pairs every time (i.e. there is no overlapping base paires in each entry).
```
~ $ GC_analysis -i GRCh38-Chrom17.fasta -w 5 -s 5 -o CRCh38-Chrom17
```

2. By default, the GC percentage of the trailing sequence is calculated and appended to the end of the output file. For example, with the following input
```
~ $ GC_analysis -i examaple1.fasta -w 5 -s 5 -o with_tail
```
and `example1.fasta` is
```
>chr1
AAAAACC
```
the generated `with_tail.wig` will look like
```
track type=wiggle_0 name="GC percentage" description="chr1"
variableStep chrom=chr1 span=5
1	0
6	100
```
If it is desirable to omit the trailing sequence in the result, the `-ot` or `--omit_tail` option can be used. For example
```
~ $ GC_analysis -i examaple1.fasta -w 5 -s 5 -o without_tail -ot
```
will generate output file `without_tail` with the following content
```
track type=wiggle_0 name="GC percentage" description="chr1"
variableStep chrom=chr1 span=5
1	0
```
