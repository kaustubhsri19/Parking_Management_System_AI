-- AI Powered Voice-to-Query Parking Management System
-- Supabase Database Schema
-- Run these commands in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_no VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type VARCHAR(50) NOT NULL CHECK (vehicle_type IN ('car', 'motorcycle', 'truck', 'van', 'bus')),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create parking_slots table
CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id SERIAL PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'available' CHECK (status IN ('available', 'booked', 'maintenance', 'reserved')),
    floor_no INTEGER NOT NULL DEFAULT 1,
    slot_type VARCHAR(20) NOT NULL DEFAULT 'standard' CHECK (slot_type IN ('standard', 'premium', 'disabled', 'electric')),
    hourly_rate DECIMAL(10,2) DEFAULT 5.00,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create parking_logs table
CREATE TABLE IF NOT EXISTS parking_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vehicle_id UUID REFERENCES vehicles(vehicle_id) ON DELETE SET NULL,
    slot_id INTEGER REFERENCES parking_slots(slot_id) ON DELETE SET NULL,
    entry_time TIMESTAMP WITH TIME ZONE NOT NULL,
    exit_time TIMESTAMP WITH TIME ZONE,
    total_amount DECIMAL(10,2) DEFAULT 0.00,
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_vehicles_user_id ON vehicles(user_id);
CREATE INDEX IF NOT EXISTS idx_vehicles_vehicle_no ON vehicles(vehicle_no);
CREATE INDEX IF NOT EXISTS idx_parking_slots_status ON parking_slots(status);
CREATE INDEX IF NOT EXISTS idx_parking_slots_floor ON parking_slots(floor_no);
CREATE INDEX IF NOT EXISTS idx_parking_logs_vehicle_id ON parking_logs(vehicle_id);
CREATE INDEX IF NOT EXISTS idx_parking_logs_slot_id ON parking_logs(slot_id);
CREATE INDEX IF NOT EXISTS idx_parking_logs_entry_time ON parking_logs(entry_time);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_vehicles_updated_at BEFORE UPDATE ON vehicles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_parking_slots_updated_at BEFORE UPDATE ON parking_slots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data
INSERT INTO users (name, phone, email) VALUES
('John Doe', '+1234567890', 'john.doe@email.com'),
('Jane Smith', '+1234567891', 'jane.smith@email.com'),
('Bob Johnson', '+1234567892', 'bob.johnson@email.com'),
('Alice Brown', '+1234567893', 'alice.brown@email.com'),
('Charlie Wilson', '+1234567894', 'charlie.wilson@email.com');

-- Insert sample vehicles
INSERT INTO vehicles (vehicle_no, vehicle_type, user_id) VALUES
('ABC-123', 'car', (SELECT user_id FROM users WHERE email = 'john.doe@email.com')),
('XYZ-789', 'motorcycle', (SELECT user_id FROM users WHERE email = 'jane.smith@email.com')),
('DEF-456', 'car', (SELECT user_id FROM users WHERE email = 'bob.johnson@email.com')),
('GHI-321', 'truck', (SELECT user_id FROM users WHERE email = 'alice.brown@email.com')),
('JKL-654', 'van', (SELECT user_id FROM users WHERE email = 'charlie.wilson@email.com'));

-- Insert sample parking slots
INSERT INTO parking_slots (location, status, floor_no, slot_type, hourly_rate) VALUES
('A1', 'available', 1, 'standard', 5.00),
('A2', 'available', 1, 'standard', 5.00),
('A3', 'booked', 1, 'premium', 8.00),
('A4', 'available', 1, 'standard', 5.00),
('A5', 'available', 1, 'electric', 6.00),
('B1', 'available', 2, 'standard', 5.00),
('B2', 'available', 2, 'premium', 8.00),
('B3', 'available', 2, 'disabled', 3.00),
('B4', 'booked', 2, 'standard', 5.00),
('B5', 'available', 2, 'electric', 6.00),
('C1', 'maintenance', 3, 'standard', 5.00),
('C2', 'available', 3, 'premium', 8.00),
('C3', 'available', 3, 'standard', 5.00),
('C4', 'available', 3, 'electric', 6.00),
('C5', 'available', 3, 'standard', 5.00);

-- Insert sample parking logs
INSERT INTO parking_logs (vehicle_id, slot_id, entry_time, exit_time, total_amount, payment_status) VALUES
((SELECT vehicle_id FROM vehicles WHERE vehicle_no = 'ABC-123'), 3, NOW() - INTERVAL '2 hours', NOW() - INTERVAL '30 minutes', 7.50, 'paid'),
((SELECT vehicle_id FROM vehicles WHERE vehicle_no = 'XYZ-789'), 4, NOW() - INTERVAL '1 hour', NULL, 0.00, 'pending'),
((SELECT vehicle_id FROM vehicles WHERE vehicle_no = 'DEF-456'), 9, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour', 10.00, 'paid');

-- Create a view for available slots with details
CREATE OR REPLACE VIEW available_slots_view AS
SELECT 
    slot_id,
    location,
    floor_no,
    slot_type,
    hourly_rate,
    created_at
FROM parking_slots 
WHERE status = 'available'
ORDER BY floor_no, location;

-- Create a view for current parking status
CREATE OR REPLACE VIEW current_parking_status AS
SELECT 
    pl.log_id,
    pl.entry_time,
    pl.total_amount,
    pl.payment_status,
    v.vehicle_no,
    v.vehicle_type,
    u.name as owner_name,
    ps.location,
    ps.floor_no,
    ps.slot_type
FROM parking_logs pl
JOIN vehicles v ON pl.vehicle_id = v.vehicle_id
JOIN users u ON v.user_id = u.user_id
JOIN parking_slots ps ON pl.slot_id = ps.slot_id
WHERE pl.exit_time IS NULL
ORDER BY pl.entry_time DESC;

-- Grant necessary permissions (adjust as needed for your setup)
-- These commands should be run by a superuser or the database owner

-- Grant usage on schema
GRANT USAGE ON SCHEMA public TO anon, authenticated;

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO anon, authenticated;

-- Grant sequence permissions
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Grant view permissions
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon, authenticated;

-- Enable Row Level Security (RLS) - optional but recommended for production
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE parking_slots ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE parking_logs ENABLE ROW LEVEL SECURITY;

-- Create policies for RLS (uncomment and modify as needed)
-- CREATE POLICY "Users can view their own data" ON users FOR SELECT USING (auth.uid() = user_id);
-- CREATE POLICY "Users can update their own data" ON users FOR UPDATE USING (auth.uid() = user_id);
-- CREATE POLICY "Anyone can view parking slots" ON parking_slots FOR SELECT USING (true);
-- CREATE POLICY "Anyone can view parking logs" ON parking_logs FOR SELECT USING (true);
