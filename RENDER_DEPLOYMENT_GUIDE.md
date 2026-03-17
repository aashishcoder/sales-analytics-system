# Render Deployment Guide for Sales Analytics System

## 🚀 Deploy to Render (Recommended)

### Step 1: Prepare GitHub Repository

```bash
# Initialize Git and commit
git add .
git commit -m "Initial commit: Sales Analytics System"

# Create GitHub repository
gh repo create sales-analytics-system --public --source=. --remote=origin --push
```

### Step 2: Deploy to Render

#### Method A: GitHub Integration (Easiest)
1. Go to [Render.com](https://render.com)
2. Sign up/login with GitHub
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub account
5. Select `sales-analytics-system` repository
6. Configure deployment settings:

**Build Settings:**
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Instance Type**: Free (to start)
- **Auto-Deploy**: Yes (on git push)
- **Health Check Path**: `/health`

#### Method B: Manual Configuration
1. **Repository**: `yourusername/sales-analytics-system`
2. **Root Directory**: `.` (leave empty)
3. **Runtime**: `Python 3`
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables (Optional)

Add these in Render dashboard:
- `PYTHON_VERSION`: `3.10`
- `PORT`: `10000` (Render's default)

### Step 4: Deploy and Test

1. Click **"Create Web Service"**
2. Wait for deployment (2-3 minutes)
3. Your app will be available at: `https://sales-analytics-system.onrender.com`

### Step 5: Test Your Live API

```bash
# Test health endpoint
curl https://sales-analytics-system.onrender.com/health

# Test KPI endpoint
curl https://sales-analytics-system.onrender.com/kpi

# View API documentation
# Open: https://sales-analytics-system.onrender.com/docs
```

## 🔧 Render Configuration Files

Your repository includes:

### `Procfile`
```
web: python -m uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### `Dockerfile`
- Optimized for Render deployment
- Runs ETL pipeline on startup
- Starts API server automatically

### `.gitignore`
- Excludes large data files
- Keeps repository clean

## 📊 Power BI Integration with Render

Once deployed:

1. **Power BI Desktop** → Get Data → Web
2. **URL**: `https://sales-analytics-system.onrender.com/sales`
3. **Headers**: None needed
4. **Transform** and create visualizations

## 🔄 Auto-Deployment

Render automatically:
- ✅ **Rebuilds** on every git push
- ✅ **Runs ETL pipeline** on startup
- ✅ **Starts API server**
- ✅ **Health checks** every minute

## 📱 Mobile Access

Your API will be accessible from:
- **Desktop**: Full browser experience
- **Mobile**: Responsive API endpoints
- **Tablet**: Optimized for touch

## 🎯 Production Features

### Automatic Scaling
- **Free Tier**: 750 hours/month
- **Starter Tier**: $7/month (more resources)
- **Standard Tier**: $25/month (better performance)

### Monitoring
- **Logs**: Available in Render dashboard
- **Metrics**: Response time, error rate
- **Health Checks**: Automatic monitoring

### Custom Domain (Optional)
1. **Render Dashboard** → Service → Settings
2. **Add Custom Domain**
3. **Update DNS** records
4. **SSL Certificate** auto-generated

## 🚀 Next Steps After Deployment

### 1. Update README
```markdown
### Live Demo
👉 **[API Documentation](https://sales-analytics-system.onrender.com/docs)**
👉 **[Health Check](https://sales-analytics-system.onrender.com/health)**
👉 **[KPI Data](https://sales-analytics-system.onrender.com/kpi)**
```

### 2. Connect Power BI
- Use your live Render URL
- Build dashboard with real data
- Publish to Power BI Service

### 3. Share Your Project
- **LinkedIn**: Post about your deployment
- **Portfolio**: Add live demo link
- **Resume**: Include production URL

### 4. Monitor Performance
- Check Render dashboard logs
- Monitor API response times
- Track usage analytics

## 🔍 Troubleshooting

### Common Issues

#### Build Fails
```bash
# Check logs in Render dashboard
# Common fix: Update requirements.txt
pip install --upgrade pip
```

#### API Not Responding
```bash
# Check health endpoint
curl https://your-app.onrender.com/health

# Check logs in Render dashboard
```

#### Database Issues
- ETL pipeline runs automatically on startup
- Database recreated on each deployment
- Data persistence: Consider PostgreSQL upgrade

### Performance Optimization

#### Free Tier Limits
- **750 hours/month** runtime
- **512MB RAM** limit
- **Sleeps after 15 minutes** inactivity

#### Upgrade Options
- **Starter ($7/month)**: Better performance
- **Standard ($25/month)**: Production ready
- **Pro ($50/month)**: High traffic

## 🎉 Success Metrics

Your deployment is successful when:
- ✅ **Health check** returns 200 OK
- ✅ **KPI endpoint** returns real data
- ✅ **API docs** load correctly
- ✅ **Power BI** can connect
- ✅ **Mobile** access works

---

## 🌟 Production Achievement

**🎯 You now have:**
- **Live API** deployed on cloud
- **Real data** from Kaggle Superstore
- **Production-ready** architecture
- **Resume-worthy** project
- **Shareable** live demo

**🚀 Your Sales Analytics System is now live and accessible worldwide!**
