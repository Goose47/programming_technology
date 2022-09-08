import unittest
from notes import NoteBook


class NotesTestCase(unittest.TestCase):
    def setUp(self):
        self.notebook = NoteBook()

    def test_note_addition(self):
        notes_count = len(self.notebook.noteRepository.all_notes())
        self.notebook.add()

        self.assertEqual(notes_count + 1, len(self.notebook.noteRepository.all_notes()))
        self.assertEqual(self.notebook.noteRepository.last_id, 2)

    def test_note_search(self):
        self.notebook.noteRepository.create_note('Note no1', 'lifestyle')
        self.notebook.noteRepository.create_note('Note no2', 'lifestyle')
        self.notebook.noteRepository.create_note('Note no3', 'chores')

        found_notes = self.notebook.noteRepository.find_notes('lifestyle')

        self.assertEqual(len(found_notes), 2)

if __name__ == '__main__':
    unittest.main()