1. Start backend (Christos + Nadiotis)
   - Open PowerShell:
       cd "%USERPROFILE%\Documents\learntwin_fullstack\backend"
       . .\.venv\Scripts\Activate.ps1
       $env:API_KEY = "devkey"
       python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   - Check: http://127.0.0.1:8000/docs

2. Send data and get recommendations (Nadiotis glue role)
   - New PowerShell:
       cd "%USERPROFILE%\Documents\hackathon_nov25_MVP"
       .\send_to_backend.ps1 -JsonPath .\sample_response.json

3. Optional UI
   - Use Swagger at http://127.0.0.1:8000/docs to call /health and /recommend interactively.
