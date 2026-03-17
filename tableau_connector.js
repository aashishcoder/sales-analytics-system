// tableau_connector.js
(function() {
    // Create connector object
    var myConnector = tableau.makeConnector();

    // Define schema
    myConnector.getSchema = function(schemaCallback) {
        var cols = [
            { id: "order_id", alias: "Order ID", dataType: tableau.dataTypeEnum.string },
            { id: "order_date", alias: "Order Date", dataType: tableau.dataTypeEnum.date },
            { id: "customer_id", alias: "Customer ID", dataType: tableau.dataTypeEnum.string },
            { id: "product_id", alias: "Product ID", dataType: tableau.dataTypeEnum.string },
            { id: "sales", alias: "Sales", dataType: tableau.dataTypeEnum.float },
            { id: "profit", alias: "Profit", dataType: tableau.dataTypeEnum.float },
            { id: "quantity", alias: "Quantity", dataType: tableau.dataTypeEnum.integer },
            { id: "region", alias: "Region", dataType: tableau.dataTypeEnum.string }
        ];

        var tableSchema = {
            id: "sales_analytics",
            alias: "Sales Analytics",
            columns: cols
        };

        schemaCallback([tableSchema]);
    };

    // Download data
    myConnector.getData = function(table, doneCallback) {
        $.ajax({
            url: "https://sales-analytics-system-4ng8.onrender.com/sales",
            dataType: 'json',
            success: function(data) {
                var tableData = [];
                
                // Process data (assuming your API returns an array)
                if (Array.isArray(data)) {
                    data.forEach(function(order) {
                        tableData.push({
                            "order_id": order["Order ID"],
                            "order_date": order["Order Date"],
                            "customer_id": order["Customer ID"],
                            "product_id": order["Product ID"],
                            "sales": order.Sales,
                            "profit": order.Profit,
                            "quantity": order.Quantity,
                            "region": order.Region
                        });
                    });
                }

                table.appendRows(tableData);
                doneCallback();
            },
            error: function(err) {
                tableau.abortWithError(err);
            }
        });
    };

    tableau.registerConnector(myConnector);

    // Create event listeners for when user submits form
    $(document).ready(function() {
        $("#submitButton").click(function() {
            tableau.connectionName = "Sales Analytics API";
            tableau.submit();
        });
    });
})();
