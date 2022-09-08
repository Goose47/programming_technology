import sys
import datetime


# A Note Repository do deal with our dummy note database
class NoteRepository:
    def __init__(self):
        self.notes = []
        self.last_id = 1

    def all_notes(self):
        self.notes.sort(key=lambda el: el.last_modified_at, reverse=True)

        return self.notes

    def find_notes(self, search):
        found_notes = []

        for note in self.notes:
            if search in note.note_text or search in note.tags:
                found_notes.append(note)

        if len(found_notes) == 0:
            raise NoteNotFound

        return found_notes

    def create_note(self, note_text, tags):
        if note_text == 'Python sucks!':
            raise BadNoteText

        note = Note(self.last_id, note_text, tags)

        self.last_id += 1
        self.notes.append(note)

    def update_note(self, id, note_text, tags):
        found_note = None

        for note in self.notes:
            if note.id == id:
                found_note = note

        if not found_note:
            raise NoteNotFound

        found_note.note_text = note_text
        found_note.tags = tags
        found_note.last_modified_at = datetime.datetime.now()


# A Note entity
class Note:
    def __init__(self, id, note_text, tags):
        self.id = id
        self.note_text = note_text
        self.tags = tags
        self.date = datetime.date.today()
        self.last_modified_at = datetime.datetime.now()


# Custom Exception classes
class NoteNotFound(Exception):
    pass


class BadNoteText(Exception):
    pass


# A NoteBook class to handle interaction with user and input/output
class NoteBook:
    def __init__(self):
        self.noteRepository = NoteRepository()

    def menu(self):
        print(''.join(80 * ["="]))
        print(f""" 
        Notebook Menu:
        1. Show all Notes
        2. Search Notes
        3. Add Note 
        4. Modify Note 
        5. Quit 
        """)

    def list(self, notes=None):
        if not notes:
            notes = self.noteRepository.all_notes()
        for note in notes:
            output = f"""Note id: {note.id}
Note tags: {note.tags}
Note text: {note.note_text}"""
            print(output)

    def search(self):
        search = input('Search for:')

        try:
            found_notes = self.noteRepository.find_notes(search)
        except NoteNotFound:
            print('No notes found!')
        else:
            self.list(found_notes)

    def add(self):
        note_text = input('Enter note text:')
        tags = input('Enter tags:')

        try:
            self.noteRepository.create_note(note_text, tags)
        except BadNoteText:
            print('You are not allowed to make such notes!')
        else:
            print("Your note has been added.")

    def update(self):
        id = int(input("Enter a note id: "))
        note_text = input("Enter new note text: ")
        tags = input("Enter new tags: ")

        try:
            self.noteRepository.update_note(id, note_text, tags)
            print('Note has been successfully updated')
        except NoteNotFound:
            print(f'There is no note with id {id}')

    def quit(self):
        print("Thank you for using your Notebook today.")

        sys.exit(0)


def main():
    notebook = NoteBook()

    while True:
        notebook.menu()

        choice = input('Enter an option: ')

        action = None
        match choice:
            case '1':
                action = 'list'
            case '2':
                action = 'search'
            case '3':
                action = 'add'
            case '4':
                action = 'update'
            case '5':
                action = 'quit'
            case _:
                print(f"{choice} is not a valid choice")
        if action:
            result = getattr(notebook, action)
            result()


if __name__ == "__main__":
    main()
