// Tableau Sales Analytics Web Data Connector
(function() {
    var myConnector = tableau.makeConnector();

    // Define the schema for Tableau
    myConnector.getSchema = function(schemaCallback) {
        var cols = [
            { id: "Order ID", alias: "Order ID", dataType: tableau.dataTypeEnum.string },
            { id: "Order Date", alias: "Order Date", dataType: tableau.dataTypeEnum.date },
            { id: "Ship Date", alias: "Ship Date", dataType: tableau.dataTypeEnum.date },
            { id: "Customer ID", alias: "Customer ID", dataType: tableau.dataTypeEnum.string },
            { id: "Customer Name", alias: "Customer Name", dataType: tableau.dataTypeEnum.string },
            { id: "Segment", alias: "Segment", dataType: tableau.dataTypeEnum.string },
            { id: "Product ID", alias: "Product ID", dataType: tableau.dataTypeEnum.string },
            { id: "Product Name", alias: "Product Name", dataType: tableau.dataTypeEnum.string },
            { id: "Category", alias: "Category", dataType: tableau.dataTypeEnum.string },
            { id: "Sub-Category", alias: "Sub-Category", dataType: tableau.dataTypeEnum.string },
            { id: "Region", alias: "Region", dataType: tableau.dataTypeEnum.string },
            { id: "State", alias: "State", dataType: tableau.dataTypeEnum.string },
            { id: "Country", alias: "Country", dataType: tableau.dataTypeEnum.string },
            { id: "Postal Code", alias: "Postal Code", dataType: tableau.dataTypeEnum.string },
            { id: "Sales", alias: "Sales", dataType: tableau.dataTypeEnum.float },
            { id: "Quantity", alias: "Quantity", dataType: tableau.dataTypeEnum.integer },
            { id: "Discount", alias: "Discount", dataType: tableau.dataTypeEnum.float },
            { id: "Profit", alias: "Profit", dataType: tableau.dataTypeEnum.float },
            { id: "Shipping Cost", alias: "Shipping Cost", dataType: tableau.dataTypeEnum.float }
        ];

        var tableSchema = {
            id: "sales_analytics",
            alias: "Sales Analytics Data",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download data from API
    myConnector.getData = function(table, doneCallback) {
        var apiURL = window.location.origin + "/tableau/orders/json";
        
        $.ajax({
            url: apiURL,
            dataType: 'json',
            success: function(response) {
                var tableData = [];
                var data = response.data || [];
                
                // Transform data for Tableau
                data.forEach(function(order) {
                    tableData.push({
                        "Order ID": order["Order ID"],
                        "Order Date": order["Order Date"],
                        "Ship Date": order["Ship Date"],
                        "Customer ID": order["Customer ID"],
                        "Customer Name": order["Customer Name"],
                        "Segment": order["Segment"],
                        "Product ID": order["Product ID"],
                        "Product Name": order["Product Name"],
                        "Category": order["Category"],
                        "Sub-Category": order["Sub-Category"],
                        "Region": order["Region"],
                        "State": order["State"],
                        "Country": order["Country"],
                        "Postal Code": order["Postal Code"],
                        "Sales": parseFloat(order.Sales),
                        "Quantity": parseInt(order.Quantity),
                        "Discount": parseFloat(order.Discount),
                        "Profit": parseFloat(order.Profit),
                        "Shipping Cost": parseFloat(order["Shipping Cost"])
                    });
                });

                table.appendRows(tableData);
                doneCallback();
            },
            error: function(xhr, textStatus, errorThrown) {
                tableau.abortWithError("Error connecting to API: " + errorThrown);
            }
        });
    };

    tableau.registerConnector(myConnector);

    // Initialize the connector
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Tableau Sales Analytics API";
            tableau.submit();
        });

        // Show connection status
        $.ajax({
            url: window.location.origin + "/health",
            success: function(data) {
                $("#status").text("Connected to API - " + data.tables.orders + " orders available").css("color", "green");
            },
            error: function() {
                $("#status").text("API connection failed").css("color", "red");
            }
        });
    });
})();