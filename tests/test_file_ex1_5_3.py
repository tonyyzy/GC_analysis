"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["python3", "./GC_analysis/GC_analysis.py",
                    "-i", "./tests/ex1.fasta",
                    "-o", "./tests/ex1_5_3_test",
                    "-w", "5",
                    "-s", "3"])
    assert filecmp.cmp("./tests/ex1_5_3_test.wig", "./tests/ex1_5_3.wig")


if __name__ == "__main__":
    test_1()
