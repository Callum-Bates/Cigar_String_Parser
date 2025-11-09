"""
Utilities for analyzing junctions and writing results
"""

from collections import defaultdict


def find_gene_for_junction(junction, genes):
    """
    Find which gene contains a junction
    
    Args:
        junction: (chromosome, start, end)
        genes: {gene_id: (chromosome, start, end)}
    
    Returns:
        gene_id or None
    """
    chrom, j_start, j_end = junction
    
    for gene_id, (g_chrom, g_start, g_end) in genes.items():
        if (chrom == g_chrom and 
            g_start <= j_start <= g_end and 
            g_start <= j_end <= g_end):
            return gene_id
    
    return None


def group_junctions_by_gene(junctions, genes):
    """
    Group junctions by their containing genes
    
    Returns:
        dict: {gene_id: [(start, end, count), ...]}
    """
    gene_junctions = defaultdict(list)
    
    for junction, count in junctions.items():
        gene_id = find_gene_for_junction(junction, genes)
        if gene_id:
            chrom, start, end = junction
            gene_junctions[gene_id].append((start, end, count))
    
    # Sort junctions within each gene by start position
    for gene_id in gene_junctions:
        gene_junctions[gene_id].sort(key=lambda x: x[0])
    
    return dict(gene_junctions)


def write_results(output_filename, gene_junctions):
    """Write junction results to file"""
    with open(output_filename, 'w') as output_file:
        # Wrie header
        output_file.write("Gene_ID\tJunction_Start\tJunction_End\tCount\n")
        
        # Write data  - sorted by gene ID
        for gene_id in sorted(gene_junctions.keys()):
            junctions = gene_junctions[gene_id]
            
            for start, end, count in junctions:
                output_file.write(f"{gene_id}\t{start}\t{end}\t{count}\n")
            
            # Add blank line between genes (except for last gene) - maybe add option for no spaces / some other way to sort by genes
            if gene_id != sorted(gene_junctions.keys())[-1]:
                output_file.write("\n")


def analyze_and_write_junctions(junctions, genes, output_filename):
    """Complete analysis pipeline: group junctions and write results"""
    gene_junctions = group_junctions_by_gene(junctions, genes)
    write_results(output_filename, gene_junctions)
    return len(gene_junctions)