# Project structure for Python discord bots

```txt
bot-project-name/
└───app/
    └───models/
│   │   config.py
│   │   helpers.py
│   │   db.py
│   │   errors.py
│   │   help.py
│   │   .env
│   └   app.py
│    
└───Dockerfile
```

## app/models : class models (optional)

Contains files for class models of objects used by the application (example: User, Entry, ...).

## app/config.py : config file

This file acts as the central configuration file that will be used by the rest of the Python files.  
It includes the initialized Discord bot client, database URI, API keys, application configurables, ...

## app/helpers.py : helper methods

This file contains helper methods that can be used by `app.py` or `db.py`.  
For example, some methods to encrypt and decrypt the credentials.

## app/db.py : database handlers

This file will cover interactions with the database (CRUD operations).

## app/errors.py : errors and exception

This file defines custom exceptions.

## app/.env : environment variables

This file contains environment variables (discord bot token, configurables, ...)

## app/help.py : help text for each command

Contains help text for each command in app/app.py

## app/app.py : main application

This is the main application file, it contains all the logic of the app (commands, events, ...)

## Dockerfile : for docker deployment

This file is used for docker deployment of the bot.
