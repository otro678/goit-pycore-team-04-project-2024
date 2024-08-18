from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='mason_app',
    version='1.0.0',
    description='A Python application for managing an address book and notes (and dominating the world).',
    author='Serhii Kozachenko',
    author_email='serhii.kozachenko.92@gmail.com',
    packages=find_packages(),
    py_modules=['main', 'new_main', 'commands', 'address_book', 'notes_book', 'record', 'note', 'serialization', 'field', 'views.View', 'views.TableView', 'views.TextView', 'views.NotesBookView', 'views.AddressBookView'],
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'mason_app=new_main:main',
        ],
    },
)
