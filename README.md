# Astro bot : a discord password manager

## How to run

### Option 1 : directly on your machine

1. Install python3 and pip.

2. Install the package dependencies :  

```bash
python3 -m pip install discord python-dotenv bcrypt validators pycrypto
```

3. Change directory to `app/` :  

```bash
cd app
```

4. Copy `example.env` to `.env` :  

```bash
cp example.env .env
```

4. Put your discord token in `.env`.

5. Run the bot :  

```bash
python3 app.py
```

### Option 2 : using docker

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
