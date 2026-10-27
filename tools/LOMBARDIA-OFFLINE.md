# Lombardia offline — pacchetto sperimentale

Questo workflow GitHub Actions genera un file PMTiles della Lombardia senza utilizzare il computer dell'utente.

1. Apri **Actions → Prepara mappa offline Lombardia → Run workflow**.
2. Lascia il livello di zoom **12** per la prima prova e indica un build ufficiale disponibile da https://maps.protomaps.com/builds.
3. Scarica l'**artifact** risultante dalla pagina del workflow.
4. Estrai lo ZIP e importa `lombardia.pmtiles` in **Moto-NAV TEST → Mappe offline**.

**Limiti:** questo è solo un test di produzione e importazione del pacchetto. Moto-NAV non renderizza ancora i PMTiles e l'archivio generato non è disponibile direttamente dal pulsante di download. La bounding box include una fascia di territorio esterna alla Lombardia. Zoom 12 non è adatto alla navigazione stradale dettagliata. Per la distribuzione reale serve uno storage HTTPS con CORS, supporto ai Range Requests e gestione dei costi di trasferimento.

Dati © OpenStreetMap contributors, ODbL. Rispettare le condizioni di utilizzo dei dataset Protomaps e la relativa attribuzione.
