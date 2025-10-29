# Deployment Guide - Congress Connect

## Option 1: Streamlit Community Cloud (Recommended - FREE)

### Prerequisites
- GitHub account
- This repository pushed to GitHub

### Steps

1. **Prepare Repository**
   - Ensure all files are committed and pushed to GitHub
   - Make sure repository is public
   - Verify `requirements.txt` is in root directory
   - Verify `app.py` is in root directory

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Sign in with GitHub

3. **Configure Deployment**
   - Repository: Select your `congress_liberation` repo
   - Branch: `main` (or your default branch)
   - Main file path: `app.py`
   - Click "Deploy"

4. **Wait for Deployment**
   - Initial deployment takes 2-5 minutes
   - Streamlit will install dependencies
   - Database will be initialized on first run

5. **Access Your App**
   - Your app will be live at: `https://[your-app-name]-[your-username].streamlit.app`
   - Share this URL with users!

### Important Notes

- **Database:** Will be recreated on each deploy. This is fine for MVP.
- **Updates:** Push to GitHub, app auto-redeploys
- **Logs:** Available in Streamlit Cloud dashboard
- **Cost:** FREE (unlimited for public repos)

### Custom Domain (Optional)

To use a custom domain:
1. Purchase domain (e.g., from Namecheap, $12/year)
2. In Streamlit settings, add custom domain
3. Update DNS records as instructed

---

## Option 2: Heroku (Alternative - FREE Tier Available)

### Prerequisites
- Heroku account
- Heroku CLI installed

### Additional Files Needed

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deploy
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

---

## Option 3: Railway (Alternative - FREE $5 Credit/Month)

### Steps

1. Visit [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `congress_liberation`
6. Railway auto-detects Python and deploys
7. Access via provided URL

---

## Option 4: Local Network Deployment

### For Local/University Network Access

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run on specific port:**
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

3. **Access:**
   - From same machine: http://localhost:8501
   - From network: http://[YOUR-IP]:8501

4. **Find your IP:**
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
```

---

## Testing Before Deployment

### Local Testing Checklist

- [ ] Database initializes successfully
- [ ] ZIP code search works
- [ ] Representative profiles display correctly
- [ ] Contact links work
- [ ] Funding information displays
- [ ] Browse page shows all reps
- [ ] Filters work properly
- [ ] Mobile responsive (test at different widths)
- [ ] All tabs functional

### Test Commands

```bash
# Initialize database
python utils/database.py

# Run app
streamlit run app.py

# Test at different screen sizes in browser:
# - Mobile: 375px width
# - Tablet: 768px width
# - Desktop: 1920px width
```

---

## Post-Deployment

### Monitoring

1. **Check Logs** (Streamlit Cloud)
   - Dashboard → Your App → Logs
   - Look for errors

2. **Test Functionality**
   - Test ZIP lookup
   - Test all links
   - Test on mobile device
   - Test filters

3. **Share**
   - Share URL on social media
   - Share with classmates/professor
   - Share with civic groups

### Updating Data

To update campaign funding after deployment:

1. Update CSV locally
2. Run `python utils/database.py`
3. Commit and push to GitHub
4. Streamlit Cloud will auto-redeploy

---

## Troubleshooting

### Common Issues

**"ModuleNotFoundError"**
- Check `requirements.txt` includes all dependencies
- Streamlit Cloud: Check deployment logs

**"Database not found"**
- Run `python utils/database.py` locally first
- Database is created automatically on Streamlit Cloud

**"Page not loading"**
- Check Streamlit Cloud deployment status
- Check browser console for errors
- Try incognito mode (clears cache)

**"ZIP lookup not working"**
- Expected behavior: Manual ZIP mapping for Florida only
- For full functionality, add Google Civic API key (see ADVANCED.md)

---

## Security Notes

### For Public Deployment

- ✅ No API keys in code (good)
- ✅ No personal data collected (good)
- ✅ SQLite database read-only for users (good)
- ⚠️ Consider adding rate limiting for production

### Environment Variables (If Adding APIs)

For Streamlit Cloud:
1. Dashboard → Your App → Settings → Secrets
2. Add secrets in TOML format:
```toml
GOOGLE_CIVIC_API_KEY = "your-key-here"
PROPUBLICA_API_KEY = "your-key-here"
```

3. Access in code:
```python
import streamlit as st
api_key = st.secrets["GOOGLE_CIVIC_API_KEY"]
```

---

## Performance Optimization

### For High Traffic

If you get > 1000 users/day:

1. **Caching**
   - Already implemented with `@st.cache_resource`
   - Database connection cached

2. **Database Optimization**
   - Indexes already created
   - Queries optimized

3. **Upgrade Hosting**
   - Streamlit Cloud scales automatically
   - Or migrate to dedicated server

---

## Cost Estimates

| Platform | Free Tier | Paid (if needed) |
|----------|-----------|------------------|
| **Streamlit Cloud** | Unlimited (public) | $99/mo (private) |
| **Heroku** | 550 hrs/mo | $7/mo |
| **Railway** | $5 credit/mo | Pay-as-you-go |
| **Domain** | - | $12/year |

**Recommended for Academic Project:** Streamlit Cloud (FREE + easiest)

---

## Going Live Checklist

Before sharing publicly:

- [ ] Test all features thoroughly
- [ ] Verify all links work
- [ ] Check mobile responsiveness
- [ ] Add "About" page information
- [ ] Update README with live URL
- [ ] Create backup of working code
- [ ] Monitor initial usage for bugs

---

## Support

For deployment issues:
- Streamlit Community: https://discuss.streamlit.io
- Streamlit Docs: https://docs.streamlit.io
- This project docs: See `docs/` folder

---

**Ready to deploy!** 🚀

Choose Streamlit Cloud for fastest, easiest, and free deployment.
