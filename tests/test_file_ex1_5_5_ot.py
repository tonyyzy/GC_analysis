"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["python3", "./scripts/GC_analysis.py",
                    "-i", "./tests/ex1.fasta",
                    "-o", "./tests/ex1_5_5_ot_test",
                    "-w", "5",
                    "-s", "5",
                    "-ot"])
    assert filecmp.cmp("./tests/ex1_5_5_ot_test.wig", "./tests/ex1_5_5_ot.wig")


if __name__ == "__main__":
    test_1()
