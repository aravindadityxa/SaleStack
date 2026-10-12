INSERT INTO branches (branch_name, branch_admin_name) VALUES
('Chennai', 'Raj Kumar'),
('Delhi', 'Priya Singh'),
('Mumbai', 'Amit Patel');

INSERT INTO users (username, password, branch_id, role, email) VALUES
('admin', 'scrypt:32768:8:1$JqC7E3D9F5K2L1M4$8a5f9c3e2b1d4f6a7e8c9b0a1d2f3e4c5a6b7d8e9f0a1c2d3e4f5a6b7c8d9', 1, 'Super Admin', 'admin@salestack.com'),
('branch_manager_chn', 'scrypt:32768:8:1$JqC7E3D9F5K2L1M4$8a5f9c3e2b1d4f6a7e8c9b0a1d2f3e4c5a6b7d8e9f0a1c2d3e4f5a6b7c8d9', 1, 'Admin', 'chn@salestack.com'),
('branch_manager_del', 'scrypt:32768:8:1$JqC7E3D9F5K2L1M4$8a5f9c3e2b1d4f6a7e8c9b0a1d2f3e4c5a6b7d8e9f0a1c2d3e4f5a6b7c8d9', 2, 'Admin', 'del@salestack.com');

INSERT INTO customer_sales (branch_id, date, name, mobile_number, product_name, gross_sales, received_amount, status) VALUES
('1', '2024-01-15', 'Rajesh Kumar', '9876543210', 'DS', 50000, 0, 'Open'),
('1', '2024-01-16', 'Anjali Singh', '9876543211', 'DA', 75000, 0, 'Open'),
('1', '2024-01-17', 'Vikram Patel', '9876543212', 'BA', 100000, 0, 'Open'),
('1', '2024-01-18', 'Priya Sharma', '9876543213', 'FSD', 150000, 0, 'Close'),
('1', '2024-01-19', 'Arjun Verma', '9876543214', 'DS', 45000, 0, 'Open'),
('2', '2024-01-15', 'Aman Gupta', '9876543220', 'DA', 80000, 0, 'Open'),
('2', '2024-01-16', 'Neha Kapoor', '9876543221', 'FSD', 200000, 0, 'Open'),
('2', '2024-01-17', 'Rohan Desai', '9876543222', 'BA', 120000, 0, 'Open'),
('3', '2024-01-15', 'Sanjay Nair', '9876543230', 'DS', 60000, 0, 'Open'),
('3', '2024-01-16', 'Divya Reddy', '9876543231', 'DA', 90000, 0, 'Open');

INSERT INTO payment_splits (sale_id, payment_date, amount_paid, payment_method) VALUES
(1, '2024-01-20', 15000, 'UPI'),
(1, '2024-01-21', 20000, 'Cash'),
(1, '2024-01-22', 15000, 'Card'),
(2, '2024-01-20', 30000, 'Cash'),
(2, '2024-01-23', 45000, 'UPI'),
(3, '2024-01-20', 60000, 'Card'),
(4, '2024-01-18', 150000, 'UPI'),
(6, '2024-01-20', 50000, 'Cash'),
(7, '2024-01-20', 100000, 'UPI'),
(7, '2024-01-25', 50000, 'Card'),
(7, '2024-01-26', 50000, 'Cash'),
(9, '2024-01-20', 40000, 'UPI');
