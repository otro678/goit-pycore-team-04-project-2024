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
```python
hello # shows greeting message
all # shows all contacts and notes

add-contact [name] # starts contact adding
delete-contact [name] # deletes a specified contact

add-note [title] # starts note adding
delete-note [title] # deletes a specified note

# those commands let user to edit a specified field
edit-phone [name]
edit-email [name]
edit-address [name]
edit-bday [name]
edit-name [old-name] [new-name]

edit-contact [name] # multi-step contact editing, n skips the field and keeps it unchanged
edit-note [title] # multi-step note editing, n skips the field and keeps it unchanged

# search within all the fields
search-contacts [query] sort:[field]:[asc/desc] #sort parameter works for every search command including ones below
search-notes [query]

#search within a specified field
search-name [query] 
search-phone [query]
search-email [query]
search-address [query]
search-tag [query]
search-title [query]
search-body [query]

birthdays [days] (parameter is optional, defaults to 7 days) # shows the contacts who has birthday in [x] days
get-contacts-by-birthdate to:[dd.mm.yyyy] from:[dd.mm.yyyy] # searches contacts with birthdays within a specified range
```

## Contributing

Illumina.py team:

@otro678 - Serhii K

@cryptophobic - Dmytro U

@S3lfik - Eduard K

@prymakov - Anton P

@MaksDeGreez - Maks S

## License

[MIT](https://choosealicense.com/licenses/mit/)