from datetime import datetime
import json
import os

class Member:
    def __init__(self, name, number, street, city, state, zip_code):
        self.name = name[:25]  # Limit to 25 characters
        self.number = str(number).zfill(9)  # Ensure 9 digits
        self.street = street[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = str(zip_code).zfill(5)
        self.status = "active"  # or "suspended"

class Provider:
    def __init__(self, name, number, street, city, state, zip_code):
        self.name = name[:25]
        self.number = str(number).zfill(9)
        self.street = street[:25]
        self.city = city[:14]
        self.state = state[:2]
        self.zip_code = str(zip_code).zfill(5)
        self.services_provided = []
        self.weekly_consultations = 0
        self.weekly_fee_total = 0.0

class Service:
    def __init__(self, code, name, fee):
        self.code = str(code).zfill(6)
        self.name = name[:20]
        self.fee = float(fee)

class ServiceRecord:
    def __init__(self, current_datetime, service_date, provider_number, 
                 member_number, service_code, comments=""):
        self.current_datetime = current_datetime
        self.service_date = service_date
        self.provider_number = provider_number
        self.member_number = member_number
        self.service_code = service_code
        self.comments = comments[:100]  # Limit comments to 100 characters

class ChocAnSystem:
    def __init__(self):
        self.members = {}  # key: member_number, value: Member object
        self.providers = {}  # key: provider_number, value: Provider object
        self.services = {}  # key: service_code, value: Service object
        self.service_records = []
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        # Initialize some sample services
        self.services = {
            "598470": Service("598470", "Dietitian Session", 50.00),
            "883948": Service("883948", "Aerobics Session", 45.00),
        }

    def validate_member(self, member_number):
        if member_number not in self.members:
            return "Invalid Number"
        member = self.members[member_number]
        if member.status == "suspended":
            return "Member suspended"
        return "Validated"

    def process_service(self, member_number, provider_number, service_date, service_code, comments=""):
        # Validate member
        validation_result = self.validate_member(member_number)
        if validation_result != "Validated":
            return validation_result

        # Validate service code
        if service_code not in self.services:
            return "Invalid service code"

        # Create service record
        current_datetime = datetime.now()
        record = ServiceRecord(
            current_datetime.strftime("%m-%d-%Y %H:%M:%S"),
            service_date,
            provider_number,
            member_number,
            service_code,
            comments
        )
        self.service_records.append(record)
        
        # Update provider's weekly totals
        provider = self.providers[provider_number]
        provider.services_provided.append(record)
        provider.weekly_consultations += 1
        provider.weekly_fee_total += self.services[service_code].fee

        return f"Service recorded. Fee: ${self.services[service_code].fee:.2f}"

    def generate_member_report(self, member_number):
        member = self.members[member_number]
        filename = f"{member.name}_{datetime.now().strftime('%Y%m%d')}_report.txt"

        with open(filename, "w") as f:
            f.write(f"Member Report for {member.name}\n")
            f.write(f"Member Number: {member.number}\n")
            f.write(f"Address: {member.street}\n")
            f.write(f"         {member.city}, {member.state} {member.zip_code}\n\n")
            f.write("Services Received:\n")
            
            # Filter and sort services for this member
            member_services = [
                record for record in self.service_records 
                if record.member_number == member_number
            ]
            member_services.sort(key=lambda x: x.service_date)

            for record in member_services:
                service = self.services[record.service_code]
                provider = self.providers[record.provider_number]
                f.write(f"Date: {record.service_date}\n")
                f.write(f"Provider: {provider.name}\n")
                f.write(f"Service: {service.name}\n\n")

    def generate_provider_report(self, provider_number):
        provider = self.providers[provider_number]
        filename = f"{provider.name}_{datetime.now().strftime('%Y%m%d')}_report.txt"

        with open(filename, "w") as f:
            f.write(f"Provider Report for {provider.name}\n")
            f.write(f"Provider Number: {provider.number}\n")
            f.write(f"Address: {provider.street}\n")
            f.write(f"         {provider.city}, {provider.state} {provider.zip_code}\n\n")
            f.write("Services Provided:\n")

            for record in provider.services_provided:
                service = self.services[record.service_code]
                member = self.members[record.member_number]
                f.write(f"Date of Service: {record.service_date}\n")
                f.write(f"Computer DateTime: {record.current_datetime}\n")
                f.write(f"Member: {member.name} (#{record.member_number})\n")
                f.write(f"Service Code: {record.service_code}\n")
                f.write(f"Fee: ${service.fee:.2f}\n\n")

            f.write(f"Total Consultations: {provider.weekly_consultations}\n")
            f.write(f"Total Fees: ${provider.weekly_fee_total:.2f}\n")

    def generate_provider_directory(self):
        filename = f"provider_directory_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(filename, "w") as f:
            f.write("ChocAn Provider Directory\n\n")
            
            # Sort services by name
            sorted_services = sorted(
                self.services.values(), 
                key=lambda x: x.name
            )
            
            for service in sorted_services:
                f.write(f"Service: {service.name}\n")
                f.write(f"Code: {service.code}\n")
                f.write(f"Fee: ${service.fee:.2f}\n\n")

    def generate_eft_report(self):
        filename = f"eft_data_{datetime.now().strftime('%Y%m%d')}.txt"
        
        with open(filename, "w") as f:
            for provider in self.providers.values():
                if provider.weekly_fee_total > 0:
                    f.write(f"Provider: {provider.name}\n")
                    f.write(f"Number: {provider.number}\n")
                    f.write(f"Transfer Amount: ${provider.weekly_fee_total:.2f}\n\n")

    def generate_summary_report(self):
        filename = f"summary_report_{datetime.now().strftime('%Y%m%d')}.txt"
        
        total_providers = 0
        total_consultations = 0
        total_fees = 0.0
        
        with open(filename, "w") as f:
            f.write("Weekly Summary Report\n\n")
            
            for provider in self.providers.values():
                if provider.weekly_consultations > 0:
                    total_providers += 1
                    total_consultations += provider.weekly_consultations
                    total_fees += provider.weekly_fee_total
                    
                    f.write(f"Provider: {provider.name}\n")
                    f.write(f"Consultations: {provider.weekly_consultations}\n")
                    f.write(f"Fees: ${provider.weekly_fee_total:.2f}\n\n")
            
            f.write(f"Total Providers: {total_providers}\n")
            f.write(f"Total Consultations: {total_consultations}\n")
            f.write(f"Total Fees: ${total_fees:.2f}\n")

    def add_member(self, name, number, street, city, state, zip_code):
        member = Member(name, number, street, city, state, zip_code)
        self.members[member.number] = member
        return "Member added successfully"

    def add_provider(self, name, number, street, city, state, zip_code):
        provider = Provider(name, number, street, city, state, zip_code)
        self.providers[provider.number] = provider
        return "Provider added successfully"

    def delete_member(self, member_number):
        if member_number in self.members:
            del self.members[member_number]
            return "Member deleted successfully"
        return "Member not found"

    def delete_provider(self, provider_number):
        if provider_number in self.providers:
            del self.providers[provider_number]
            return "Provider deleted successfully"
        return "Provider not found"

    def update_member(self, member_number, **kwargs):
        if member_number not in self.members:
            return "Member not found"
        
        member = self.members[member_number]
        for key, value in kwargs.items():
            if hasattr(member, key):
                setattr(member, key, value)
        return "Member updated successfully"

    def update_provider(self, provider_number, **kwargs):
        if provider_number not in self.providers:
            return "Provider not found"
        
        provider = self.providers[provider_number]
        for key, value in kwargs.items():
            if hasattr(provider, key):
                setattr(provider, key, value)
        return "Provider updated successfully"

# Example usage and testing
def main():
    # Initialize the system
    system = ChocAnSystem()
    
    # Add a sample member
    system.add_member(
        "John Doe",
        "123456789",
        "123 Chocolate St",
        "Sweet City",
        "SC",
        "12345"
    )
    
    # Add a sample provider
    system.add_provider(
        "Dr. Cocoa",
        "987654321",
        "456 Sugar Ave",
        "Candy City",
        "CC",
        "54321"
    )
    
    # Process a service
    result = system.process_service(
        "123456789",  # member number
        "987654321",  # provider number
        "11-01-2024",  # service date
        "598470",     # service code
        "Initial consultation"  # comments
    )
    print(result)
    
    # Generate reports
    system.generate_member_report("123456789")
    system.generate_provider_report("987654321")
    system.generate_provider_directory()
    system.generate_eft_report()
    system.generate_summary_report()

if __name__ == "__main__":
    main()
