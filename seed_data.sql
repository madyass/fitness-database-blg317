-- seed_data.sql

-- 1. Önce eski verileri temizle (Sıralama önemli: önce child, sonra parent tablolar)
TRUNCATE attendance, payments, class_enrollments, group_classes, members, instructors, membership_plans, rooms, users RESTART IDENTITY CASCADE;

-- 2. Kullanıcılar (Admin ve Normal Üye)
INSERT INTO users (username, password, role) VALUES 
('admin', '123', 'admin'),
('instructor_john', '123', 'instructor'),
('member_ali', '123', 'member');

-- 3. Üyelik Planları
INSERT INTO membership_plans (plan_name, description, monthly_fee, duration_months, access_level) VALUES 
('Gold Plan', 'Her şeye erişim', 150.00, 12, 'High'),
('Silver Plan', 'Sınırlı erişim', 80.00, 6, 'Medium'),
('Bronze Plan', 'Sadece giriş', 50.00, 1, 'Low');

-- 4. Üyeler
-- Not: Ali ve Ayşe aktif, Mehmet pasif olsun.
INSERT INTO members (first_name, last_name, email, phone, status, plan_id, join_date) VALUES 
('Ali', 'Yilmaz', 'ali@test.com', '555-0001', 'Active', 1, CURRENT_DATE - INTERVAL '60 days'),
('Ayşe', 'Demir', 'ayse@test.com', '555-0002', 'Active', 2, CURRENT_DATE - INTERVAL '10 days'),
('Mehmet', 'Kaya', 'mehmet@test.com', '555-0003', 'Active', 1, CURRENT_DATE - INTERVAL '40 days'), -- Devamsız üye (Rapor için)
('Zeynep', 'Celik', 'zeynep@test.com', '555-0004', 'Cancelled', 3, CURRENT_DATE - INTERVAL '100 days');

-- 5. Eğitmenler ve Odalar
INSERT INTO instructors (first_name, last_name, specialization) VALUES 
('John', 'Doe', 'Yoga Uzmanı'),
('Jane', 'Smith', 'Pilates Eğitmeni');

INSERT INTO rooms (room_name, capacity, location) VALUES 
('Studio A', 20, '1. Kat'),
('Studio B', 15, '2. Kat');

-- 6. Grup Dersleri
INSERT INTO group_classes (class_name, description, instructor_id, room_id, start_time, capacity) VALUES 
('Morning Yoga', 'Sabah yogası', 1, 1, CURRENT_TIMESTAMP, 20),
('Advanced Pilates', 'İleri seviye', 2, 2, CURRENT_TIMESTAMP + INTERVAL '1 day', 15);

-- 7. Ders Kayıtları ve Yoklama (Attendance)
-- Ali ve Ayşe derse gelmiş olsun. Mehmet hiç gelmemiş olsun (Rapor testi için önemli).
INSERT INTO class_enrollments (class_id, member_id, status) VALUES 
(1, 1, 'Confirmed'),
(1, 2, 'Confirmed');

INSERT INTO attendance (member_id, class_id, attendance_date, status) VALUES 
(1, 1, CURRENT_DATE, 'Present'), -- Ali geldi
(2, 1, CURRENT_DATE, 'Present'); -- Ayşe geldi
-- Mehmet için attendance eklemiyoruz!

-- 8. Ödemeler
INSERT INTO payments (member_id, amount, method, status) VALUES 
(1, 150.00, 'Credit Card', 'Paid'),
(2, 80.00, 'Cash', 'Paid');