DROP DATABASE IF EXISTS terina_app;
CREATE DATABASE terina_app;
USE terina_app;

CREATE TABLE Patient (
    patient_id VARCHAR(4) PRIMARY KEY,
    full_name VARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    phone VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE Scan_Session (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(4) NOT NULL,
    session_date DATE NOT NULL,
    scan_type VARCHAR(20),    -- OCT / Fundus / Fundus, OCT

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
	UNIQUE (patient_id, scan_type, session_date)
);

CREATE TABLE Medical_Profile (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id VARCHAR(4) NOT NULL,
    session_id INT NOT NULL,
    diabetes BOOLEAN,
    family_history_diabetes BOOLEAN,
    hypertension BOOLEAN,
    vision_problems BOOLEAN,
    previous_eye_disease BOOLEAN,
    profile_date DATE NOT NULL,

    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id),
    UNIQUE (session_id)
);




CREATE TABLE Fundus (
    name VARCHAR(255) PRIMARY KEY,
    session_id INT NOT NULL,
    eye_side VARCHAR(10),
    DME TINYINT,
    DR ENUM('0', 'NPDR', 'PDR') NULL,

    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
);

CREATE TABLE OCT (
    name VARCHAR(255) PRIMARY KEY,
    session_id INT NOT NULL,
    eye_side VARCHAR(10),
    DME TINYINT,
    DR ENUM('0', 'NPDR', 'PDR') NULL,

    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
);

CREATE TABLE Analysis_Results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    modality VARCHAR(20),        
    image_name VARCHAR(255),
    DME TINYINT,
    DR ENUM('0', 'NPDR', 'PDR') NULL,
    confidence_score FLOAT,
    risk_score FLOAT,
    severity_level ENUM('Low', 'Moderate', 'High', 'Critical'),
    clinical_summary TEXT,
    recommendation TEXT,
    analysis_date DATE,

    FOREIGN KEY (session_id) REFERENCES Scan_Session(session_id)
);
