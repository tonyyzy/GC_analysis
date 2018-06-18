"""
Test_1
"""

import filecmp
import subprocess


def test_1():
    """Test_1"""
    subprocess.run(["python3", "./scripts/GC_analysis.py",
                    "-i", "./tests/ex1.fasta",
                    "-o", "./tests/ex1_5_5_ot_bw_test",
                    "-w", "5",
                    "-s", "5",
                    "-ot",
                    "-f", "bigwig"])
    subprocess.run(["wget", "http://hgdownload.soe.ucsc.edu/admin/exe/linux.x86_64/bigWigToWig"])
    subprocess.run(["./bigWigTowig", "./tests/ex1_5_5_ot_bw_test.bw", "./tests/ex1_5_5_ot_bw_test.wig"])
    assert filecmp.cmp("./tests/ex1_5_5_ot_bw_test.wig", "./tests/ex1_5_5_ot_bw.wig")


if __name__ == "__main__":
    test_1()
