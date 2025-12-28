-- seed_data.sql

-- 1. DROP TABLES 
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

-- 2. CREATE TABLES (Tablo Olusturma)

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
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE, 
    class_id INT REFERENCES group_classes(class_id),
    enrollment_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Registered'
);

CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE, 
    class_id INT REFERENCES group_classes(class_id),
    attendance_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'Present'
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE, 
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    method VARCHAR(50), 
    payment_type VARCHAR(50) DEFAULT 'Membership',
    status VARCHAR(20) DEFAULT 'Paid'
);

CREATE TABLE private_sessions (
    session_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES members(member_id) ON DELETE CASCADE, 
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

-- ==========================================
-- 3. INSERT DATA (Veri Girisi)
-- ==========================================

-- A. Users (Admin, Instructors, and matching Members)
INSERT INTO users (username, password, role) VALUES 
('admin', '123', 'admin'),
('inst_john', '123', 'instructor'),
('inst_jane', '123', 'instructor'),
('inst_murat', '123', 'instructor'),
('inst_elif', '123', 'instructor'),
('inst_alex', '123', 'instructor'),
('mem_ali', '123', 'member'),
('mem_ayse', '123', 'member'),
('mem_mehmet', '123', 'member'),
('mem_zeynep', '123', 'member'),
('mem_burak', '123', 'member'),
('mem_ceren', '123', 'member'),
('mem_deniz', '123', 'member'),
('mem_emir', '123', 'member'),
('mem_fatma', '123', 'member'),
('mem_gamze', '123', 'member'),
('mem_hakan', '123', 'member'),
('mem_irem', '123', 'member'),
('mem_can', '123', 'member'),
('mem_leyla', '123', 'member');

-- B. Membership Plans
INSERT INTO membership_plans (plan_name, description, monthly_fee, duration_months, access_level) VALUES 
('Gold Plan', 'Unlimited access to all facilities + Spa', 150.00, 12, 'High'),
('Silver Plan', 'Standard gym access + Group Classes', 80.00, 6, 'Medium'),
('Bronze Plan', 'Off-peak gym access only', 50.00, 1, 'Low'),
('Student Saver', 'Discounted plan for students', 40.00, 3, 'Medium'),
('Platinum VIP', 'Personal trainer included + Private parking', 300.00, 12, 'High'),
('Weekend Warrior', 'Access only on weekends', 30.00, 1, 'Low'),
('Corporate Flex', 'Company sponsored plan', 100.00, 12, 'Medium'),
('Senior Citizen', 'Special plan for 65+', 45.00, 12, 'Low');

-- C. Members (15 Records)
INSERT INTO members (first_name, last_name, email, phone, address, gender, date_of_birth, status, plan_id, join_date) VALUES 
('Ali', 'Yilmaz', 'ali@test.com', '555-0101', 'Istanbul, Sisli', 'M', '1990-05-15', 'Active', 1, CURRENT_DATE - INTERVAL '120 days'),
('Ayşe', 'Demir', 'ayse@test.com', '555-0102', 'Istanbul, Kadikoy', 'F', '1995-08-20', 'Active', 2, CURRENT_DATE - INTERVAL '60 days'),
('Mehmet', 'Kaya', 'mehmet@test.com', '555-0103', 'Istanbul, Besiktas', 'M', '1988-03-10', 'Inactive', 1, CURRENT_DATE - INTERVAL '200 days'),
('Zeynep', 'Celik', 'zeynep@test.com', '555-0104', 'Istanbul, Beyoglu', 'F', '1992-11-25', 'Cancelled', 3, CURRENT_DATE - INTERVAL '300 days'),
('Burak', 'Oz', 'burak@test.com', '555-0105', 'Istanbul, Fatih', 'M', '2000-01-01', 'Active', 4, CURRENT_DATE - INTERVAL '10 days'),
('Ceren', 'Yildiz', 'ceren@test.com', '555-0106', 'Istanbul, Uskudar', 'F', '1998-04-14', 'Active', 2, CURRENT_DATE - INTERVAL '15 days'),
('Deniz', 'Arslan', 'deniz@test.com', '555-0107', 'Istanbul, Maltepe', 'M', '1985-07-30', 'Active', 5, CURRENT_DATE - INTERVAL '400 days'),
('Emir', 'Kara', 'emir@test.com', '555-0108', 'Istanbul, Sariyer', 'M', '1993-09-09', 'Active', 1, CURRENT_DATE - INTERVAL '90 days'),
('Fatma', 'Sahin', 'fatma@test.com', '555-0109', 'Istanbul, Kartal', 'F', '1975-12-12', 'Active', 7, CURRENT_DATE - INTERVAL '30 days'),
('Gamze', 'Polat', 'gamze@test.com', '555-0110', 'Istanbul, Pendik', 'F', '1996-02-28', 'Active', 2, CURRENT_DATE - INTERVAL '5 days'),
('Hakan', 'Kurt', 'hakan@test.com', '555-0111', 'Istanbul, Bakirkoy', 'M', '1980-06-05', 'Frozen', 5, CURRENT_DATE - INTERVAL '150 days'),
('Irem', 'Koc', 'irem@test.com', '555-0112', 'Istanbul, Atasehir', 'F', '1999-10-10', 'Active', 4, CURRENT_DATE - INTERVAL '20 days'),
('Can', 'Aydin', 'can@test.com', '555-0113', 'Istanbul, Beykoz', 'M', '1991-05-22', 'Active', 1, CURRENT_DATE - INTERVAL '365 days'),
('Leyla', 'Tekin', 'leyla@test.com', '555-0114', 'Istanbul, Sisli', 'F', '1989-08-15', 'Active', 6, CURRENT_DATE - INTERVAL '2 days'),
('Onur', 'Guler', 'onur@test.com', '555-0115', 'Istanbul, Besiktas', 'M', '1994-03-03', 'Active', 2, CURRENT_DATE - INTERVAL '45 days');

-- D. Instructors
INSERT INTO instructors (first_name, last_name, specialization, phone, email, hire_date) VALUES 
('John', 'Doe', 'Yoga Expert', '555-2001', 'john@gym.com', '2020-01-15'),
('Jane', 'Smith', 'Pilates Instructor', '555-2002', 'jane@gym.com', '2021-06-01'),
('Murat', 'Yilmaz', 'Bodybuilding Coach', '555-2003', 'murat@gym.com', '2019-03-10'),
('Elif', 'Demir', 'Zumba & Dance', '555-2004', 'elif@gym.com', '2022-09-05'),
('Alex', 'Muller', 'CrossFit', '555-2005', 'alex@gym.com', '2021-01-20'),
('Sarah', 'Connor', 'HIIT Specialist', '555-2006', 'sarah@gym.com', '2023-01-15'),
('Mike', 'Tyson', 'Boxing Coach', '555-2007', 'mike@gym.com', '2018-05-30'),
('Emily', 'Blunt', 'Rehabilitation', '555-2008', 'emily@gym.com', '2020-11-11'),
('David', 'Beck', 'Cardio & Running', '555-2009', 'david@gym.com', '2022-04-04'),
('Jessica', 'Alba', 'Nutritionist & Wellness', '555-2010', 'jessica@gym.com', '2023-05-01');

-- E. Rooms
INSERT INTO rooms (room_name, capacity, location) VALUES 
('Studio A', 20, '1st Floor'),
('Studio B', 15, '2nd Floor'),
('Main Gym Floor', 100, 'Ground Floor'),
('Spinning Room', 25, 'Basement'),
('Boxing Ring', 10, 'Ground Floor Area 2'),
('Pool Area', 50, 'B1 Level'),
('Yoga Loft', 12, 'Rooftop'),
('CrossFit Zone', 30, 'Outdoor Area'),
('Massage Room 1', 1, 'Spa Area'),
('Sauna', 8, 'Spa Area');

-- F. Group Classes (Mixed Past and Future dates for testing)
INSERT INTO group_classes (class_name, description, instructor_id, room_id, start_time, end_time, capacity, level) VALUES 
('Morning Yoga', 'Wake up flow', 1, 1, CURRENT_TIMESTAMP - INTERVAL '2 days', CURRENT_TIMESTAMP - INTERVAL '2 days' + INTERVAL '1 hour', 20, 'Beginner'),
('Advanced Pilates', 'Core strength', 2, 2, CURRENT_TIMESTAMP + INTERVAL '1 day', CURRENT_TIMESTAMP + INTERVAL '1 day' + INTERVAL '1 hour', 15, 'Advanced'),
('Zumba Party', 'Dance fitness', 4, 1, CURRENT_TIMESTAMP + INTERVAL '2 hours', CURRENT_TIMESTAMP + INTERVAL '3 hours', 20, 'All Levels'),
('Hardcore CrossFit', 'High intensity', 5, 8, CURRENT_TIMESTAMP + INTERVAL '3 days', CURRENT_TIMESTAMP + INTERVAL '3 days' + INTERVAL '90 minutes', 30, 'Advanced'),
('Spinning 101', 'Intro to cycling', 6, 4, CURRENT_TIMESTAMP - INTERVAL '5 days', CURRENT_TIMESTAMP - INTERVAL '5 days' + INTERVAL '45 minutes', 25, 'Beginner'),
('Boxing Basics', 'Technique training', 7, 5, CURRENT_TIMESTAMP + INTERVAL '4 days', CURRENT_TIMESTAMP + INTERVAL '4 days' + INTERVAL '1 hour', 10, 'Intermediate'),
('Aqua Aerobics', 'Pool workout', 9, 6, CURRENT_TIMESTAMP + INTERVAL '1 week', CURRENT_TIMESTAMP + INTERVAL '1 week' + INTERVAL '1 hour', 20, 'Low Impact'),
('HIIT Blast', 'Fat burning', 6, 3, CURRENT_TIMESTAMP - INTERVAL '1 day', CURRENT_TIMESTAMP - INTERVAL '1 day' + INTERVAL '30 minutes', 40, 'Advanced'),
('Sunset Yoga', 'Relaxing flow', 1, 7, CURRENT_TIMESTAMP + INTERVAL '12 hours', CURRENT_TIMESTAMP + INTERVAL '13 hours', 12, 'All Levels'),
('BodyPump', 'Weight lifting', 3, 1, CURRENT_TIMESTAMP - INTERVAL '10 days', CURRENT_TIMESTAMP - INTERVAL '10 days' + INTERVAL '1 hour', 20, 'Intermediate'),
('Meditation', 'Mindfulness', 8, 2, CURRENT_TIMESTAMP + INTERVAL '5 hours', CURRENT_TIMESTAMP + INTERVAL '6 hours', 15, 'Beginner'),
('Kickboxing', 'Cardio kickboxing', 7, 5, CURRENT_TIMESTAMP + INTERVAL '2 days', CURRENT_TIMESTAMP + INTERVAL '2 days' + INTERVAL '1 hour', 15, 'Intermediate');

-- G. Class Enrollments
INSERT INTO class_enrollments (member_id, class_id, status) VALUES 
(1, 1, 'Completed'), -- Past class
(2, 1, 'Completed'),
(5, 3, 'Registered'), -- Future class
(6, 3, 'Registered'),
(7, 4, 'Registered'),
(8, 2, 'Waitlist'),
(1, 4, 'Registered'),
(9, 5, 'Cancelled'),
(10, 6, 'Registered'),
(11, 7, 'Registered'),
(12, 3, 'Registered'),
(13, 10, 'Completed'),
(14, 9, 'Registered'),
(15, 8, 'Completed');

-- H. Attendance (For past classes)
INSERT INTO attendance (member_id, class_id, attendance_date, status) VALUES 
(1, 1, CURRENT_DATE - INTERVAL '2 days', 'Present'),
(2, 1, CURRENT_DATE - INTERVAL '2 days', 'Present'),
(13, 10, CURRENT_DATE - INTERVAL '10 days', 'Present'),
(15, 8, CURRENT_DATE - INTERVAL '1 day', 'Present'),
(1, 5, CURRENT_DATE - INTERVAL '5 days', 'Absent'),
(2, 10, CURRENT_DATE - INTERVAL '10 days', 'Excused');

-- I. Payments
INSERT INTO payments (member_id, amount, method, payment_type, status) VALUES 
(1, 150.00, 'Credit Card', 'Membership', 'Paid'),
(2, 80.00, 'Cash', 'Membership', 'Paid'),
(3, 150.00, 'Credit Card', 'Membership', 'Paid'),
(4, 50.00, 'Bank Transfer', 'Membership', 'Paid'),
(5, 40.00, 'Credit Card', 'Membership', 'Paid'),
(6, 80.00, 'Cash', 'Membership', 'Paid'),
(7, 300.00, 'Credit Card', 'Membership', 'Paid'),
(8, 150.00, 'Credit Card', 'Membership', 'Failed'),
(9, 100.00, 'Company Check', 'Membership', 'Paid'),
(1, 50.00, 'Cash', 'Personal Training', 'Paid'),
(7, 20.00, 'Credit Card', 'Merchandise', 'Paid'),
(10, 80.00, 'Credit Card', 'Membership', 'Paid'),
(11, 300.00, 'Bank Transfer', 'Membership', 'Paid'),
(12, 40.00, 'Cash', 'Membership', 'Pending'),
(13, 150.00, 'Credit Card', 'Membership', 'Paid');

-- J. Private Sessions
INSERT INTO private_sessions (member_id, instructor_id, session_date, start_time, end_time, status, notes) VALUES
(1, 1, CURRENT_DATE + INTERVAL '2 days', '10:00:00', '11:00:00', 'Scheduled', 'Focus on flexibility'),
(2, 2, CURRENT_DATE + INTERVAL '3 days', '14:00:00', '15:00:00', 'Scheduled', 'Core strength'),
(7, 3, CURRENT_DATE + INTERVAL '1 day', '09:00:00', '10:30:00', 'Scheduled', 'Heavy lifting technique'),
(5, 6, CURRENT_DATE + INTERVAL '5 days', '18:00:00', '19:00:00', 'Scheduled', 'HIIT cardio personal'),
(1, 8, CURRENT_DATE - INTERVAL '5 days', '11:00:00', '12:00:00', 'Completed', 'Shoulder rehab'),
(11, 3, CURRENT_DATE - INTERVAL '10 days', '08:00:00', '09:00:00', 'Cancelled', 'Member felt sick'),
(8, 7, CURRENT_DATE + INTERVAL '6 days', '15:00:00', '16:00:00', 'Scheduled', 'Boxing pad work'),
(9, 1, CURRENT_DATE + INTERVAL '1 week', '07:00:00', '08:00:00', 'Scheduled', 'Morning meditation'),
(15, 5, CURRENT_DATE + INTERVAL '2 weeks', '12:00:00', '13:00:00', 'Scheduled', 'Crossfit fundamentals'),
(4, 2, CURRENT_DATE - INTERVAL '20 days', '10:00:00', '11:00:00', 'Completed', 'Intro session');

-- K. Equipment
INSERT INTO equipment (name, category, purchase_date, cost, condition) VALUES
('Treadmill X1', 'Cardio', '2022-01-10', 2500.00, 'Good'),
('Treadmill X2', 'Cardio', '2022-01-10', 2500.00, 'Repair Needed'),
('Dumbbell Set A', 'Strength', '2021-05-20', 500.00, 'Used'),
('Dumbbell Set B', 'Strength', '2021-05-20', 500.00, 'Good'),
('Yoga Mats Bulk', 'Accessories', '2023-01-01', 200.00, 'New'),
('Smith Machine', 'Strength', '2020-08-15', 3000.00, 'Good'),
('Elliptical Runner', 'Cardio', '2022-03-10', 1800.00, 'Good'),
('Rowing Machine', 'Cardio', '2021-12-05', 1200.00, 'Good'),
('Kettlebell Set', 'Strength', '2022-06-20', 300.00, 'Used'),
('Bench Press Station', 'Strength', '2019-11-11', 800.00, 'Old'),
('Leg Press Machine', 'Strength', '2020-02-28', 2200.00, 'Good'),
('Cable Crossover', 'Strength', '2021-09-09', 2500.00, 'Good'),
('Spin Bike Pro 1', 'Cardio', '2023-02-15', 900.00, 'New'),
('Spin Bike Pro 2', 'Cardio', '2023-02-15', 900.00, 'New'),
('Boxing Bag', 'Accessories', '2022-07-07', 150.00, 'Used');

-- L. Equipment Maintenance
INSERT INTO equipment_maintenance (equipment_id, maintenance_date, description, maintenance_type, cost) VALUES
(1, CURRENT_DATE - INTERVAL '5 days', 'Belt replacement', 'Repair', 150.00),
(2, CURRENT_DATE - INTERVAL '2 days', 'Screen malfunction', 'Inspection', 50.00),
(10, CURRENT_DATE - INTERVAL '30 days', 'Upholstery fix', 'Repair', 80.00),
(6, CURRENT_DATE - INTERVAL '60 days', 'Oiling and tightening', 'Routine', 40.00),
(13, CURRENT_DATE - INTERVAL '10 days', 'Pedal adjustment', 'Adjustment', 0.00),
(8, CURRENT_DATE - INTERVAL '100 days', 'Chain replaced', 'Repair', 120.00),
(2, CURRENT_DATE - INTERVAL '1 year', 'Initial Setup', 'Installation', 100.00),
(11, CURRENT_DATE - INTERVAL '15 days', 'Safety check', 'Inspection', 30.00),
(15, CURRENT_DATE - INTERVAL '20 days', 'Chain replacement', 'Repair', 45.00),
(1, CURRENT_DATE - INTERVAL '6 months', 'Motor check', 'Routine', 200.00);