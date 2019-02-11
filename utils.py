"""Utilities."""

from io import BytesIO
import locale
import os
import shutil

class FakeFile(BytesIO):
    """Fakes out a memory based object that can be opened and written to by the
    petl html generator."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self, *args, **kwargs):
        return self

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass


def get_html(table):
    """Extract the html from a petl table using a fake file."""

    temp_file = FakeFile()
    table.tohtml(temp_file)

    html = temp_file.getvalue().decode(locale.getpreferredencoding(False))
    temp_file.close()

    return html

def clear_directory(directory):
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        if item.startswith('.'):
            continue
        elif os.path.isfile(full_path):
            os.remove(os.path.join(full_path))
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)