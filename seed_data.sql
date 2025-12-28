-- seed_data.sql

-- 1. DROP Tables
DROP TABLE IF EXISTS equipment_maintenance CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;
DROP TABLE IF EXISTS private_sessions CASCADE;
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS class_enrollments CASCADE;
DROP TABLE IF EXISTS group_classes CASCADE;
DROP TABLE IF EXISTS members CASCADE;
DROP TABLE IF EXISTS instructors CASCADE;
DROP TABLE IF EXISTS membership_plans CASCADE;
DROP TABLE IF EXISTS rooms CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- 2. CREATE Tables

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL -- admin, instructor, member
);

CREATE TABLE membership_plans (
    plan_id SERIAL PRIMARY KEY,
    plan_name VARCHAR(50) NOT NULL,
    description TEXT,
    monthly_fee DECIMAL(10, 2) NOT NULL,
    duration_months INT NOT NULL,
    access_level VARCHAR(20) DEFAULT 'Medium',
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    gender CHAR(1),
    date_of_birth DATE,
    join_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Active',
    plan_id INT REFERENCES membership_plans(plan_id)
);

CREATE TABLE instructors (
    instructor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    hire_date DATE
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(50) NOT NULL,
    capacity INT,
    location VARCHAR(100)
);

CREATE TABLE group_classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    description TEXT,
    instructor_id INT REFERENCES instructors(instructor_id),
    room_id INT REFERENCES rooms(room_id),
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    capacity INT,
    level VARCHAR(20)
);

CREATE TABLE class_enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    class_id INT REFERENCES group_classes(class_id),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Registered'
);

CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    class_id INT REFERENCES group_classes(class_id),
    attendance_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Present'
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    method VARCHAR(50), -- Credit Card, Cash
    payment_type VARCHAR(50) DEFAULT 'Membership',
    status VARCHAR(20) DEFAULT 'Paid'
);

CREATE TABLE private_sessions (
    session_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id),
    instructor_id INT REFERENCES instructors(instructor_id),
    session_date DATE,
    start_time TIME,
    end_time TIME,
    status VARCHAR(20) DEFAULT 'Scheduled',
    notes TEXT
);

CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    purchase_date DATE,
    cost DECIMAL(10, 2),
    condition VARCHAR(50) DEFAULT 'New'
);

CREATE TABLE equipment_maintenance (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INT REFERENCES equipment(equipment_id),
    maintenance_date DATE DEFAULT CURRENT_DATE,
    description TEXT,
    maintenance_type VARCHAR(50),
    cost DECIMAL(10, 2)
);

-- 3. INSERT Data

INSERT INTO users (username, password, role) VALUES 
('admin', '123', 'admin'),
('instructor_john', '123', 'instructor'),
('member_ali', '123', 'member');

INSERT INTO membership_plans (plan_name, description, monthly_fee, duration_months, access_level) VALUES 
('Gold Plan', 'Access to everything', 150.00, 12, 'High'),
('Silver Plan', 'Limited access', 80.00, 6, 'Medium'),
('Bronze Plan', 'Entry only', 50.00, 1, 'Low');

INSERT INTO members (first_name, last_name, email, phone, address, gender, date_of_birth, status, plan_id, join_date) VALUES 
('Ali', 'Yilmaz', 'ali@test.com', '555-0001', 'Istanbul, Sisli', 'M', '1990-05-15', 'Active', 1, CURRENT_DATE - INTERVAL '60 days'),
('Ayşe', 'Demir', 'ayse@test.com', '555-0002', 'Istanbul, Kadikoy', 'F', '1995-08-20', 'Active', 2, CURRENT_DATE - INTERVAL '10 days'),
('Mehmet', 'Kaya', 'mehmet@test.com', '555-0003', 'Istanbul, Besiktas', 'M', '1988-03-10', 'Active', 1, CURRENT_DATE - INTERVAL '40 days'), -- Absent member
('Zeynep', 'Celik', 'zeynep@test.com', '555-0004', 'Istanbul, Beyoglu', 'F', '1992-11-25', 'Cancelled', 3, CURRENT_DATE - INTERVAL '100 days');

INSERT INTO instructors (first_name, last_name, specialization, phone, email, hire_date) VALUES 
('John', 'Doe', 'Yoga Expert', '555-1001', 'john@gym.com', '2020-01-15'),
('Jane', 'Smith', 'Pilates Instructor', '555-1002', 'jane@gym.com', '2021-06-01');

INSERT INTO rooms (room_name, capacity, location) VALUES 
('Studio A', 20, '1st Floor'),
('Studio B', 15, '2nd Floor');

INSERT INTO group_classes (class_name, description, instructor_id, room_id, start_time, capacity) VALUES 
('Morning Yoga', 'Morning yoga', 1, 1, CURRENT_TIMESTAMP, 20),
('Advanced Pilates', 'Advanced level', 2, 2, CURRENT_TIMESTAMP + INTERVAL '1 day', 15);

INSERT INTO class_enrollments (class_id, member_id, status) VALUES 
(1, 1, 'Confirmed'),
(1, 2, 'Confirmed');

INSERT INTO attendance (member_id, class_id, attendance_date, status) VALUES 
(1, 1, CURRENT_DATE, 'Present'),
(2, 1, CURRENT_DATE, 'Present');

INSERT INTO payments (member_id, amount, method, status) VALUES 
(1, 150.00, 'Credit Card', 'Paid'),
(2, 80.00, 'Cash', 'Paid');

INSERT INTO private_sessions (member_id, instructor_id, session_date, start_time, end_time, status, notes) VALUES
(1, 1, CURRENT_DATE + INTERVAL '2 days', '10:00:00', '11:00:00', 'Scheduled', 'Focus on flexibility'),
(2, 2, CURRENT_DATE + INTERVAL '3 days', '14:00:00', '15:00:00', 'Scheduled', 'Core strength');

INSERT INTO equipment (name, category, purchase_date, cost, condition) VALUES
('Treadmill X1', 'Cardio', '2022-01-10', 2500.00, 'Good'),
('Dumbbell Set', 'Strength', '2021-05-20', 500.00, 'Used'),
('Yoga Mats', 'Accessories', '2023-01-01', 200.00, 'New');

INSERT INTO equipment_maintenance (equipment_id, maintenance_date, description, maintenance_type, cost) VALUES
(1, CURRENT_DATE - INTERVAL '5 days', 'Belt replacement', 'Repair', 150.00);