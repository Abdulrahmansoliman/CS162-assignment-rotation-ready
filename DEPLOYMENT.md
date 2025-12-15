# 🚀 Deployment Guide - Rotation Ready

This guide walks you through deploying Rotation Ready using **Render** (backend) and **Vercel** (frontend).

## Prerequisites

- GitHub account with the repo pushed
- [Render](https://render.com) account (free)
- [Vercel](https://vercel.com) account (free)
- Gmail account with App Password for emails

---

## Part 1: Deploy Backend to Render

### Option A: One-Click Deploy (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Render will detect `render.yaml` and create:
   - Web Service (Flask API)
   - PostgreSQL Database

### Option B: Manual Setup

1. **Create PostgreSQL Database**
   - Render Dashboard → New → PostgreSQL
   - Name: `rotation-ready-db`
   - Plan: Free
   - Copy the **Internal Database URL**

2. **Create Web Service**
   - Render Dashboard → New → Web Service
   - Connect GitHub repo
   - Configure:
     - **Name**: `rotation-ready-api`
     - **Root Directory**: `backend`
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 "app:create_app('production')"`

3. **Set Environment Variables** (in Render dashboard):

   | Variable | Value |
   |----------|-------|
   | `FLASK_ENV` | `production` |
   | `SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
   | `JWT_SECRET_KEY` | Generate: `python -c "import secrets; print(secrets.token_hex(32))"` |
   | `DATABASE_URL` | (auto-filled if using Blueprint) |
   | `CORS_ORIGINS` | Your Vercel URL (add after frontend deploy) |
   | `MAIL_ENABLED` | `true` |
   | `MAIL_SERVER` | `smtp.gmail.com` |
   | `MAIL_PORT` | `587` |
   | `MAIL_USE_TLS` | `true` |
   | `MAIL_USERNAME` | Your Gmail address |
   | `MAIL_PASSWORD` | Your Gmail App Password |
   | `MAIL_DEFAULT_SENDER` | Your Gmail address |

4. **Initialize Database**
   
   The database is automatically created and seeded during the build process.
   
   If you need to re-seed manually, use Render Shell:
   ```bash
   cd backend
   python seed/seed.py
   ```

---

## Part 2: Deploy Frontend to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)

2. Click **Add New** → **Project**

3. Import your GitHub repository

4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. **Set Environment Variables**:

   | Variable | Value |
   |----------|-------|
   | `VITE_API_URL` | Your Render backend URL (e.g., `https://rotation-ready-api.onrender.com`) |

6. Click **Deploy**

---

## Part 3: Connect Frontend & Backend

### Update CORS on Render

After deploying frontend, go back to Render and update:

```
CORS_ORIGINS=https://your-app.vercel.app
```

If you have multiple domains:
```
CORS_ORIGINS=https://your-app.vercel.app,https://custom-domain.com
```

---

## Post-Deployment Checklist

- [ ] Backend is running on Render
- [ ] Database is connected and seeded
- [ ] Frontend is deployed on Vercel
- [ ] `VITE_API_URL` points to Render backend
- [ ] `CORS_ORIGINS` includes Vercel frontend URL
- [ ] Email sending works (test signup)
- [ ] Login/signup flow works end-to-end

---

## Troubleshooting

### "CORS error" in browser console
- Check `CORS_ORIGINS` on Render includes your Vercel URL
- Make sure there's no trailing slash in the URL

### "Internal Server Error" on Render
- Check Render logs for Python errors
- Verify DATABASE_URL is set correctly
- Run database migrations if needed

### Emails not sending
- Verify `MAIL_ENABLED=true`
- Check Gmail App Password is correct
- Look for email errors in Render logs

### Database not seeded
- Connect to Render Shell and run:
  ```bash
  cd backend
  python seed/seed.py
  ```

---

## Custom Domain (Optional)

### Vercel (Frontend)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### Render (Backend)
1. Go to Service Settings → Custom Domains
2. Add your API subdomain (e.g., `api.yourdomain.com`)
3. Update DNS records

---

## Costs

| Service | Free Tier | Paid |
|---------|-----------|------|
| Render Web Service | ✅ Free (spins down after inactivity) | $7/mo (always on) |
| Render PostgreSQL | ✅ Free for 90 days | $7/mo |
| Vercel | ✅ Free (hobby) | $20/mo (pro) |

**Note**: Free tier services may have cold starts (first request takes ~30s after inactivity).

---

## Quick Reference

| Resource | URL |
|----------|-----|
| Backend API | `https://rotation-ready-api.onrender.com` |
| Frontend | `https://rotation-ready.vercel.app` |
| Render Dashboard | https://dashboard.render.com |
| Vercel Dashboard | https://vercel.com/dashboard |
