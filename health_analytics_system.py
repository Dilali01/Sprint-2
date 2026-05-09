""" 
HEALTH DATA ANALYTICS SYSTEM 
Milestone 3 & 4 - Live Presentation Code 
""" 
import json 
import os 
from datetime import date 
from collections import deque 
import pandas as pd 
from typing import List, Dict 
 
# ====================== MILESTONE 4: CUSTOM EXCEPTIONS ====================== 
class InvalidHealthDataError(Exception): 
    pass 
 
class PatientNotFoundError(Exception): 
    pass 
 
 
# ====================== PATIENT CLASS (OOP + Data Structures) ====================== 
class Patient: 
    def __init__(self, patient_id: str, name: str, age: int, gender: str): 
        self.patient_id = patient_id 
        self.name = name 
        self.age = age 
        self.gender = gender 
        self.records: List[Dict] = []      # List 
        self.conditions: set = set()       # Set 
 
    def add_record(self, record: Dict): 
        if not all(k in record for k in ['date', 'blood_pressure', 'heart_rate', 'temperature']): 
            raise InvalidHealthDataError("Missing required fields") 
        if not (30 <= record['heart_rate'] <= 200): 
            raise InvalidHealthDataError("Invalid heart rate") 
         
        self.records.append(record) 
        if record.get('condition'): 
            self.conditions.add(record['condition']) 
 
 
# ====================== MILESTONE 3: FUNCTIONAL PROGRAMMING ====================== 
def clean_record(record: Dict) -> Dict: 
    """Pure function to clean data""" 
    cleaned = record.copy() 
    cleaned['date'] = pd.to_datetime(cleaned['date']).date() 
    if isinstance(cleaned.get('blood_pressure'), str): 
        cleaned['blood_pressure'] = tuple(map(int, cleaned['blood_pressure'].split('/'))) 
    return cleaned 
 
 
def calculate_stats(records: List[Dict]) -> Dict: 
    """Calculate metrics""" 
    if not records: 
        return {"message": "No records"} 
     
    df = pd.DataFrame(records) 
    return { 
        "total_records": len(records), 
        "avg_heart_rate": round(float(df['heart_rate'].mean()), 1), 
        "avg_temperature": round(float(df['temperature'].mean()), 1), 
        "max_bp_systolic": int(df['blood_pressure'].apply(lambda x: x[0]).max()) 
    } 
 
 
def detect_anomalies(records: List[Dict]) -> List[Dict]: 
    """Find abnormal readings using filter""" 
    def is_anomaly(r): 
        return r.get('heart_rate', 70) < 55 or r.get('heart_rate', 70) > 110 
    return list(filter(is_anomaly, records)) 
 
 
def health_data_pipeline(records: List[Dict]) -> Dict: 
    """Full Functional Data Pipeline - Milestone 3 Core""" 
    cleaned_records = list(map(clean_record, records)) 
    stats = calculate_stats(cleaned_records) 
    anomalies = detect_anomalies(cleaned_records) 
     
    return { 
        **stats, 
        "anomalies_detected": len(anomalies), 
        "anomalies": anomalies[:2]   # Show max 2 anomalies 
    } 
 
 
# ====================== MILESTONE 4: DESIGN PATTERNS ====================== 
 
# Strategy Pattern 
class AnalysisStrategy: 
    def analyze(self, patient: Patient) -> Dict: 
        raise NotImplementedError 
 
class BasicStatsStrategy(AnalysisStrategy): 
    def analyze(self, patient: Patient) -> Dict: 
        return health_data_pipeline(patient.records) 
 
 
# Observer Pattern (Simple) 
class PatientObserver: 
    def update(self, patient: Patient, message: str): 
        print(f"     ALERT: {patient.name} ({patient.patient_id}) - {message}") 
 
 
# ====================== MAIN SYSTEM ====================== 
class HealthAnalyticsSystem: 
    def __init__(self): 
        self.patients: Dict[str, Patient] = {}      # Dictionary 
        self.analysis_queue: deque = deque()        # Queue 
        self.observer = PatientObserver() 
 
    def add_patient(self, patient: Patient): 
        self.patients[patient.patient_id] = patient 
        print(f"✓ Patient {patient.name} added successfully.") 
 
    def add_record(self, patient_id: str, record: Dict): 
        if patient_id not in self.patients: 
            raise PatientNotFoundError(f"Patient {patient_id} not found") 
         
        patient = self.patients[patient_id] 
        patient.add_record(record) 
        self.analysis_queue.append(patient_id) 
        self.observer.update(patient, "New health record added") 
 
 
# ====================== LIVE DEMO - MILESTONE 3 FIRST ====================== 
if __name__ == "__main__": 
    print("=" * 65) 
    print("HEALTH DATA ANALYTICS SYSTEM - MILESTONE 3 & 4") 
    print("=" * 65) 
 
    system = HealthAnalyticsSystem() 
 
    # Create patients 
    p1 = Patient("P001", "John Doe", 45, "Male") 
    system.add_patient(p1) 
 
    # Add sample records 
    sample_records = [ 
        {"date": "2025-04-01", "blood_pressure": "120/80", "heart_rate": 76, "temperature": 36.8}, 
        {"date": "2025-04-02", "blood_pressure": "135/85", "heart_rate": 98, "temperature": 37.4}, 
        {"date": "2025-04-03", "blood_pressure": "110/70", "heart_rate": 48, "temperature": 34.9}   # Anomaly 
    ] 
 
    print("\n--- Adding Health Records ---") 
    for record in sample_records: 
        system.add_record("P001", record) 
 
    print("\n" + "="*65) 
    print("MILESTONE 3: FUNCTIONAL DATA PIPELINE") 
    print("="*65) 
     
    result = health_data_pipeline(p1.records) 
    print(json.dumps(result, indent=2, default=str)) 
 
    print("\n" + "="*65) 
    print("MILESTONE 4: DESIGN PATTERNS DEMO") 
    print("="*65) 
     
    strategy = BasicStatsStrategy() 
    strategy_result = strategy.analyze(p1) 
    print("Strategy Pattern Result:") 
    print(json.dumps(strategy_result, indent=2, default=str)) 
 
    print("\n" + "="*65) 
    print("    DEMO COMPLETE") 
    print("Milestone 3: Data Structures + Functional Pipeline Done") 
    print("Milestone 4: Exceptions + Strategy + Observer Patterns Done") 
    print("="*65)
