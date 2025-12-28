-- seed_data.sql

-- 1. Clean up old data (Order is important: child tables first, then parent tables)
TRUNCATE attendance, payments, class_enrollments, group_classes, members, instructors, membership_plans, rooms, users RESTART IDENTITY CASCADE;

-- 2. Users (Admin and Normal Member)
INSERT INTO users (username, password, role) VALUES 
('admin', '123', 'admin'),
('instructor_john', '123', 'instructor'),
('member_ali', '123', 'member');

('member_ali', '123', 'member');

-- 3. Membership Plans
INSERT INTO membership_plans (plan_name, description, monthly_fee, duration_months, access_level) VALUES 
('Gold Plan', 'Access to everything', 150.00, 12, 'High'),
('Silver Plan', 'Limited access', 80.00, 6, 'Medium'),
('Bronze Plan', 'Entry only', 50.00, 1, 'Low');

-- 4. Members
-- Note: Ali and Ayse are active, Mehmet is passive.
INSERT INTO members (first_name, last_name, email, phone, status, plan_id, join_date) VALUES 
('Ali', 'Yilmaz', 'ali@test.com', '555-0001', 'Active', 1, CURRENT_DATE - INTERVAL '60 days'),
('Ayşe', 'Demir', 'ayse@test.com', '555-0002', 'Active', 2, CURRENT_DATE - INTERVAL '10 days'),
('Mehmet', 'Kaya', 'mehmet@test.com', '555-0003', 'Active', 1, CURRENT_DATE - INTERVAL '40 days'), -- Absent member (For report)
('Zeynep', 'Celik', 'zeynep@test.com', '555-0004', 'Cancelled', 3, CURRENT_DATE - INTERVAL '100 days');

-- 5. Instructors and Rooms
INSERT INTO instructors (first_name, last_name, specialization) VALUES 
('John', 'Doe', 'Yoga Expert'),
('Jane', 'Smith', 'Pilates Instructor');

INSERT INTO rooms (room_name, capacity, location) VALUES 
('Studio A', 20, '1st Floor'),
('Studio B', 15, '2nd Floor');

-- 6. Group Classes
INSERT INTO group_classes (class_name, description, instructor_id, room_id, start_time, capacity) VALUES 
('Morning Yoga', 'Morning yoga', 1, 1, CURRENT_TIMESTAMP, 20),
('Advanced Pilates', 'Advanced level', 2, 2, CURRENT_TIMESTAMP + INTERVAL '1 day', 15);

-- 7. Class Enrollments and Attendance
-- Ali and Ayse attended class. Mehmet never attended (Important for report test).
INSERT INTO class_enrollments (class_id, member_id, status) VALUES 
(1, 1, 'Confirmed'),
(1, 2, 'Confirmed');

INSERT INTO attendance (member_id, class_id, attendance_date, status) VALUES 
(1, 1, CURRENT_DATE, 'Present'), -- Ali attended
(2, 1, CURRENT_DATE, 'Present'); -- Ayse attended
-- No attendance added for Mehmet!

-- 8. Payments
INSERT INTO payments (member_id, amount, method, status) VALUES 
(1, 150.00, 'Credit Card', 'Paid'),
(2, 80.00, 'Cash', 'Paid');