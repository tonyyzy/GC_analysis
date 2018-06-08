"""
Test_1
"""

import filecmp
from scripts import GC_analysis


def test_1():
    """Test_1"""
    GC_analysis.generate_wiggle("./tests/ex1.fasta", "ex1.fasta.wig", 5, 3, False)
    assert filecmp.cmp("./tests/ex1.fasta.wig", "./tests/ex1_5_3.wig")


if __name__ == "__main__":
    test_1()
