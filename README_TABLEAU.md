# Tableau Sales Analytics System

A production-ready sales analytics API optimized for Tableau Web Data Connector with comprehensive data visualization capabilities.

## 🎯 **Tableau-Optimized Features**

### **📊 Data Structure**
- **2,000+ orders** with realistic business data
- **500 unique customers** with segmentation
- **200 unique products** across 3 categories
- **5 geographic regions** for spatial analysis
- **2 years of historical data** for trend analysis

### **🔗 Tableau Connection Methods**

#### **Method 1: Web Data Connector (Recommended)**
1. **Tableau Desktop** → Connect → To a Server → More → Web Data Connector
2. **URL**: `https://sales-analytics-system-4ng8.onrender.com/tableau_wdc.html`
3. **Click** "Connect Sales Data to Tableau"
4. **Build** your dashboards with live data

#### **Method 2: CSV Export (Quick Start)**
- **Orders**: `/tableau/orders` - Complete order dataset
- **Customers**: `/tableau/customers` - Customer dimension
- **Products**: `/tableau/products` - Product catalog
- **KPIs**: `/tableau/kpi` - Pre-calculated metrics

### **📈 Available Data Fields**

#### **Orders Table**
| Field | Type | Description |
|-------|------|-------------|
| Order ID | String | Unique order identifier |
| Order Date | Date | Order placement date |
| Ship Date | Date | Shipping date |
| Customer ID | String | Customer identifier |
| Customer Name | String | Customer name |
| Segment | String | Customer segment (Consumer/Corporate/Home Office) |
| Product ID | String | Product identifier |
| Product Name | String | Product description |
| Category | String | Product category (Technology/Furniture/Office Supplies) |
| Sub-Category | String | Product sub-category |
| Region | String | Geographic region |
| State | String | State/Province |
| Country | String | Country |
| Postal Code | String | Postal code |
| Sales | Float | Order value ($)
| Quantity | Integer | Units ordered |
| Discount | Float | Discount percentage |
| Profit | Float | Order profit ($)
| Shipping Cost | Float | Shipping charges ($)

#### **Customers Table**
| Field | Type | Description |
|-------|------|-------------|
| Customer ID | String | Unique customer identifier |
| Customer Name | String | Customer name |
| Segment | String | Customer segment |
| City | String | Customer city |
| State | String | Customer state |
| Country | String | Customer country |
| Postal Code | String | Customer postal code |
| Region | String | Customer region |

#### **Products Table**
| Field | Type | Description |
|-------|------|-------------|
| Product ID | String | Unique product identifier |
| Product Name | String | Product name |
| Category | String | Product category |
| Sub-Category | String | Product sub-category |

## 🚀 **Quick Start with Tableau**

### **Step 1: Connect to Data**
```bash
# Web Data Connector URL
https://sales-analytics-system-4ng8.onrender.com/tableau_wdc.html

# Direct CSV Downloads
https://sales-analytics-system-4ng8.onrender.com/tableau/orders
https://sales-analytics-system-4ng8.onrender.com/tableau/kpi
```

### **Step 2: Build Your Dashboard**

#### **Essential Visualizations**
1. **KPI Cards**
   - Total Sales: `SUM([Sales])`
   - Total Profit: `SUM([Profit])`
   - Order Count: `COUNT([Order ID])`
   - Avg Order Value: `AVG([Sales])`

2. **Regional Analysis**
   - Sales by Region: Bar chart with Region on Rows, SUM(Sales) on Columns
   - Profit by Region: Map visualization with Region and Profit

3. **Product Performance**
   - Sales by Category: Pie chart with Category and SUM(Sales)
   - Top Products: Bar chart with Product Name and SUM(Sales)

4. **Customer Segmentation**
   - Sales by Segment: Donut chart with Segment and SUM(Sales)
   - Customer Distribution: Treemap with Customer Name and SUM(Sales)

5. **Time Series Analysis**
   - Sales Trend: Line chart with Order Date and SUM(Sales)
   - Monthly Comparison: Area chart with Month and SUM(Sales)

