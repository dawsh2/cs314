# ChocAn Data Processing System
Design Document

## 1. Introduction
This document describes the design and implementation of the ChocAn (Chocoholics Anonymous) data processing system, a software solution for managing healthcare services for chocolate addiction treatment.

### 1.1. Purpose and Scope
The purpose of this document is to detail the design decisions and implementation specifics of the ChocAn data processing system. The scope includes all data processing components specified in the requirements, including member management, provider interactions, service recording, and report generation. The design excludes communications software, terminal hardware design, accounting services, and EFT implementation, which are handled by other contractors.

### 1.2. Target Audience
This document is intended for:
- Software developers implementing or maintaining the ChocAn system
- System architects reviewing the design
- Project managers overseeing the implementation
- Quality assurance teams testing the system

### 1.3. Terms and Definitions
- **ChocAn**: Chocoholics Anonymous
- **Member**: An individual enrolled in ChocAn's healthcare program
- **Provider**: Healthcare professional providing services to ChocAn members
- **EFT**: Electronic Funds Transfer
- **Service Record**: Documentation of a healthcare service provided to a member
- **Provider Directory**: List of available services and their codes

## 2. Design Considerations

### 2.1. Constraints and Dependencies
1. **Technical Constraints**:
   - Terminal input/output must be simulated via keyboard and screen
   - Reports must be written to files rather than sent as email attachments
   - Member reports must be named using member name and date
   - Provider reports must follow similar naming convention

2. **Functional Constraints**:
   - Member numbers must be 9 digits
   - Provider numbers must be 9 digits
   - Service codes must be 6 digits
   - Comments limited to 100 characters
   - Name fields limited to 25 characters
   - Service names limited to 20 characters
   - City names limited to 14 characters
   - State codes must be 2 letters
   - ZIP codes must be 5 digits

### 2.2. Methodology
The system employs an object-oriented design methodology, chosen for its:
1. Natural mapping of real-world entities (members, providers, services) to classes
2. Encapsulation of data and operations
3. Modularity and maintainability
4. Easy extensibility for future features

Implementation uses Python for its:
- Rich standard library
- Clear syntax for rapid development
- Strong object-oriented support
- Cross-platform compatibility

## 3. System Overview
The ChocAn system consists of five main components:

1. **Data Management Layer**:
   - Member database
   - Provider database
   - Service records
   - Provider directory

2. **Terminal Interface Layer**:
   - Provider terminal simulation
   - Manager terminal simulation

3. **Service Processing Layer**:
   - Member validation
   - Service recording
   - Fee calculation

4. **Report Generation Layer**:
   - Member reports
   - Provider reports
   - Summary reports
   - EFT reports

5. **System Administration Layer**:
   - Member management
   - Provider management
   - System maintenance

## 4. System Architecture

### 4.1. Data Management Subsystem
The core classes managing system data:

#### 4.1.1. Member Class
```python
class Member:
    name: str  # 25 chars max
    number: str  # 9 digits
    street: str  # 25 chars max
    city: str  # 14 chars max
    state: str  # 2 letters
    zip_code: str  # 5 digits
    status: str  # active/suspended
```

#### 4.1.2. Provider Class
```python
class Provider:
    name: str  # 25 chars max
    number: str  # 9 digits
    street: str  # 25 chars max
    city: str  # 14 chars max
    state: str  # 2 letters
    zip_code: str  # 5 digits
    services_provided: List[ServiceRecord]
    weekly_consultations: int
    weekly_fee_total: float
```

#### 4.1.3. Service Class
```python
class Service:
    code: str  # 6 digits
    name: str  # 20 chars max
    fee: float
```

### 4.2. Service Processing Subsystem
Handles the core business logic:
- Member validation
- Service recording
- Fee calculation
- Transaction logging

### 4.3. Report Generation Subsystem
Manages all report creation:
- Member service reports
- Provider service reports
- EFT data reports
- Summary reports
- Provider directory

## 5. Detailed System Design

### 5.1. Data Management Implementation

#### 5.1.1. Data Storage
- In-memory storage using Python dictionaries for fast lookup
- Member and provider records indexed by their respective numbers
- Service records stored in chronological order
- File-based persistence for reports

#### 5.1.2. Data Validation
- Input validation for all fields
- Format checking for dates, numbers, and codes
- Status verification for members
- Duplicate checking for new records

### 5.2. Service Processing Implementation
The service processing workflow:

1. **Member Validation**:
```python
def validate_member(member_number):
    if member_number not in members:
        return "Invalid Number"
    if members[member_number].status == "suspended":
        return "Member suspended"
    return "Validated"
```

2. **Service Recording**:
```python
def process_service(member_number, provider_number, 
                   service_date, service_code, comments=""):
    # Validate inputs
    # Create service record
    # Update provider statistics
    # Return confirmation
```

### 5.3. Report Generation Implementation

1. **Member Reports**:
- Generated weekly or on-demand
- Sorted by service date
- Includes all required fields
- Named using member name and date

2. **Provider Reports**:
- Generated weekly or on-demand
- Includes service details and summaries
- Calculates total consultations and fees
- Named using provider name and date

3. **Summary Reports**:
- Aggregates all provider activities
- Calculates system-wide totals
- Supports management decision-making

4. **EFT Reports**:
- Contains provider payment information
- Structured for banking system integration
- Includes verification totals
