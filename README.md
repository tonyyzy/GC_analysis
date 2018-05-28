[![Build Status](https://travis-ci.org/tonyyzy/GC_analysis.svg?branch=master)](https://travis-ci.org/tonyyzy/GC_analysis)
# GC-analysis
A command-line utility for calculating GC percentages of genome sequences

# Quick starter
```
~ $ GC_analysis input_file window_size shift [-o output_file]
```
## Example usage
1. Calculate the GC content of chromosome 17 of the human reference genome, the percentage is calculated over five base pairs (window_size), and the window is shifted by five base pairs every time (i.e. there is no overlapping base paires in each entry).
```
~ $ GC_analysis GRCh38-Chrom17.fasta 5 5 -o CRCh38-Chrom17.wig
```
