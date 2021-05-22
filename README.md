# Astro bot : a discord password manager

## How to run

### Option 1 : directly on your machine

1. Install python3 and pip.

2. Install the package dependencies :  

```bash
python -m pip install -r requirements.txt
```

3. Copy `app/example.env` to `app/.env` :  

```bash
cp app/example.env app/.env
```

4. Put your discord token in `app/.env`.

5. Run the bot :  

```bash
python app/app.py
```

### Option 2 : using docker (not working)

**Note :** The docker method is not working, a fix is in the works

1. Install docker and docker-compose.

2. Copy `app/example.env` to `app/.env` :  

```bash
cp app/example.env app/.env
```

3. Put your discord token in `app/.env`.

4. Run `docker-compose up -d --build`.

## Project structure

Check the structure of the project [here](./STRUCTURE.md)

## Contribution

Check the contribution guidelines [here](./CONTRIBUTING.md)
