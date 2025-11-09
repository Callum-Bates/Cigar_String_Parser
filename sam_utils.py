"""
Utilities for processing SAM files
"""

import re
from collections import defaultdict


def parse_nh_tag(sam_line):
    """Extract NH tag value from SAM line"""
    nh_match = re.search(r'NH:i:(\d+)', sam_line)
    return int(nh_match.group(1)) if nh_match else None


def parse_cigar_junctions(cigar, start_pos, chromosome):
    """
    Parse CIGAR string to find intron junctions
    
    Returns:
        List of tuples: (chromosome, junction_start, junction_end)
    """
    junctions = []
    current_pos = start_pos
    
    for match in re.finditer(r"(\d+)([MDN])", cigar):
        length = int(match.group(1))
        operation = match.group(2)
        
        if operation in ["M", "D"]:
            current_pos += length
        elif operation == "N":
            junction_start = current_pos
            junction_end = current_pos + length
            junctions.append((chromosome, junction_start, junction_end))
            current_pos = junction_end
    
    return junctions


def process_sam_file(sam_filename):
    """
    Process SAM file and return junction counts
    
    Returns:
        dict: {(chromosome, start, end): count}
    """
    junction_counts = defaultdict(int)
    
    with open(sam_filename, 'r') as sam_file:
        for line in sam_file:
            if line.startswith("@"):  # Skip headers
                continue
            
            parts = line.strip().split("\t")
            if len(parts) < 6:
                continue
            
            # Extract SAM fields
            chromosome = parts[2]
            cigar = parts[5]
            
            try:
                start_pos = int(parts[3])
            except ValueError:
                continue  # Skip malformed lines
            
            # Only process uniquely mapped reads with introns
            if parse_nh_tag(line) != 1 or 'N' not in cigar:
                continue
            
            # Find junctions and count them
            junctions = parse_cigar_junctions(cigar, start_pos, chromosome)
            for junction in junctions:
                junction_counts[junction] += 1
    
    return dict(junction_counts)