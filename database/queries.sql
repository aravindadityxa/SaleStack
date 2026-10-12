-- Basic Queries

-- 1. Retrieve all records from the customer_sales table
SELECT * FROM customer_sales;

-- 2. Retrieve all records from the branches table
SELECT * FROM branches;

-- 3. Retrieve all records from the payment_splits table
SELECT * FROM payment_splits;

-- 4. Display all sales with status = 'Open'
SELECT * FROM customer_sales WHERE status = 'Open';

-- 5. Retrieve all sales belonging to the Chennai branch
SELECT cs.* FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
WHERE b.branch_name = 'Chennai';

-- Aggregation Queries

-- 6. Calculate the total gross sales across all branches
SELECT SUM(gross_sales) as total_gross_sales FROM customer_sales;

-- 7. Calculate the total received amount across all sales
SELECT SUM(received_amount) as total_received FROM customer_sales;

-- 8. Calculate the total pending amount across all sales
SELECT SUM(pending_amount) as total_pending FROM customer_sales;

-- 9. Count the total number of sales per branch
SELECT 
    b.branch_name, 
    COUNT(cs.sale_id) as total_sales
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
GROUP BY b.branch_id, b.branch_name
ORDER BY total_sales DESC;

-- 10. Find the average gross sales amount
SELECT AVG(gross_sales) as average_gross_sales FROM customer_sales;

-- Join-Based Queries

-- 11. Retrieve sales details along with the branch name
SELECT 
    cs.sale_id,
    cs.date,
    b.branch_name,
    cs.name as customer_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount,
    cs.status
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.date DESC;

-- 12. Retrieve sales details along with total payment received (using payment_splits)
SELECT 
    cs.sale_id,
    cs.name as customer_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount,
    COUNT(ps.payment_id) as payment_count,
    SUM(ps.amount_paid) as total_paid
FROM customer_sales cs
LEFT JOIN payment_splits ps ON cs.sale_id = ps.sale_id
GROUP BY cs.sale_id, cs.name, cs.gross_sales, cs.received_amount, cs.pending_amount
ORDER BY cs.sale_id;

-- 13. Show branch-wise total gross sales (using JOIN & GROUP BY)
SELECT 
    b.branch_id,
    b.branch_name,
    b.branch_admin_name,
    COUNT(cs.sale_id) as total_sales,
    SUM(cs.gross_sales) as total_gross_sales,
    SUM(cs.received_amount) as total_received,
    SUM(cs.pending_amount) as total_pending
FROM branches b
LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_id, b.branch_name, b.branch_admin_name
ORDER BY total_gross_sales DESC;

-- 14. Display sales along with payment method used
SELECT 
    cs.sale_id,
    cs.name as customer_name,
    cs.gross_sales,
    cs.received_amount,
    ps.payment_method,
    ps.amount_paid,
    ps.payment_date
FROM customer_sales cs
LEFT JOIN payment_splits ps ON cs.sale_id = ps.sale_id
ORDER BY cs.sale_id, ps.payment_date;

-- 15. Retrieve sales along with branch admin name
SELECT 
    cs.sale_id,
    cs.date,
    b.branch_name,
    b.branch_admin_name,
    cs.name as customer_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount,
    cs.status
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.date DESC;

-- Financial Tracking Queries

-- 16. Find sales where the pending amount is greater than 5000
SELECT 
    cs.sale_id,
    cs.name as customer_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount,
    b.branch_name
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
WHERE cs.pending_amount > 5000
ORDER BY cs.pending_amount DESC;

-- 17. Retrieve top 3 highest gross sales
SELECT 
    cs.sale_id,
    cs.name as customer_name,
    cs.date,
    b.branch_name,
    cs.product_name,
    cs.gross_sales,
    cs.received_amount,
    cs.pending_amount
FROM customer_sales cs
JOIN branches b ON cs.branch_id = b.branch_id
ORDER BY cs.gross_sales DESC
LIMIT 3;

-- 18. Find the branch with highest total gross sales
SELECT 
    b.branch_id,
    b.branch_name,
    b.branch_admin_name,
    COUNT(cs.sale_id) as total_sales,
    SUM(cs.gross_sales) as total_gross_sales
FROM branches b
LEFT JOIN customer_sales cs ON b.branch_id = cs.branch_id
GROUP BY b.branch_id, b.branch_name, b.branch_admin_name
ORDER BY total_gross_sales DESC
LIMIT 1;

-- 19. Retrieve monthly sales summary (group by month & year)
SELECT 
    DATE_FORMAT(cs.date, '%Y-%m') as month,
    COUNT(cs.sale_id) as total_sales,
    SUM(cs.gross_sales) as total_gross_sales,
    SUM(cs.received_amount) as total_received,
    SUM(cs.pending_amount) as total_pending,
    ROUND((SUM(cs.received_amount) / SUM(cs.gross_sales)) * 100, 2) as received_percentage
FROM customer_sales cs
GROUP BY DATE_FORMAT(cs.date, '%Y-%m')
ORDER BY month DESC;

-- 20. Calculate payment method-wise total collection (Cash / UPI / Card)
SELECT 
    ps.payment_method,
    COUNT(ps.payment_id) as total_payments,
    SUM(ps.amount_paid) as total_collected,
    ROUND(AVG(ps.amount_paid), 2) as average_payment
FROM payment_splits ps
GROUP BY ps.payment_method
ORDER BY total_collected DESC;
