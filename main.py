#!/usr/bin/env python3
"""
Main entry point for intron junction analysis
"""

# Importing libraries 
import argparse
import sys
from pathlib import Path

from sam_utils import process_sam_file
from gene_utils import parse_gene_file
from junction_utils import analyze_and_write_junctions


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        prog="intron_junction_analyzer",
        description="Parses SAM file and creates table with intron junction locations"
    )
    parser.add_argument("sam_file", help="Input SAM file path")
    parser.add_argument("genes_file", help="Gene summary file path")
    parser.add_argument("-o", "--output", help="Output file path (optional)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set default output filename if arugment not used
    if not args.output:
        sam_path = Path(args.sam_file)
        args.output = f"{sam_path.stem}_junctions.txt"
    
    try:
        # Process files
        if args.verbose:
            print(f"Processing SAM file: {args.sam_file}")
        
        junctions = process_sam_file(args.sam_file)
        
        if args.verbose:
            print(f"Found {len(junctions)} unique junctions")
            print(f"Processing genes file: {args.genes_file}")
        
        genes = parse_gene_file(args.genes_file)
        
        if args.verbose:
            print(f"Loaded {len(genes)} genes")
            print(f"Writing results to: {args.output}")
        
        # Analyze and write results
        analyze_and_write_junctions(junctions, genes, args.output)
        
        print(f"Analysis complete. Results written to {args.output}")
        # Handle Errors
    except FileNotFoundError as e:
        sys.exit(f"Error: File not found - {e}")
    except Exception as e:
        sys.exit(f"Error: {e}")


if __name__ == "__main__":
    main()