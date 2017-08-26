# README #

### Hva er dette? ###

Demo applikasjon som gjenskaper TFK sin ansatte app: http://apps.t-fk.no/ansatte

Den består av en backend og en frontend. Backend er skrevet i `Python` med `Django` som rammeverk
og bruker `Django Rest Framework` for api oppsett.
Frontend er skrevet i `Ember` og snakker med backend via AJAX kall.

Alle tjenester håndteres av `docker` og `docker-compose`, `docker-compose` tar seg å starte opp
alle tjenesten man trenger og binder dem sammen med bruk av `nginx` som reverse proxy.

Skripting gjøres via Fabric, feks. for første gangs oppsett og deployment.

### Oppsett ###

* Git clone dette repoet
* Gå inn in working copy
* kopier dist filene til lokale filer og modifiser
* start docker containere med docker-compose
* Importer data til databasen med Django kommandoen `import_data`


Første gangs oppsett krever at noen lokale filer lages, dette kan gjøres med:


```bash
fab setup
```

Eller manuelt med:

```bash
cp .env-dist .env
cp backend/settings/.env-dist backend/settings/.env
cp backend/settings/local-dist.py backend/settings/local.py
```

Bygg docker images med:

```bash
docker-compose build
```

For å starte alle tjenestene kjør:

```bash
docker-compose up
```

Applikasjonen er nå tilgjengelig via `WEB_PORT` som konfigurert

Importer data om ansatte ved å kjøre:

```bash
docker-compose run --rm backend python manage.py import_data ansatte.json
```

## Docker ##

Litt informasjon om docker imagene som er brukt.

### django ###

Docker image som er basert på Python men som starter Django applikasjonen via
`start-dev.sh` skriptet, dette skriptet sørger for å migrere databasen og vil håndtere feil
og prøver å restarte applikasjonen hvis dette skjer.

`entrypoint.sh` sørger for å vente på at databasen er klar før den fortsetter.

Det er også et oppsett for produksjon hvor `gunicorn` er brukt.

### nginx ###

Docker image basert på offisiell nginx men som integrerer `envplate`, dette
gjør det mulig å bruke environment variabler i konfigen.


### assets ###

Docker image basert på nodejs, som integrer yarn, watchman, bower, livereload
og nodemon.

yarn erstatter npm for installasjon av pakker, og nodemon brukes for å starte
og restarte ember serveren når hovedkonfigurasjon er endret. Dette gjør
utviklingsjobben en del enklere.

### postgres ### 

Offisielt image brukes men er konfigurert for lokalt utvikling.


### docker-compose ###

Fila docker-compose.yml brukes til lokal utvikling 


### Porter ###

Docker oppsettet eksponerer to porter (settes i `.env`), `WEB_PORT` er porten
for reverse proxy som er den man bruker til vanlig. `APP_PORT` er porten
direkte mot Django backend, trengs normalt ikke men kan brukes for 

Livereload er konfigurert slik at alt går igjennom `WEB_PORT`, dette gjør
det også enkelt å ta bruk tjenester som ngrok slik at man kan få hele
oppsettet gjennom et domene og SSL.

### API ###

API'et ligger i backend og leveres via pathen `/backend/api`, koden
for dette ligger i `backend/backend/api.py` og er laget i Django Rest Framework.