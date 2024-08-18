# App

The app made by Illumina.py team
It's a simple CLI contacts & notes storage app with editing and search functions.

## Installation

You'll need conda and pip to use the app. You can use any other virtual env of your liking, but instructions are for conda :)

Open a terminal from the working folder of a project and execute following commands:
```bash
conda create -n illuminapy python=3.12

conda activate illuminapy

pip install -r requirements.txt

python main.py
```

Or, if you want to use it as a standalone app from anywhere in your system you should do the following:
```bash
conda create -n illuminapy python=3.12

conda activate illuminapy

pip install .

```

After that, open a Terminal/PowerShell app from any folder and run following commands:
```bash
conda activate illuminapy

mason_app
```

## Usage

List of available commands:

- `all` - prints all Contacts and Notes
- `all-contacts` - prints all Contacts
- `all-notes` - prints all Notes
- `search-contacts <query string> [field:<FieldName>] [sort:<FieldName>[:direction]]` - performs search in Contacts; if `field` parameter is set - search is done only by this field; if `sort` param is set - search results are sorted by this field
- `search-notes <query string> [field:FieldName] [sort:FieldName[:direction]]` - performs search in Notes; if `field` parameter is set - search is done only by this field; if `sort` param is set - search results are sorted by this field
- `add-contact <Name>` - creates new Contact initialized with Name field
- `add-note <Title>` - creates new Note initialized with Title field
- `edit-contact <Name> [field:FieldName]` - searches for Contact by Name and starts fields edit procedure; if `field` param is passed - allows only to edit this field
- `edit-note <Title> [field:FieldName]` - searches for Note by Title and starts fields edit procedure; if `field` param is passed - allows only to edit this field
- `delete-contact <Name>` - deletes Contact found by Name
- `delete-note <Title>` - deletes Note found by Title
- `show-birthdays <days>` - shows Contacts whose Birthdays are happening in the closest `days` in the future
- `close`, `exit`, `quit`, `stop`, `Ctrl+C`, `Ctrl+D` - saves current Contacts/Notes and stops the Bot
- `hello` - prints greeting message
- `help` - prints all available commands list

## Contributing

Illumina.py team:

@otro678 - Serhii K

@cryptophobic - Dmytro U

@S3lfik - Eduard K

@prymakov - Anton P

@MaksDeGreez - Maks S

## License

[MIT](https://choosealicense.com/licenses/mit/)
