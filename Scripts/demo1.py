import streamlit as st
import mysql.connector
import pandas as pd

# MySQL database connection setup
def create_connection():
    return mysql.connector.connect(
        host="localhost",         # Replace with your host
        user="root",              # Replace with your MySQL username
        password="12345",         # Replace with your MySQL password
        database="retail_orders"  # Replace with your database name
    )

# Function to execute SQL query and return results
def execute_sql_query(query):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(query)  # Execute the actual query
        result = cursor.fetchall()  # Fetch all the results
        columns = cursor.description  # Get column names
        # Convert to a Pandas DataFrame
        df = pd.DataFrame(result, columns=[col[0] for col in columns])
        return df
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
    finally:
        cursor.close()
        conn.close()

# Multi-select options
selected_options = st.multiselect(
    "Select the queries to execute",
    [
        "1.Find top highest revenue generating products",
        "2.Find the Cities with the Highest Profit Margins",
        "3.Calculate the total discount given for each category",
        "4.Find the average sale price per product category",
        "5.Find the region with the highest average sale price",
        "6.Find the total profit per category",
        "7.Identify the Top Segments with the Highest Quantity of Orders",
        "8.Determine the average discount percentage given per region",
        "9.Find the product category with the highest total profit",
        "10.Calculate the Revenue Generated Per Year"
    ]
)

# Function to generate SQL queries based on selected options
def generate_query(option):
    if option == "1.Find top highest revenue generating products":
        return """
    SELECT p.category, SUM(o.quantity * o.sale_price) AS revenue
FROM df_orders o
JOIN df_orders p ON o.product_id = p.product_id
GROUP BY category
ORDER BY revenue DESC;
 
        """
    elif option == "2.Find the Cities with the Highest Profit Margins":
        return """
      SELECT c.city, SUM(o.quantity * o.sale_price - o.discount_percent) / SUM(o.quantity * o.sale_price) AS profit_margin
FROM df_orders o
JOIN df_orders c ON o.order_id = c.order_id
GROUP BY c.city
ORDER BY profit_margin DESC
LIMIT 5;

        """
    elif option == "3.Calculate the total discount given for each category":
        return """
        SELECT p.category, SUM(o.sale_price) AS total_discount
FROM df_orders o
JOIN df_orders p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_discount DESC;

        """
    elif option == "4.Find the average sale price per product category":
        return """
        SELECT p.category, AVG(o.sale_price) AS avg_sale_price
FROM df_orders o
JOIN df_orders p ON o.product_id = p.product_id
GROUP BY p.category;
        """
    elif option == "5.Find the region with the highest average sale price":
        return """
     SELECT r.region, AVG(o.sale_price) AS avg_sale_price
FROM df_orders o
JOIN df_orders r ON o.product_id = r.product_id
GROUP BY r.region
ORDER BY avg_sale_price DESC
LIMIT 1;

        """
    elif option == "6.Find the total profit per category":
        return """
        
SELECT p.category, SUM(o.quantity * (o.sale_price - p.profit)) AS total_profit
FROM df_orders o
JOIN df_orders p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_profit DESC;
        """
    elif option == "7.Identify the Top Segments with the Highest Quantity of Orders":
        return """
       SELECT s.segment, SUM(o.quantity) AS total_quantity
FROM df_orders o
JOIN df_orders s ON o.order_id = s.order_id
GROUP BY s.segment
ORDER BY total_quantity DESC
LIMIT 3;

        """
    elif option == "8.Determine the average discount percentage given per region":
        return """
      SELECT r.region, AVG(o.discount_percent) AS avg_discount_percentage
FROM df_orders o
JOIN df_orders r ON o.product_id = r.product_id
GROUP BY r.region;

        """
    elif option == "9.Find the product category with the highest total profit":
        return """
        SELECT p.category, SUM(o.quantity * (o.sale_price - p.category)) AS total_profit
FROM df_orders o
JOIN df_orders p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_profit DESC
LIMIT 1;

        """
    elif option == "10.Calculate the Revenue Generated Per Year":
        return """
    SELECT (o.order_date) AS year, SUM(o.quantity * o.sale_price) AS total_revenue
FROM df_orders o
GROUP BY year
ORDER BY total_revenue DESC;
"""
    return None

# Execute the SQL queries for selected options
if st.button("Execute SQL Queries"):
    for option in selected_options:
        query = generate_query(option)
        
        if query:
            st.write(f"Executing query for: {option}")
            df = execute_sql_query(query)  # Execute the actual query
            
            st.dataframe(df)  # Display results as a DataFrame
        else:
            st.warning(f"No query defined for {option}")