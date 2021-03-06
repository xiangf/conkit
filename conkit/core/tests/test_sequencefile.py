"""Testing facility for conkit.core.SequenceFile"""

__author__ = "Felix Simkovic"
__date__ = "12 Aug 2016"

import unittest

try:
    import scipy.spatial
    SCIPY = True
except ImportError:
    SCIPY = False

from conkit.core.sequence import Sequence
from conkit.core.sequencefile import SequenceFile


def skipUnless(condition):
    if condition:
        return lambda x: x
    else:
        return lambda x: None


class TestSequenceFile(unittest.TestCase):
    def test_ascii_matrix_1(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', '-CC-C-'), Sequence('doe', 'BBBBBB')]:
            sequence_file.add(seq)
        matrix = sequence_file.ascii_matrix
        self.assertEqual([65, 65, 65, 65, 65, 65], list(matrix)[0])
        self.assertEqual([45, 67, 67, 45, 67, 45], list(matrix)[1])
        self.assertEqual([66, 66, 66, 66, 66, 66], list(matrix)[2])

    def test_is_alignment_1(self):
        sequence_file = SequenceFile('test')
        sequence_file.add(Sequence('foo', 'AAAAA'))
        sequence_file.add(Sequence('bar', 'BBBBB'))
        self.assertTrue(sequence_file.is_alignment)

    def test_is_alignment_2(self):
        sequence_file = SequenceFile('test')
        sequence_file.add(Sequence('foo', 'AAAAA'))
        sequence_file.add(Sequence('bar', 'BBBB'))
        self.assertFalse(sequence_file.is_alignment)

    def test_empty_1(self):
        sequence_file = SequenceFile("test")
        self.assertTrue(sequence_file.empty)

    def test_empty_2(self):
        sequence_file = SequenceFile("test")
        sequence_file.add(Sequence('foo', 'AAAAA'))
        self.assertFalse(sequence_file.empty)

    def test_nseq_1(self):
        sequence_file = SequenceFile('test')
        self.assertEqual(0, sequence_file.nseq)

    def test_nseq_2(self):
        sequence_file = SequenceFile('test')
        sequence_file.add(Sequence('foo', 'AAAAA'))
        self.assertEqual(1, sequence_file.nseq)

    def test_nseq_3(self):
        sequence_file = SequenceFile('test')
        sequence_file.add(Sequence('foo', 'AAAAA'))
        sequence_file.add(Sequence('bar', 'BBBBB'))
        self.assertEqual(2, sequence_file.nseq)

    def test_remark_1(self):
        sequence_file = SequenceFile('test')
        sequence_file.remark = 'Hello'
        self.assertEqual(['Hello'], sequence_file.remark)

    def test_remark_2(self):
        sequence_file = SequenceFile('test')
        sequence_file.remark = 'Hello'
        sequence_file.remark = 'World'
        self.assertEqual(['Hello', 'World'], sequence_file.remark)

    def test_remark_3(self):
        sequence_file = SequenceFile('test')
        sequence_file.remark = 'Hello'
        sequence_file.remark = '5'
        sequence_file.remark = 'World'
        sequence_file.remark = '!'
        self.assertEqual(['Hello', '5', 'World', '!'], sequence_file.remark)

    def test_remark_4(self):
        sequence_file = SequenceFile('test')
        self.assertEqual([], sequence_file.remark)

    def test_remark_5(self):
        sequence_file = SequenceFile('test')
        sequence_file.remark = 'hello'
        sequence = Sequence('foo', 'GSMFTPK')
        sequence.remark = 'bar'
        sequence_file.add(sequence)
        self.assertEqual(['hello'], sequence_file.remark)
        self.assertEqual(['bar'], sequence_file[0].remark)

    def test_top_sequence_1(self):
        sequence_file = SequenceFile('test')
        self.assertEqual(None, sequence_file.top_sequence)

    def test_top_sequence_2(self):
        sequence_file = SequenceFile('test')
        sequence1 = Sequence('foo', 'AAAAA')
        sequence_file.add(sequence1)
        self.assertEqual(sequence1, sequence_file.top_sequence)

    def test_top_sequence_3(self):
        sequence_file = SequenceFile('test')
        sequence1 = Sequence('foo', 'AAAAA')
        sequence2 = Sequence('bar', 'BBBBB')
        sequence_file.add(sequence1)
        sequence_file.add(sequence2)
        self.assertEqual(sequence1, sequence_file.top_sequence)

    @skipUnless(SCIPY)
    def test_calculate_weights_1(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AAAAAAA'),
                Sequence('cho', 'AAAAAAA'),
                Sequence('baz', 'AAAAAAA')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.7)
        self.assertEqual(weights, [0.25, 0.25, 0.25, 0.25])

    @skipUnless(SCIPY)
    def test_calculate_weights_2(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AAAAAAA'),
                Sequence('cho', 'AAAAAAA'),
                Sequence('baz', 'BBBBBBB')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.7)
        self.assertEqual(weights, [0.3333333333333333, 0.3333333333333333, 0.3333333333333333, 1.0])

    @skipUnless(SCIPY)
    def test_calculate_weights_3(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'A-AABA-'),
                Sequence('cho', 'B-BAA--'),
                Sequence('baz', 'BBBBBBB')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.7)
        self.assertEqual(weights, [1.0, 1.0, 1.0, 1.0])

    @skipUnless(SCIPY)
    def test_calculate_weights_4(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AAAABA-'),
                Sequence('cho', 'B-BAA--'),
                Sequence('baz', 'BBBBBBB')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.7)
        self.assertEqual(weights, [0.5, 0.5, 1.0, 1.0])

    @skipUnless(SCIPY)
    def test_calculate_weights_5(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AA-ABA-'),
                Sequence('cho', 'B-BAA--'),
                Sequence('baz', 'BBBBBBB')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.6)
        self.assertEqual(weights, [1.0, 1.0, 1.0, 1.0])

    @skipUnless(SCIPY)
    def test_calculate_weights_6(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AA-ABA-'),
                Sequence('cho', 'AAACBAA'),
                Sequence('doo', 'B-BAA--'),
                Sequence('miu', 'BBBBBBB'),
                Sequence('nop', 'AAAAAAB')
        ]:
            sequence_file.add(s)
        weights = sequence_file.calculate_weights(identity=0.6)
        self.assertEqual(weights, [0.3333333333333333, 1.0, 0.5, 1.0, 1.0, 0.5])

    @skipUnless(SCIPY)
    def test_calculate_weights_6(self):
        sequence_file = SequenceFile('test')
        for s in [
                Sequence('foo', 'AAAAAAA'),
                Sequence('bar', 'AA-ABA-'),
                Sequence('cho', 'AAACBAA'),
                Sequence('doo', 'B-BAA--'),
                Sequence('miu', 'BBBBBBB'),
                Sequence('nop', 'AAAAAAB')
        ]:
            sequence_file.add(s)
        self.assertEqual(5, sequence_file.neff)

    def test_calculate_freq_1(self):
        sequence_file = SequenceFile('test')
        for s in [Sequence('foo', 'AAAAAAA'), Sequence('bar', 'A-AAAA-'), Sequence('cho', '--AAA--')]:
            sequence_file.add(s)
        calculated_freqs = [round(i, 6) for i in sequence_file.calculate_freq()]
        self.assertEqual([0.666667, 0.333333, 1.0, 1.0, 1.0, 0.666667, 0.333333], calculated_freqs)

    def test_calculate_freq_2(self):
        sequence_file = SequenceFile('test')
        for s in [Sequence('foo', '-------'), Sequence('bar', '-------'), Sequence('cho', '-------')]:
            sequence_file.add(s)
        calculated_freqs = [round(i, 6) for i in sequence_file.calculate_freq()]
        self.assertEqual([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], calculated_freqs)

    def test_calculate_freq_3(self):
        sequence_file = SequenceFile('test')
        for s in [Sequence('foo', 'AAAAAAA'), Sequence('bar', 'AAAAAAA'), Sequence('cho', 'AAAAAAA')]:
            sequence_file.add(s)
        calculated_freqs = [round(i, 6) for i in sequence_file.calculate_freq()]
        self.assertEqual([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], calculated_freqs)

    def test_sort_1(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_sorted = sequence_file.sort('id', reverse=False, inplace=False)
        self.assertEqual(['bar', 'doe', 'foo'], [s.id for s in sequence_file_sorted])
        self.assertEqual(['BBBBB', 'CCCCC', 'AAAAA'], [s.seq for s in sequence_file_sorted])
        self.assertNotEqual(sequence_file, sequence_file_sorted)

    def test_sort_2(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_sorted = sequence_file.sort('id', reverse=True, inplace=False)
        self.assertEqual(['foo', 'doe', 'bar'], [s.id for s in sequence_file_sorted])
        self.assertEqual(['AAAAA', 'CCCCC', 'BBBBB'], [s.seq for s in sequence_file_sorted])
        self.assertNotEqual(sequence_file, sequence_file_sorted)

    def test_sort_3(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_sorted = sequence_file.sort('seq', reverse=False, inplace=True)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in sequence_file_sorted])
        self.assertEqual(['AAAAA', 'BBBBB', 'CCCCC'], [s.seq for s in sequence_file_sorted])
        self.assertEqual(sequence_file, sequence_file_sorted)

    def test_sort_4(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_sorted = sequence_file.sort('seq', reverse=True, inplace=True)
        self.assertEqual(['doe', 'bar', 'foo'], [s.id for s in sequence_file_sorted])
        self.assertEqual(['CCCCC', 'BBBBB', 'AAAAA'], [s.seq for s in sequence_file_sorted])
        self.assertEqual(sequence_file, sequence_file_sorted)

    def test_trim_1(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_trimmed = sequence_file.trim(1, 5)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in sequence_file_trimmed])
        self.assertEqual(['AAAAA', 'BBBBB', 'CCCCC'], [s.seq for s in sequence_file_trimmed])
        self.assertNotEqual(sequence_file, sequence_file_trimmed)

    def test_trim_2(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAA'), Sequence('bar', 'BBBBB'), Sequence('doe', 'CCCCC')]:
            sequence_file.add(seq)
        sequence_file_trimmed = sequence_file.trim(3, 5)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in sequence_file_trimmed])
        self.assertEqual(['AAA', 'BBB', 'CCC'], [s.seq for s in sequence_file_trimmed])
        self.assertNotEqual(sequence_file, sequence_file_trimmed)

    def test_trim_3(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'ABCDE'), Sequence('bar', 'BCDEF'), Sequence('doe', 'CDEFG')]:
            sequence_file.add(seq)
        sequence_file_trimmed = sequence_file.trim(1, 3)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in sequence_file_trimmed])
        self.assertEqual(['ABC', 'BCD', 'CDE'], [s.seq for s in sequence_file_trimmed])
        self.assertNotEqual(sequence_file, sequence_file_trimmed)

    def test_trim_4(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'ABCDE'), Sequence('bar', 'BCDEF'), Sequence('doe', 'CDEFG')]:
            sequence_file.add(seq)
        sequence_file_trimmed = sequence_file.trim(2, 3)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in sequence_file_trimmed])
        self.assertEqual(['BC', 'CD', 'DE'], [s.seq for s in sequence_file_trimmed])
        self.assertNotEqual(sequence_file, sequence_file_trimmed)

    @skipUnless(SCIPY)
    def test_filter_1(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'AAAAAA'), Sequence('doe', 'AAAAAA')]:
            sequence_file.add(seq)
        filtered = sequence_file.filter(min_id=0.0, max_id=1.0)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in filtered])

    @skipUnless(SCIPY)
    def test_filter_2(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'AAAABB'), Sequence('doe', 'AAAAAA')]:
            sequence_file.add(seq)
        filtered = sequence_file.filter(min_id=0.0, max_id=0.9)
        self.assertEqual(['foo', 'bar'], [s.id for s in filtered])

    @skipUnless(SCIPY)
    def test_filter_3(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'AAAAAA'), Sequence('doe', 'BBBBBB')]:
            sequence_file.add(seq)
        filtered = sequence_file.filter(min_id=0.0, max_id=0.9)
        self.assertEqual(['foo', 'doe'], [s.id for s in filtered])

    @skipUnless(SCIPY)
    def test_filter_4(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'CCCCCC'), Sequence('doe', 'BBBBBB')]:
            sequence_file.add(seq)
        filtered = sequence_file.filter(min_id=0.0, max_id=0.9)
        self.assertEqual(['foo', 'bar', 'doe'], [s.id for s in filtered])

    @skipUnless(SCIPY)
    def test_filter_5(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'CCCCCC'), Sequence('doe', 'BBBBBB')]:
            sequence_file.add(seq)
        filtered = sequence_file.filter(min_id=0.1, max_id=0.9)
        self.assertEqual(['foo'], [s.id for s in filtered])

    def test_diversity_1(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'CCCCCC'), Sequence('doe', 'BBBBBB')]:
            sequence_file.add(seq)
        self.assertEqual(0.289, sequence_file.diversity)

    def test_diversity_2(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'AAAAAA'), Sequence('doe', 'AAAAAA')]:
            sequence_file.add(seq)
        self.assertEqual(0.289, sequence_file.diversity)

    def test_diversity_3(self):
        sequence_file = SequenceFile('test')
        self.assertEqual(0.0, sequence_file.diversity)

    def test_diversity_4(self):
        sequence_file = SequenceFile('test')
        for seq in [Sequence('foo', 'AAAAAA'), Sequence('bar', 'B'), Sequence('doe', 'CCC')]:
            sequence_file.add(seq)
        with self.assertRaises(ValueError):
            sequence_file.diversity


if __name__ == "__main__":
    unittest.main(verbosity=2)
