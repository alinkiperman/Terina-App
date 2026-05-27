-- Create database
-- DROP DATABASE IF EXISTS terina_app;
CREATE DATABASE terina_app;
USE terina_app;

-- ========================
-- 1. Patient
-- ========================
CREATE TABLE Patient (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(100),
    consent_status BOOLEAN DEFAULT FALSE,

    -- The most updated medical profile of the patient
    current_profile_id INT NULL
);

-- ========================
-- 2. Medical Profile
-- ========================
CREATE TABLE Medical_Profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,

    -- Timestamp for tracking profile history over time
    profile_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Indicates whether this is the current medical profile
    is_current BOOLEAN DEFAULT TRUE,

    diabetes BOOLEAN,
    hypertension BOOLEAN,
    cardiovascular BOOLEAN,
    neurological BOOLEAN,
    smoking_status VARCHAR(20),
    physical_activity VARCHAR(20),
    sleep_hours FLOAT,

    -- Changed from Alzheimer family history to diabetes family history
    family_history_diabetes BOOLEAN,

    medications TEXT,

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
        ON DELETE CASCADE
);

-- Link Patient to the most updated Medical_Profile
ALTER TABLE Patient
ADD CONSTRAINT fk_patient_current_profile
FOREIGN KEY (current_profile_id) REFERENCES Medical_Profile(profile_id)
    ON DELETE SET NULL;

-- ========================
-- 3. Scan Session
-- ========================
CREATE TABLE Scan_Session (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    scan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    eye VARCHAR(2),  -- OD / OS
    quality_score FLOAT,
    data_source VARCHAR(50), -- upload / simulated / external
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
        ON DELETE CASCADE
);

-- ========================
-- 4. OCT Image
-- ========================
CREATE TABLE OCT_Image (
    oct_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    filename VARCHAR(255),
    scan_index INT,
    DME INT,
    DR VARCHAR(20),
    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
        ON DELETE CASCADE
);

-- ========================
-- 5. Fundus Image
-- ========================
CREATE TABLE Fundus_Image (
    fundus_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    filename VARCHAR(255),
    scan_index INT,
    DME INT,
    DR VARCHAR(20),
    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
        ON DELETE CASCADE
);

-- ========================
-- 6. Analysis Result
-- ========================
CREATE TABLE Analysis_Result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    risk_score FLOAT,
    disease_status VARCHAR(50),
    confidence_score FLOAT,
    trend VARCHAR(20),
    recommendation TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
        ON DELETE CASCADE
);