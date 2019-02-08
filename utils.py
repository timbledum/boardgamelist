"""Utilities."""

from io import BytesIO

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

    html = temp_file.getvalue().decode('utf-8')
    temp_file.close()

    return html