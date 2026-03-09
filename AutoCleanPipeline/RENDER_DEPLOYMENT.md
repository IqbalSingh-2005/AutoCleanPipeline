# Render.com Deployment Guide for AutoClean Pipeline

## Prerequisites
- GitHub repository with your code pushed
- Render.com account

## Render.com Configuration

### 1. Create New Web Service
- Go to Render Dashboard
- Click **New +** → **Web Service**
- Connect your GitHub repository

### 2. Configuration Settings

**Basic Settings:**
- **Name:** autoclean-dashboard (or your preferred name)
- **Region:** Singapore (Southeast Asia)
- **Branch:** master
- **Root Directory:** `AutoCleanSet`
- **Runtime:** Python 3

**Build & Deploy:**
- **Build Command:**
  ```bash
  pip install -r ../requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
  ```

- **Start Command:**
  ```bash
  gunicorn AutoClean.wsgi:application
  ```

### 3. Environment Variables

Add these environment variables in Render dashboard:

| Key | Value | Description |
|-----|-------|-------------|
| `PYTHON_VERSION` | `3.11.0` | Python version |
| `DEBUG` | `False` | Turn off debug mode for production |
| `SECRET_KEY` | `your-secret-key-here` | Generate using command below |
| `ALLOWED_HOSTS` | `*.onrender.com,dashboard.sparksx.me,www.dashboard.sparksx.me` | Allowed hosts |

**Generate SECRET_KEY:**
Run this command locally in your terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copy the output and use it as your SECRET_KEY.

### 4. Custom Domain Setup (dashboard.sparksx.me)

**In Render Dashboard:**
1. Go to your web service
2. Click on **Settings**
3. Scroll to **Custom Domain**
4. Click **Add Custom Domain**
5. Enter: `dashboard.sparksx.me`
6. Render will provide DNS records

**In Your Domain Provider (e.g., Cloudflare, GoDaddy):**
Add these DNS records:
- **Type:** CNAME
- **Name:** dashboard (or @)
- **Value:** [your-app-name].onrender.com (provided by Render)
- **TTL:** Auto or 300

For www subdomain:
- **Type:** CNAME
- **Name:** www.dashboard
- **Value:** [your-app-name].onrender.com

### 5. Persistent Disk (Optional but Recommended)

For storing uploaded files and database:
1. Go to your web service
2. Click **Disks** in left sidebar
3. Click **Add Disk**
4. **Name:** autoclean-storage
5. **Mount Path:** `/opt/render/project/src/AutoCleanSet/media`
6. **Size:** 1 GB (free tier)

### 6. Deploy

1. Click **Create Web Service**
2. Render will automatically:
   - Install dependencies
   - Run collectstatic
   - Run migrations
   - Start gunicorn server
3. Monitor deployment logs
4. Once deployed, visit your URL

## Post-Deployment

### Test Your Deployment
1. Visit `https://[your-app-name].onrender.com`
2. Upload a test CSV file
3. Verify data cleaning and visualization works
4. Test download features (Excel, PDF)

### Custom Domain Activation
- After adding DNS records, wait 24-48 hours for propagation
- Render automatically provisions SSL certificate
- Access your app at `https://dashboard.sparksx.me`

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` ran successfully in build logs
- Check STATIC_ROOT is configured in settings.py
- Verify WhiteNoise middleware is enabled

### Application Errors
- Check Render logs: Click **Logs** in service dashboard
- Verify all environment variables are set correctly
- Ensure SECRET_KEY is properly generated

### Database Issues
- SQLite works for small deployments
- For production scale, consider PostgreSQL (Render provides free tier)

### Upload Files Lost After Restart
- Use Persistent Disk to store media files
- Mount disk to `/opt/render/project/src/AutoCleanSet/media`

## Important Notes

1. **Free Tier Limitations:**
   - Render free tier spins down after 15 minutes of inactivity
   - First request after spin down may take 30-60 seconds
   - Consider paid tier for production use

2. **Security:**
   - Never commit SECRET_KEY to Git
   - Always use environment variables for sensitive data
   - Keep DEBUG=False in production

3. **File Storage:**
   - Use persistent disk for uploaded files
   - Or consider cloud storage (AWS S3, Cloudflare R2)

4. **Database:**
   - SQLite works for testing
   - For production, migrate to PostgreSQL

## Maintenance

### Update Deployment
- Push changes to GitHub master branch
- Render auto-deploys on new commits

### Manual Redeploy
- Go to Render dashboard
- Click **Manual Deploy** → **Deploy latest commit**

### View Logs
- Click **Logs** in service dashboard
- Monitor real-time application logs

## Support Resources
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.1/howto/deployment/

---

**Deployment Checklist:**
- [ ] Code pushed to GitHub
- [ ] requirements.txt at repository root
- [ ] settings.py configured for production
- [ ] Environment variables added in Render
- [ ] SECRET_KEY generated and set
- [ ] Build and start commands configured
- [ ] Custom domain DNS records added
- [ ] Persistent disk configured (optional)
- [ ] First deployment successful
- [ ] Test file upload and visualization
- [ ] SSL certificate active
