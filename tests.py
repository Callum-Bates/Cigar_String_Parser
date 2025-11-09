"""
Simple tests for the junction analyzer modules
Made up some random data for each test

"""

from sam_utils import parse_cigar_junctions, parse_nh_tag
from gene_utils import _parse_gene_line
from junction_utils import find_gene_for_junction


def test_cigar_parsing():
    """Test CIGAR string parsing"""
    # Test single junction
    result = parse_cigar_junctions("8M276N75M", 100, "chr1")
    assert result == [("chr1", 108, 384)], f"Expected [('chr1', 108, 384)], got {result}"
    
    # Test multiple junctions
    result = parse_cigar_junctions("8M276N75M320N", 100, "chr1")
    expected = [("chr1", 108, 384), ("chr1", 459, 779)]
    assert result == expected, f"Expected {expected}, got {result}"
    
    # Test with deletions
    result = parse_cigar_junctions("8M2D276N75M", 100, "chr1")
    assert result == [("chr1", 110, 386)], f"Expected [('chr1', 110, 386)], got {result}"
    
    print("CIGAR parsing tests passed")


def test_nh_parsing():
    """Test NH tag parsing"""
    line1 = "read1\t0\tchr1\t100\t60\t50M\t*\t0\t0\tACGT\tIIII\tNH:i:1"
    assert parse_nh_tag(line1) == 1
    
    line2 = "read2\t0\tchr1\t100\t60\t50M\t*\t0\t0\tACGT\tIIII\tNH:i:10"
    assert parse_nh_tag(line2) == 10
    
    line3 = "read3\t0\tchr1\t100\t60\t50M\t*\t0\t0\tACGT\tIIII"
    assert parse_nh_tag(line3) is None
    
    print("NH tag parsing tests passed")


def test_gene_parsing():
    """Test gene line parsing"""
    line = "TGME49_268220\tTGME49_268220-t26_1\tTGME49_chrVIII:6,631,349..6,636,865(+)"
    result = _parse_gene_line(line)
    expected = {'TGME49_268220': ('TGME49_chrVIII', 6631349, 6636865)}
    assert result == expected, f"Expected {expected}, got {result}"
    
    print("Gene parsing tests passed")


def test_junction_gene_matching():
    """Test junction to gene matching"""
    genes = {
        'GENE1': ('chr1', 1000, 2000),
        'GENE2': ('chr1', 3000, 4000)
    }
    
    # Junction within GENE1
    junction1 = ('chr1', 1100, 1200)
    assert find_gene_for_junction(junction1, genes) == 'GENE1'
    
    # Junction outside any gene
    junction2 = ('chr1', 2500, 2600)
    assert find_gene_for_junction(junction2, genes) is None
    
    # Junction on different chromosome
    junction3 = ('chr2', 1100, 1200)
    assert find_gene_for_junction(junction3, genes) is None
    
    print("Junction-gene matching tests passed")


def run_all_tests():
    """Run all tests"""
    print("Test Start")
    test_cigar_parsing()
    test_nh_parsing()
    test_gene_parsing()
    test_junction_gene_matching()
    print("All tests passed.:)")


if __name__ == "__main__":
    run_all_tests()