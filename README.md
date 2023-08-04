cd client
npm install
npm install --legacy-peer-deps
json-server --watch db.json --port 8000 --routes routes.json
json-server --watch dbb.json --port 5000
json-server --watch dbbb.json --port 4000
