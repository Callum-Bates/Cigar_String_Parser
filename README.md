# Cigar_String_Parser

## About

Small program designed to parse SAM files, and report genomic coordinates of splice junctions.
This works by extracting CIGAR strings for intron-spanning reads, quality filtering of these reads, mapping of reads to genomic coordinates and quantifies how many reads support each junction.
The program outputs a tab-separated file showing gene IDs with associated junction coordinates and read counts.

## Prerequisites

- Git
- python 3.6+

## Installation

**1. Clone the repository:**
```
git clone https://github.com/Callum-Bates/Cigar_String_Parser
cd Cigar_String_Parser
```

## Using Cigar_String_Parser

**At Command Line**

```
python main.py <sam_file> <genes_file>

# With options
python main.py input.sam genes.txt -o output.txt --verbose
```

## Help
- <sam_file> - File path to input SAM file containing RNA-seq data
- <genes_file> - Tab-separated file with gene IDs and genomic coordinates string
- -o - Specify output file name
- --verbose - Enable verbose mode - detailed processing information displayed

## License
This project is licensed under the [MIT License](LICENSE).

