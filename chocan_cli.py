import sys
from datetime import datetime
from chocan_system import ChocAnSystem

class ChocAnCLI:
    def __init__(self):
        self.system = ChocAnSystem()
        self.current_provider = None

    def provider_terminal(self):
        """Simulate provider terminal interface"""
        print("\nChocAn Provider Terminal")
        provider_number = input("Enter provider number (9 digits): ")
        
        if provider_number not in self.system.providers:
            print("Error: Invalid provider number")
            return
        
        self.current_provider = self.system.providers[provider_number]
        print(f"\nWelcome, {self.current_provider.name}")
        
        while True:
            print("\nProvider Menu:")
            print("1. Process member service")
            print("2. Request Provider Directory")
            print("3. View weekly summary")
            print("4. Exit terminal")
            
            choice = input("\nEnter choice (1-4): ")
            
            if choice == "1":
                self.process_service()
            elif choice == "2":
                self.system.generate_provider_directory()
                print("\nProvider Directory has been generated.")
            elif choice == "3":
                self.system.generate_provider_report(self.current_provider.number)
                print("\nWeekly report has been generated.")
            elif choice == "4":
                print("\nLogging out...")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def process_service(self):
        """Handle service processing workflow"""
        print("\nProcess Service")
        member_number = input("Enter member number (or swipe card): ")
        
        # Validate member
        validation_result = self.system.validate_member(member_number)
        print(f"\nMember Status: {validation_result}")
        
        if validation_result != "Validated":
            return
        
        # Get service details
        service_date = input("Enter service date (MM-DD-YYYY): ")
        
        # Display available services
        print("\nAvailable Services:")
        for code, service in self.system.services.items():
            print(f"{code}: {service.name} - ${service.fee:.2f}")
        
        service_code = input("\nEnter service code: ")
        
        if service_code not in self.system.services:
            print("Error: Invalid service code")
            return
        
        # Confirm service
        service = self.system.services[service_code]
        print(f"\nSelected service: {service.name}")
        confirm = input("Is this correct? (y/n): ")
        
        if confirm.lower() != 'y':
            return
        
        comments = input("Enter any comments (optional): ")
        
        # Process the service
        result = self.system.process_service(
            member_number,
            self.current_provider.number,
            service_date,
            service_code,
            comments
        )
        
        print(f"\n{result}")

    def manager_terminal(self):
        """Simulate manager terminal interface"""
        while True:
            print("\nChocAn Manager Terminal")
            print("1. Generate Reports")
            print("2. Manage Members")
            print("3. Manage Providers")
            print("4. Exit")
            
            choice = input("\nEnter choice (1-4): ")
            
            if choice == "1":
                self.manager_reports_menu()
            elif choice == "2":
                self.manage_members()
            elif choice == "3":
                self.manage_providers()
            elif choice == "4":
                print("\nExiting manager terminal...")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def manager_reports_menu(self):
        """Handle manager report generation options"""
        while True:
            print("\nReport Generation Menu:")
            print("1. Generate All Reports")
            print("2. Generate Member Report")
            print("3. Generate Provider Report")
            print("4. Generate Summary Report")
            print("5. Generate EFT Report")
            print("6. Return to Main Menu")
            
            choice = input("\nEnter choice (1-6): ")
            
            if choice == "1":
                # Generate all reports
                for member_number in self.system.members:
                    self.system.generate_member_report(member_number)
                for provider_number in self.system.providers:
                    self.system.generate_provider_report(provider_number)
                self.system.generate_summary_report()
                self.system.generate_eft_report()
                print("\nAll reports have been generated.")
            
            elif choice == "2":
                member_number = input("\nEnter member number: ")
                if member_number in self.system.members:
                    self.system.generate_member_report(member_number)
                    print("\nMember report has been generated.")
                else:
                    print("\nMember not found.")
            
            elif choice == "3":
                provider_number = input("\nEnter provider number: ")
                if provider_number in self.system.providers:
                    self.system.generate_provider_report(provider_number)
                    print("\nProvider report has been generated.")
                else:
                    print("\nProvider not found.")
            
            elif choice == "4":
                self.system.generate_summary_report()
                print("\nSummary report has been generated.")
            
            elif choice == "5":
                self.system.generate_eft_report()
                print("\nEFT report has been generated.")
            
            elif choice == "6":
                break
            
            else:
                print("\nInvalid choice. Please try again.")

    def manage_members(self):
        """Handle member management operations"""
        while True:
            print("\nMember Management Menu:")
            print("1. Add Member")
            print("2. Delete Member")
            print("3. Update Member")
            print("4. View Member")
            print("5. Return to Main Menu")
            
            choice = input("\nEnter choice (1-5): ")
            
            if choice == "1":
                name = input("Enter member name: ")
                number = input("Enter member number (9 digits): ")
                street = input("Enter street address: ")
                city = input("Enter city: ")
                state = input("Enter state (2 letters): ")
                zip_code = input("Enter ZIP code (5 digits): ")
                
                result = self.system.add_member(name, number, street, city, state, zip_code)
                print(f"\n{result}")
            
            elif choice == "2":
                number = input("Enter member number: ")
                result = self.system.delete_member(number)
                print(f"\n{result}")
            
            elif choice == "3":
                number = input("Enter member number: ")
                if number in self.system.members:
                    print("\nEnter new information (press Enter to keep current value):")
                    member = self.system.members[number]
                    
                    name = input(f"Name [{member.name}]: ") or member.name
                    street = input(f"Street [{member.street}]: ") or member.street
                    city = input(f"City [{member.city}]: ") or member.city
                    state = input(f"State [{member.state}]: ") or member.state
                    zip_code = input(f"ZIP [{member.zip_code}]: ") or member.zip_code
                    
                    result = self.system.update_member(
                        number,
                        name=name,
                        street=street,
                        city=city,
                        state=state,
                        zip_code=zip_code
                    )
                    print(f"\n{result}")
                else:
                    print("\nMember not found.")
            
            elif choice == "4":
                number = input("Enter member number: ")
                if number in self.system.members:
                    member = self.system.members[number]
                    print(f"\nMember Details:")
                    print(f"Name: {member.name}")
                    print(f"Number: {member.number}")
                    print(f"Address: {member.street}")
                    print(f"         {member.city}, {member.state} {member.zip_code}")
                    print(f"Status: {member.status}")
                else:
                    print("\nMember not found.")
            
            elif choice == "5":
                break
            
            else:
                print("\nInvalid choice. Please try again.")

    def manage_providers(self):
        """Handle provider management operations"""
        while True:
            print("\nProvider Management Menu:")
            print("1. Add Provider")
            print("2. Delete Provider")
            print("3. Update Provider")
            print("4. View Provider")
            print("5. Return to Main Menu")
            
            choice = input("\nEnter choice (1-5): ")
            
            if choice == "1":
                name = input("Enter provider name: ")
                number = input("Enter provider number (9 digits): ")
                street = input("Enter street address: ")
                city = input("Enter city: ")
                state = input("Enter state (2 letters): ")
                zip_code = input("Enter ZIP code (5 digits): ")
                
                result = self.system.add_provider(name, number, street, city, state, zip_code)
                print(f"\n{result}")
            
            elif choice == "2":
                number = input("Enter provider number: ")
                result = self.system.delete_provider(number)
                print(f"\n{result}")
            
            elif choice == "3":
                number = input("Enter provider number: ")
                if number in self.system.providers:
                    print("\nEnter new information (press Enter to keep current value):")
                    provider = self.system.providers[number]
                    
                    name = input(f"Name [{provider.name}]: ") or provider.name
                    street = input(f"Street [{provider.street}]: ") or provider.street
                    city = input(f"City [{provider.city}]: ") or provider.city
                    state = input(f"State [{provider.state}]: ") or provider.state
                    zip_code = input(f"ZIP [{provider.zip_code}]: ") or provider.zip_code
                    
                    result = self.system.update_provider(
                        number,
                        name=name,
                        street=street,
                        city=city,
                        state=state,
                        zip_code=zip_code
                    )
                    print(f"\n{result}")
                else:
                    print("\nProvider not found.")
            
            elif choice == "4":
                number = input("Enter provider number: ")
                if number in self.system.providers:
                    provider = self.system.providers[number]
                    print(f"\nProvider Details:")
                    print(f"Name: {provider.name}")
                    print(f"Number: {provider.number}")
                    print(f"Address: {provider.street}")
                    print(f"         {provider.city}, {provider.state} {provider.zip_code}")
                    print(f"Weekly consultations: {provider.weekly_consultations}")
                    print(f"Weekly fees: ${provider.weekly_fee_total:.2f}")
                else:
                    print("\nProvider not found.")
            
            elif choice == "5":
                break
            
            else:
                print("\nInvalid choice. Please try again.")

def main():
    cli = ChocAnCLI()
    
    while True:
        print("\nChocAn Terminal System")
        print("1. Provider Terminal")
        print("2. Manager Terminal")
        print("3. Exit")
        
        choice = input("\nEnter choice (1-3): ")
        
        if choice == "1":
            cli.provider_terminal()
        elif choice == "2":
            cli.manager_terminal()
        elif choice == "3":
            print("\nExiting ChocAn system...")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
