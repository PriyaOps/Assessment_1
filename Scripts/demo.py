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
        "1.Find top 10 highest revenue generating products",
        "2.Find the top 5 cities with the highest profit margins",
        "3.Calculate the total discount given for each category",
        "4.Find the average sale price per product category",
        "5.Find the region with the highest average sale price",
        "6.Find the total profit per category",
        "7.Identify the top 3 segments with the highest quantity of orders",
        "8.Determine the average discount percentage given per region",
        "9.Find the product category with the highest total profit",
        "10.Calculate the total revenue generated per year"
    ]
)

# Function to generate SQL queries based on selected options
def generate_query(option):
    if option == "1.Find top 10 highest revenue generating products":
        return """
        SELECT category, sub_category, profit
        FROM df_orders
        ORDER BY category DESC;
        """
    elif option == "2.Find the top 5 cities with the highest profit margins":
        return """
        SELECT city, sum(discount) as total_discount 
        FROM df_orders
        GROUP BY  city
        ORDER BY total_discount DESC
        LIMIT 5;
        """
    elif option == "3.Calculate the total discount given for each category":
        return """
        SELECT category, SUM(discount) AS total_discount
FROM df_orders
GROUP BY category
ORDER BY total_discount DESC;
        """
    elif option == "4.Find the average sale price per product category":
        return """
        SELECT category, AVG(sale_price) AS avg_sale_price
        FROM df_orders
        GROUP BY category
        ORDER BY avg_sale_price DESC;
        """
    elif option == "5.Find the region with the highest average sale price":
        return """
        SELECT region, AVG(sale_price) AS avg_sale_price
        FROM df_orders
        GROUP BY region
        ORDER BY avg_sale_price DESC
        LIMIT 1;
;
        """
    elif option == "6.Find the total profit per category":
        return """
        SELECT category, SUM(profit) AS total_profit
        FROM df_orders
        GROUP BY category 
        ORDER BY total_profit DESC;
        """
    elif option == "7.Identify the top 3 segments with the highest quantity of orders":
        return """
        SELECT segment, COUNT(*) AS order_count
        FROM df_orders
        GROUP BY segment
        ORDER BY order_count DESC
        LIMIT 3;
        """
    elif option == "8.Determine the average discount percentage given per region":
        return """
        SELECT region, AVG(discount) AS avg_discount
FROM df_orders
GROUP BY region
ORDER BY avg_discount DESC;
        """
    elif option == "9.Find the product category with the highest total profit":
        return """
        SELECT category, SUM(profit) AS total_profit
        FROM df_orders
        GROUP BY category
        ORDER BY total_profit DESC
        LIMIT 1;
        """
    elif option == "10.Calculate the total revenue generated per year":
        return """
        SELECT YEAR(order_date) AS year, SUM(sale_price) AS total_revenue
        FROM df_orders
        GROUP BY YEAR
        ORDER BY year;
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
