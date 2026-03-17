# Tableau Sales Analytics System

A production-ready sales analytics API optimized specifically for Tableau Web Data Connector with comprehensive business intelligence capabilities.

## 🎯 **Tableau Integration**

### **🔗 Connect Methods**
- **Web Data Connector**: `https://sales-analytics-system-4ng8.onrender.com/tableau_wdc.html`
- **CSV Downloads**: Direct file downloads for quick import
- **JSON API**: For custom Tableau integrations

### **📊 Data Overview**
- **2,000+ orders** with realistic business metrics
- **500 customers** across 3 segments
- **200 products** in 3 categories  
- **5 regions** for geographic analysis
- **2 years** of historical data

## 🚀 **Quick Start**

### **Method 1: Web Data Connector (Recommended)**
1. **Tableau Desktop** → Connect → To a Server → More → Web Data Connector
2. **URL**: `https://sales-analytics-system-4ng8.onrender.com/tableau_wdc.html`
3. **Click** "Connect Sales Data to Tableau"
4. **Build** your dashboards

### **Method 2: CSV Import**
```bash
# Download data directly
https://sales-analytics-system-4ng8.onrender.com/tableau/orders
https://sales-analytics-system-4ng8.onrender.com/tableau/customers
https://sales-analytics-system-4ng8.onrender.com/tableau/products
https://sales-analytics-system-4ng8.onrender.com/tableau/kpi
```

## 📈 **Tableau Dashboard Examples**

### **Essential Visualizations**
```tableau
// Key Metrics
Total Sales: SUM([Sales])
Total Profit: SUM([Profit])  
Order Count: COUNT([Order ID])
Avg Order Value: AVG([Sales])

// Calculated Fields
Profit Margin: [Profit] / [Sales]
High Value Orders: IF [Sales] > 500 THEN "High" ELSE "Standard" END
```

### **Dashboard Layout**
- **KPI Cards**: Sales, Profit, Orders, AOV
- **Regional Analysis**: Sales by region bar chart
- **Product Performance**: Category pie chart
- **Customer Segments**: Segment donut chart
- **Time Series**: Sales trend line chart

## 🔧 **API Endpoints**

| Endpoint | Description | Format |
|----------|-------------|--------|
| `/health` | API status | JSON |
| `/tableau/orders` | Complete orders data | CSV |
| `/tableau/customers` | Customer dimension | CSV |
| `/tableau/products` | Product catalog | CSV |
| `/tableau/kpi` | KPI summary | CSV |
| `/tableau/orders/json` | Orders for WDC | JSON |

## 🌐 **Live Demo**
- **API**: https://sales-analytics-system-4ng8.onrender.com
- **Web Data Connector**: https://sales-analytics-system-4ng8.onrender.com/tableau_wdc.html
- **Health Check**: https://sales-analytics-system-4ng8.onrender.com/health

## 📱 **Deployment**
- **Platform**: Render Cloud
- **Database**: SQLite (optimized for Tableau)
- **Framework**: FastAPI with CORS support
- **Auto-refresh**: Real-time data updates

## 🎨 **Tableau Features**
- **Star schema** optimized for Tableau
- **Proper data types** for all fields
- **Calculated fields** ready to use
- **Geographic data** for maps
- **Time series** for trend analysis

## 📞 **Documentation**
- **Complete Guide**: See `README_TABLEAU.md`
- **API Docs**: Available at `/docs` endpoint
- **Web Data Connector**: Interactive setup page

---

## 🌟 **Resume Achievement**

> Built production-ready Tableau sales analytics system with Web Data Connector integration, serving comprehensive business intelligence with 2,000+ orders, customer segmentation, and real-time KPI tracking. Designed optimized database schema for Tableau performance and created interactive dashboards with regional analysis and trend visualization.

**🎯 Perfect for Tableau professionals, business analysts, and data visualization portfolios!**