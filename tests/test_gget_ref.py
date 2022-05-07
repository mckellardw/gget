import unittest
from gget.gget_ref import ref


class TestRef(unittest.TestCase):
    def test_ref(self):
        result_to_test = ref(
            "taeniopygia_guttata", which="all", release=None, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/cdna/Taeniopygia_guttata.bTaeGut1_v1.p.cdna.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": "27460065",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "21-Feb-2022",
                    "release_time": "10:57",
                    "bytes": "318945687",
                },
                "annotation_gtf": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
                    "ensembl_release": 106,
                    "release_date": "02-Mar-2022",
                    "release_time": "03:06",
                    "bytes": "13462785",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/cds/Taeniopygia_guttata.bTaeGut1_v1.p.cds.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": "13909381",
                },
                "non-coding_seq_ncRNA": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/ncrna/Taeniopygia_guttata.bTaeGut1_v1.p.ncrna.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "11:56",
                    "bytes": " 5204084",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.bTaeGut1_v1.p.pep.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": " 8682829",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_which(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["gtf", "dna", "pep"], release=None, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "annotation_gtf": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
                    "ensembl_release": 106,
                    "release_date": "02-Mar-2022",
                    "release_time": "03:06",
                    "bytes": "13462785",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "21-Feb-2022",
                    "release_time": "10:57",
                    "bytes": "318945687",
                },
                "protein_translation_pep": {
                    "ftp": "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.bTaeGut1_v1.p.pep.all.fa.gz",
                    "ensembl_release": 106,
                    "release_date": "23-Feb-2022",
                    "release_time": "07:18",
                    "bytes": " 8682829",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["cdna", "dna", "cds"], release=76, ftp=False
        )
        expected_result = {
            "taeniopygia_guttata": {
                "transcriptome_cdna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/cdna/Taeniopygia_guttata.taeGut3.2.4.cdna.all.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "10:53",
                    "bytes": " 8522766",
                },
                "genome_dna": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.taeGut3.2.4.dna.toplevel.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "01:16",
                    "bytes": "368607088",
                },
                "coding_seq_cds": {
                    "ftp": "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/cds/Taeniopygia_guttata.taeGut3.2.4.cds.all.fa.gz",
                    "ensembl_release": 76,
                    "release_date": "19-Jul-2014",
                    "release_time": "10:53",
                    "bytes": " 7972695",
                },
            }
        }

        self.assertEqual(result_to_test, expected_result)

    def test_ref_rel_ftp(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["gtf", "dna", "pep"], release=76, ftp=True
        )
        expected_result = [
            "http://ftp.ensembl.org/pub/release-76/gtf/taeniopygia_guttata/Taeniopygia_guttata.taeGut3.2.4.76.gtf.gz",
            "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.taeGut3.2.4.dna.toplevel.fa.gz",
            "http://ftp.ensembl.org/pub/release-76/fasta/taeniopygia_guttata/pep/Taeniopygia_guttata.taeGut3.2.4.pep.all.fa.gz",
        ]

        self.assertEqual(result_to_test, expected_result)

    def test_ref_ftp(self):
        result_to_test = ref(
            "taeniopygia_guttata", which=["dna", "ncrna", "gtf"], release=None, ftp=True
        )
        expected_result = [
            "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/dna/Taeniopygia_guttata.bTaeGut1_v1.p.dna.toplevel.fa.gz",
            "http://ftp.ensembl.org/pub/release-106/fasta/taeniopygia_guttata/ncrna/Taeniopygia_guttata.bTaeGut1_v1.p.ncrna.fa.gz",
            "http://ftp.ensembl.org/pub/release-106/gtf/taeniopygia_guttata/Taeniopygia_guttata.bTaeGut1_v1.p.106.gtf.gz",
        ]

        self.assertEqual(result_to_test, expected_result)

    ## Test bad input errors
    def test_ref_bad_species(self):
        with self.assertRaises(ValueError):
            ref("banana", which=["cdna", "dna", "cds"], release=76, ftp=False)

    def test_ref_bad_which(self):
        with self.assertRaises(ValueError):
            ref("taeniopygia_guttata", which=["sneeze"], release=105, ftp=False)

    def test_ref_bad_rel(self):
        with self.assertRaises(ValueError):
            ref("taeniopygia_guttata", which=["gtf"], release=2000, ftp=False)