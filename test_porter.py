import csv
import unittest
from reporter import RePorterStemmer as ps

class TestPorterStemmer(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(ValueError):
            ps.stem('')

    def test_csv_sample(self):
        with open('test_sample.csv', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            for word, expected in csvreader:
                self.assertEqual(ps.stem(word), expected)

    def test_custom(self):
        words = {
            'гналась': 'гнал',
            'противоестесвтенном':'противоестесвтен',
            'выживший':'выж',
            'забегавшись':'забега',
            'неотвратимость':'неотвратим',
            'падшему':'падш'
        }
        
        for word, expected in words.items():
            stemmed = ps.stem(word)
            self.assertEqual(stemmed, expected)
            
if __name__ == '__main__':
    unittest.main()