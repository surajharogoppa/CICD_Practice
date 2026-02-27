# Angular + Flask CI/CD on Render

## Architecture

```
Browser
  │
  ├──▶ Angular App (Render Service 1) → yourapp.onrender.com
  │         │ HTTP calls
  └──▶ Flask API (Render Service 2) → yourapi.onrender.com
```

## Project Structure

```
angular-flask-cicd/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       └── test_app.py
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts
│   │   │   ├── app.component.html
│   │   │   ├── app.component.css
│   │   │   └── services/
│   │   │       └── api.service.ts
│   │   ├── environments/
│   │   │   ├── environment.ts        ← local dev URL
│   │   │   └── environment.prod.ts   ← Render API URL
│   │   ├── main.ts
│   │   ├── index.html
│   │   └── styles.css
│   ├── angular.json
│   ├── tsconfig.json
│   ├── package.json
│   ├── nginx.conf
│   └── Dockerfile
└── .github/
    └── workflows/
        └── ci-cd.yml
```

---

## Setup Steps

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "init: angular + flask cicd"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2 — Deploy Backend on Render

1. Go to render.com → New → Web Service
2. Connect your GitHub repo
3. Set **Root Directory** to `backend`
4. Set **Environment** to Docker
5. Create service → copy the **Deploy Hook URL** from Settings

### Step 3 — Deploy Frontend on Render

1. Go to render.com → New → Web Service
2. Connect same GitHub repo
3. Set **Root Directory** to `frontend`
4. Set **Environment** to Docker
5. Create service → copy the **Deploy Hook URL** from Settings

### Step 4 — Update Frontend API URL

In `frontend/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://YOUR-BACKEND.onrender.com'  // ← paste your backend URL here
};
```

### Step 5 — Add GitHub Secrets

Go to GitHub repo → Settings → Secrets → Actions:

| Secret | Value |
|---|---|
| `RENDER_BACKEND_DEPLOY_HOOK` | Deploy hook URL from backend Render service |
| `RENDER_FRONTEND_DEPLOY_HOOK` | Deploy hook URL from frontend Render service |

### Step 6 — Push and Watch Pipeline Run

```bash
git add .
git commit -m "feat: add render deploy hooks"
git push origin main
```

---

## Run Locally

```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py        # runs on http://localhost:5000

# Frontend (new terminal)
cd frontend
npm install
ng serve             # runs on http://localhost:4200
```

---

## CI/CD Pipeline Flow

```
git push to main
      │
      ├── test-backend (pytest)
      │        │ pass
      │        ▼
      │   deploy-backend → GHCR → Render API
      │
      └── test-frontend (ng build)
               │ pass
               ▼
          deploy-frontend → GHCR → Render Angular App
```

Backend and frontend pipelines run in parallel — independent of each other.

---

## GitHub Secrets Needed

| Secret | Purpose |
|---|---|
| `RENDER_BACKEND_DEPLOY_HOOK` | Triggers backend redeploy |
| `RENDER_FRONTEND_DEPLOY_HOOK` | Triggers frontend redeploy |
| `GITHUB_TOKEN` | Auto-generated, push to GHCR (no setup needed) |
