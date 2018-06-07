"""
Test_3
"""

import pytest
from scripts import GC_analysis


def test_3(capsys):
    """Test_1"""
    with pytest.raises(SystemError):
        GC_analysis.generate_wiggle("./tests/ex3.fasta", "ex3.fasta.wig", 5, 5)
    out, err = capsys.readouterr()
    assert out == "WARNING! The input file is not in fasta format.\n"

if __name__ == "__main__":
    test_3()