#### **Calculated Fields**
```tableau
// Profit Margin
[Profit] / [Sales]

// Profitable Orders
IF [Profit] > 0 THEN "Profitable" ELSE "Not Profitable" END

// High Value Orders
IF [Sales] > 500 THEN "High Value" ELSE "Standard" END

// Order Size Category
IF [Quantity] <= 3 THEN "Small"
ELSEIF [Quantity] <= 7 THEN "Medium"
ELSE "Large" END
```

### **Step 3: Create Dashboard Layout**

#### **Recommended Layout**
```
┌─────────────────┬─────────────────┬─────────────────┐
│   Total Sales    │   Total Profit  │   Order Count   │
│   $2,145,678    │    $432,109     │     2,000       │
└─────────────────┴─────────────────┴─────────────────┘
┌─────────────────────────────────────┬─────────────────┐
│          Sales by Region            │   Sales Trend    │
│        [Bar Chart]                  │   [Line Chart]  │
└─────────────────────────────────────┴─────────────────┘
┌─────────────────────────────────────┬─────────────────┐
│        Product Performance          │ Customer Segments│
│        [Pie Chart]                  │   [Donut Chart] │
└─────────────────────────────────────┴─────────────────┘
```

## 📱 **Mobile & Web Integration**

### **Tableau Cloud/Server**
1. **Publish** your workbook to Tableau Cloud
2. **Set refresh schedule** for live data updates
3. **Share** with stakeholders via web browser
4. **Mobile access** through Tableau Mobile app

### **Embedding Options**
- **Tableau Public**: Free public dashboards
- **Tableau Online**: Professional cloud hosting
- **Tableau Server**: On-premise deployment

## 🔧 **API Endpoints Reference**

### **Core Endpoints**
| Endpoint | Method | Description | Format |
|----------|--------|-------------|--------|
| `/health` | GET | API status check | JSON |
| `/tableau/orders` | GET | Complete orders data | CSV |
| `/tableau/customers` | GET | Customer dimension | CSV |
| `/tableau/products` | GET | Product catalog | CSV |
| `/tableau/kpi` | GET | KPI summary data | CSV |
| `/tableau/orders/json` | GET | Orders for WDC | JSON |
| `/tableau/schema` | GET | Data schema for WDC | JSON |

### **Live API URL**
```
https://sales-analytics-system-4ng8.onrender.com
```

## 🎨 **Dashboard Design Tips**

### **Color Schemes**
- **Sales**: Blue (#1e6ba8)
- **Profit**: Green (#28a745)
- **Loss**: Red (#dc3545)
- **Regions**: Multi-color palette

### **Chart Types**
- **KPIs**: Big number cards
- **Comparisons**: Bar charts
- **Trends**: Line charts
- **Composition**: Pie/donut charts
- **Distribution**: Histograms
- **Relationships**: Scatter plots

### **Best Practices**
1. **Use consistent color schemes**
2. **Add clear labels and titles**
3. **Include tooltips with details**
4. **Use appropriate chart types**
5. **Enable filters for interactivity**

## 🔄 **Data Refresh & Maintenance**

### **Automatic Updates**
- **Web Data Connector**: Refresh in Tableau
- **CSV Files**: Re-download latest data
- **API**: Always serves latest data

### **Performance Tips**
- **Extract data** for better performance
- **Set appropriate refresh intervals**
- **Use filters** to limit data size
- **Optimize calculated fields**

## 🌟 **Resume Description**

> **Tableau Sales Analytics System (Python, FastAPI, SQLite, Tableau)**
> 
> Built production-ready sales analytics API optimized for Tableau Web Data Connector, serving 2,000+ orders with comprehensive business metrics. Designed star schema database with customer segmentation, product categorization, and regional analysis. Created interactive Tableau dashboards with real-time KPI tracking, trend analysis, and geographic visualization. Implemented automated data pipeline with CSV exports and JSON endpoints for seamless Tableau integration.

## 📞 **Support & Documentation**

- **API Documentation**: Available at `/docs` endpoint
- **Web Data Connector**: `/tableau_wdc.html`
- **Health Check**: `/health`
- **Live Demo**: `https://sales-analytics-system-4ng8.onrender.com`

---

## 🎯 **Perfect for:**
- **Tableau Desktop** users
- **Business analysts** and data professionals
- **Sales teams** needing real-time insights
- **Executive dashboards** and reporting
- **Data visualization** portfolios

**🌟 Your Tableau-optimized sales analytics system is ready for professional dashboard creation!**