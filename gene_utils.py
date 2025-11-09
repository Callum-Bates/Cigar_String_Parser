"""
Utilities for processing gene annotation files
"""


def parse_gene_file(genes_filename):
    """
    Parse gene summary file
    
    Returns:
        dict: {gene_id: (chromosome, start, end)}
    """
    genes = {}
    
    with open(genes_filename, 'r') as gene_file:
        # Skip header if present
        first_line = next(gene_file, None)
        if first_line and not first_line.startswith('TGME49_'):
            pass  # Header was skipped
        else:
            # Process first line if it's data
            genes.update(_parse_gene_line(first_line))
        
        # Process remaining lines
        for line in gene_file:
            genes.update(_parse_gene_line(line))
    
    return genes


def _parse_gene_line(line):
    """Parse a single gene line and return gene info"""
    if not line or not line.strip():
        return {}
    
    parts = line.strip().split("\t")
    if len(parts) < 3:
        return {}
    
    gene_id = parts[0]
    location_info = parts[2]
    
    # Parse location: "chromosome:start..end(strand)"
    if ':' not in location_info or '..' not in location_info:
        return {}
    
    try:
        chrom_part, coord_part = location_info.split(':', 1)
        coord_clean = coord_part.split('(')[0]  # Remove strand info
        start_str, end_str = coord_clean.split('..')
        
        # Remove commas, convert to integers
        start = int(start_str.replace(',', ''))
        end = int(end_str.replace(',', ''))
        
        return {gene_id: (chrom_part, start, end)}
    
    except (ValueError, IndexError):
        return {}