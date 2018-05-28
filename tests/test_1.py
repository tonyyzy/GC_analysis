"""
Test_1
"""

import filecmp
from scripts import GC_analysis


def test_1():
    """Test_1"""
    GC_analysis.generate_wiggle("./tests/example.fasta", "test_1.wig", 5, 5)
    print(filecmp.cmp("./tests/test_1.wig", "./tests/example.wig"))


if __name__ == "__main__":
    test_1()
