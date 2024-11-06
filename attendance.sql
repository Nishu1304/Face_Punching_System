create 	database attendance;
use attendance;


CREATE TABLE employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE entries (
    attendance_id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT,
    Date DATE,
    check_in TIME,
    check_out TIME,
    hours_worked FLOAT,
    late_arrival BOOLEAN,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

INSERT INTO employees (name)
VALUES
    ('Aditya'),												-- cluster_1
    ('Nishanka'),											-- cluster_5
    ('Sonu'),												-- cluster_2
    ('Pranav'),												-- cluster_0		
    ('Pranjal'), 											-- cluster_4
    ('Vijaykrishna');                                       -- cluster_3

SELECT * FROM employees;

CREATE TABLE status (
    employee_id INT PRIMARY KEY,
    in_out_status BOOLEAN DEFAULT 0,   -- 0 for checked out, 1 for checked in
    check_in_time DATETIME,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);


INSERT INTO entries (employee_id, date, check_in, check_out, hours_worked, late_arrival)
VALUES
    (1, '2024-10-01', '09:05:00', '17:30:00', 8.42, TRUE),   -- Overtime
    (2, '2024-10-01', '08:55:00', '17:10:00', 8.25, FALSE),
    (3, '2024-10-01', '09:15:00', '17:35:00', 8.33, TRUE),   -- Overtime
    (4, '2024-10-01', '08:50:00', '17:05:00', 8.25, FALSE),
    (5, '2024-10-01', '09:10:00', '17:25:00', 8.25, TRUE),
    (6, '2024-10-01', '09:00:00', '17:50:00', 8.83, FALSE),  -- Overtime

    (1, '2024-10-02', '09:02:00', '17:15:00', 8.22, TRUE),   -- Overtime
    (2, '2024-10-02', '08:58:00', '17:12:00', 8.23, FALSE),
    (3, '2024-10-02', '09:20:00', '18:00:00', 8.67, TRUE),   -- Overtime
    (4, '2024-10-02', '08:45:00', '17:15:00', 8.50, FALSE),
    (5, '2024-10-02', '09:15:00', '17:30:00', 8.25, TRUE),
    (6, '2024-10-02', '09:05:00', '18:05:00', 9.00, TRUE),   -- Overtime

    (1, '2024-10-03', '09:00:00', '17:00:00', 8.00, FALSE),
    (2, '2024-10-03', '09:10:00', '17:15:00', 8.08, TRUE),
    (3, '2024-10-03', '09:05:00', '17:10:00', 8.08, FALSE),
    (4, '2024-10-03', '09:00:00', '17:20:00', 8.33, FALSE),
    (5, '2024-10-03', '09:25:00', '17:55:00', 8.50, TRUE),   -- Overtime
    (6, '2024-10-03', '09:00:00', '17:45:00', 8.75, TRUE),   -- Overtime

    (1, '2024-10-04', '09:05:00', '17:10:00', 8.08, TRUE),
    (2, '2024-10-04', '08:50:00', '17:00:00', 8.17, FALSE),
    (3, '2024-10-04', '09:20:00', '18:00:00', 8.67, TRUE),   -- Overtime
    (4, '2024-10-04', '08:55:00', '17:30:00', 8.58, FALSE),  -- Overtime
    (5, '2024-10-04', '09:00:00', '17:30:00', 8.50, FALSE),  -- Overtime
    (6, '2024-10-04', '09:10:00', '17:50:00', 8.67, TRUE),   -- Overtime

    (1, '2024-10-05', '09:00:00', '17:45:00', 8.75, FALSE),  -- Overtime
    (2, '2024-10-05', '09:10:00', '17:15:00', 8.08, TRUE),
    (3, '2024-10-05', '09:00:00', '17:40:00', 8.67, FALSE),  -- Overtime
    (4, '2024-10-05', '09:05:00', '17:05:00', 8.00, FALSE),
    (5, '2024-10-05', '09:15:00', '17:25:00', 8.17, TRUE),
    (6, '2024-10-05', '09:05:00', '17:20:00', 8.25, TRUE),

    (1, '2024-10-06', '09:10:00', '17:55:00', 8.75, TRUE),   -- Overtime
    (2, '2024-10-06', '09:00:00', '17:00:00', 8.00, FALSE),
    (3, '2024-10-06', '09:15:00', '17:45:00', 8.50, TRUE),   -- Overtime
    (4, '2024-10-06', '09:10:00', '17:05:00', 7.92, TRUE),
    (5, '2024-10-06', '08:50:00', '17:25:00', 8.58, FALSE),  -- Overtime
    (6, '2024-10-06', '09:05:00', '18:00:00', 8.92, TRUE),   -- Overtime

    (1, '2024-10-07', '09:05:00', '17:10:00', 8.08, TRUE),
    (2, '2024-10-07', '08:45:00', '17:20:00', 8.58, FALSE),  -- Overtime
    (3, '2024-10-07', '09:20:00', '17:15:00', 7.92, TRUE),
    (4, '2024-10-07', '09:00:00', '17:30:00', 8.50, FALSE),  -- Overtime
    (5, '2024-10-07', '09:00:00', '17:10:00', 8.17, FALSE),
    (6, '2024-10-07', '09:10:00', '17:50:00', 8.67, TRUE);   -- Overtime

SELECT * FROM entries;

