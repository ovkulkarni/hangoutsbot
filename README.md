# HangoutsBot
This is a bot made to interface with Google Hangouts. It uses the [`hangups`](https://github.com/tdryer/hangups) library to connect to hangouts.
**NOTE: This project requires `python3`**

## Setting up
The following instructions will help you get started:

Clone the github repository to your computer:
`git clone https://github.com/ovkulkarni/hangoutsbot.git`

Install all requirements:
```bash
cd hangoutsbot/
pip install -r requirements.txt
```

Create needed directories:
```
mkdir private logs
```

Create database tables:
```
./manage.py create_tables
```

Copy `settings/secret.sample` to `settings/secret.py`:
```
cp settings/secret.{sample,py}
```

Get Bot's ID and set in `settings/secret.py`:
```
./manage.py get_bot_id
```

Modify any other relevant information in `settings/secret.py` to your liking.

Run the bot:
```
./manage.py run
```
**NOTE: Make sure to run the bot before adding it to a conversation. This way, it can correctly populate the database with Users.**

Accessing the python shell with context:
```
./manage.py shell
```

To set your user as an admin, enter a shell and do the following:
```
>>> user = User.get(first_name="<enter your name here>")
>>> user.is_admin = True
>>> user.save()
```