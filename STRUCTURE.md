# Project structure for Python discord bots

```txt
bot-project-name/
└───app/
│   └───models/
│   └───helpers/
│   │   config.py
│   │   db.py
│   │   errors.py
│   │   text.py
│   │   .env
│   └   app.py
│    
└───Dockerfile
```

## app/models : class models (optional)

Contains files for class models of objects used by the application.

## app/config.py : config file

This file acts as the central configuration file that will be used by the rest of the Python files.  
It includes the initialized Discord bot client, database URI, API keys, application configurables, ...

## app/helpers/ : helper modules

This file contains helper modules that can be used by `app.py` or `db.py`.  
For example, a modules for encryption and decryption, another module for password generation, ...

## app/db.py : database handlers

This file will cover interactions with the database (CRUD operations).

## app/errors.py : errors and exceptions

This file defines custom exceptions and error handlers.

## app/.env : environment variables

This file contains environment variables (discord bot token, configurables, ...)

## app/text.py : help and description text

Contains help text for each command in app/app.py, and some more description text

## app/app.py : main application

This is the main application file, it contains all the logic of the app (commands, events, ...)

## Dockerfile : for docker deployment

This file is used for docker deployment of the bot.
