import os.path
import PIL.Image
import unittest
import yaml


class TestJournalPapers(unittest.TestCase):
    def setUp(self) -> None:
        """
        Parse our data files and combine them into a dictionary.
        """
        data_files = [
            'authors',
            'journalpapers',
            'journals'
        ]

        self.data = {}
        for data_current in data_files:
            with open('_data/{}.yml'.format(data_current)) as f:
                self.data[data_current] = yaml.load(f)

    def test_parse_yaml(self) -> None:
        """
        Confirm all YAML from setUp successfully parses.
        """
        pass

    def test_journalpapers_authors_exist(self) -> None:
        """
        Confirm all authors referenced by a paper actually exist.
        """
        for id_journalpaper, journalpaper in self.data['journalpapers'].items():
            for id_author in journalpaper['authors']:
                self.assertIn(
                    id_author,
                    self.data['authors'],
                    '{} references author {} not found in authors.yml'.format(id_journalpaper, id_author)
                )

    def test_journalpapers_journal_exist(self) -> None:
        """
        Confirm all journals referenced by a paper actually exist.
        """
        for id_journalpaper, journalpaper in self.data['journalpapers'].items():
            id_journal = journalpaper['journal']
            self.assertIn(
                id_journal,
                self.data['journals'],
                '{} references journal {} not found in journals.yml'.format(id_journalpaper, id_journal)
            )

    def test_journalpapers_files_exist(self) -> None:
        """
        Confirm all files references by a paper actually exist.
        """
        for id_journalpaper, journalpaper in self.data['journalpapers'].items():
            # Every paper must have a thumb of the right size
            self.assertIn(
                'localthumb',
                journalpaper,
                '{} missing field localthumb'.format(id_journalpaper)
            )
            file_path = journalpaper['localthumb']
            self.assertTrue(
                os.path.isfile('publications/{}'.format(file_path)),
                '{} references localthumb {} not found in publications/'.format(id_journalpaper, file_path)
            )

            file_name = os.path.basename(file_path)
            self.assertRegexpMatches(
                file_name,
                '^[a-z0-9\-\.]*$',
                '{} file name contains illegal characters'.format(id_journalpaper)
            )

            image = PIL.Image.open('publications/{}'.format(file_path))
            self.assertEqual(
                image.size,
                (120, 120),
                '{} image thumb is not 120x120'.format(id_journalpaper)
            )

            # Papers may have a PDF
            if 'localpdf' in journalpaper:
                file_path = journalpaper['localpdf']
                self.assertTrue(
                    os.path.isfile('publications/{}'.format(file_path)),
                    '{} references localpdf {} not found in publications/'.format(id_journalpaper, file_path)
                )

                file_name = os.path.basename(file_path)
                self.assertRegexpMatches(
                    file_name,
                    '^[a-z0-9\-\.]*$',
                    '{} file name contains illegal characters'.format(id_journalpaper)
                )
