# Running
## Development
### Backend FastAPI app
1. Copy content of app/.env.example to app/.env and change the secret key
2. Run `pip install -r app/requirements.txt`
3. Run `uvicorn.exe app.main:app --host 127.0.0.1 --port 8080 --reload` to start the FastAPI application
4. Visit auto generated documentations at [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
### Frontend SvelteKit app
1. Copy content of frontend/.env.example to frontend/.env
2. `cd` to frontend folder
3. Run `npm install`
4. Run `npm run dev` to start the SvelteKit application
5. Visit the application at [http://127.0.0.1:5173](http://127.0.0.1:5173)
## Production
1. Copy content of app/.env.example to app/.env and change the secret key
2. Copy content of frontend/.env.example to frontend/.env
3. Run `docker compose up -d` at project root
4. The FastAPI application will be exposed to port 8080 at [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs)
5. The SvelteKit application will be exposed to port 3000 at [http://127.0.0.1:3000](http://127.0.0.1:3000)