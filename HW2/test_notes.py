import unittest
from time import sleep
from notes import NoteBook


class NotesTestCase(unittest.TestCase):
    def setUp(self):
        self.notebook = NoteBook()

    def test_last_modified_at_changes(self):
        self.notebook.noteRepository.create_note('sample', 'tag')
        note = self.notebook.noteRepository.find_notes('sample')[0]

        last_modified_at = note.last_modified_at

        sleep(1)

        self.notebook.noteRepository.update_note(1, 'sample', 'tag')
        note = self.notebook.noteRepository.find_notes('sample')[0]

        self.assertNotEqual(last_modified_at, note.last_modified_at)

    def test_last_modified_at_sorting_works(self):
        self.notebook.noteRepository.create_note('note 1', 'tag')
        sleep(1)
        self.notebook.noteRepository.create_note('note 2', 'tag')

        notes = self.notebook.noteRepository.all_notes()

        self.assertEqual(notes[0].note_text, 'note 2')


if __name__ == '__main__':
    unittest.main()