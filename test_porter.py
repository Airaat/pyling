#!/usr/bin/env python3
import csv
import unittest
from porter import stem


class TestPorterStemmer(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(ValueError):
            stem('')

    def test_csv_sample(self):
        with open('test_sample.csv', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for word, expected in csvreader:
                self.assertEqual(stem(word), expected)

    def test_custom(self):
        words = {
            'гналась': 'гнал',
            'противоестесвтенном': 'противоестесвтен',
            'выживший': 'выж',
            'забегавшись': 'забега',
            'неотвратимость': 'неотвратим',
            'падшему': 'падш',
            'работал': 'работа',
            'валяются': 'валя',
        }

        for word, expected in words.items():
            stemmed = stem(word)
            self.assertEqual(stemmed, expected)


if __name__ == '__main__':
    unittest.main()
