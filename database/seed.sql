-- Suppliers
INSERT INTO supplier (name, manager, phone, status)
VALUES
('NorthStar Logistics', 'Amit Sharma', '9876543210', 'Active'),
('FastMove Transport', 'Neha Singh', '9876543211', 'Active');

-- Trucks
INSERT INTO truck (registration, driver, capacity, status)
VALUES
('DL01AB1234', 'Rahul', 10, 'Available'),
('DL02CD5678', 'Vikas', 15, 'Available'),
('DL03EF9012', 'Kim', 20, 'Maintenance');

-- Products
INSERT INTO product (name, sku, quantity, supplier_id)
VALUES
('Electronic Components', 'ELEC-001', 500, 1),
('Packaging Material', 'PACK-001', 1000, 2),
('Industrial Equipment', 'IND-001', 100, 1);

-- Routes
INSERT INTO route (origin, destination, distance_km, selected, truck_id)
VALUES
('Delhi', 'Jaipur', 280, TRUE, 1),
('Delhi', 'Lucknow', 550, FALSE, 2),
('Agra', 'Delhi', 230, FALSE, 3);

-- Tickets
INSERT INTO ticket (title, description, priority, status, assignee, jira_key)
VALUES
('Truck maintenance required', 'Truck requires scheduled maintenance', 'High', 'Open', 'Rahul', 'LOG-101'),
('Route delay', 'Delivery delayed due to traffic', 'Medium', 'In Progress', 'Vikas', 'LOG-102');