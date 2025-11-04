#!/usr/bin/env python3
"""
Email Verifier Application
A Python application that verifies email addresses using port 25 and detects disposable emails
"""

import socket
import smtplib
import re
import json
import sys
from typing import Dict, Any

class EmailVerifier:
    def __init__(self):
        # List of known disposable email domains
        self.disposable_domains = {
            '10minutemail.com', 'guerrillamail.com', 'mailinator.com', 
            'tempmail.org', 'temp-mail.org', 'yopmail.com', 'throwaway.email',
            'maildrop.cc', 'sharklasers.com', 'guerrillamailblock.com',
            'pokemail.net', 'spam4.me', 'bccto.me', 'chacuo.net',
            'dispostable.com', 'fakeinbox.com', 'fantastu.com'
        }
    
    def is_valid_email_format(self, email: str) -> bool:
        """Check if email has valid format using regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_disposable_email(self, email: str) -> bool:
        """Check if email domain is in disposable email list"""
        domain = email.split('@')[1].lower()
        return domain in self.disposable_domains
    
    def verify_email_smtp(self, email: str) -> bool:
        """Verify email using SMTP connection on port 25"""
        try:
            # Extract domain from email
            domain = email.split('@')[1]
            
            # Get MX record for domain
            mx_record = self.get_mx_record(domain)
            if not mx_record:
                return False
            
            # Connect to SMTP server on port 25
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_record, 25)
            server.helo('localhost')
            server.mail('test@example.com')
            
            # Try to verify the recipient
            code, message = server.rcpt(email)
            server.quit()
            
            # Check if email is accepted (codes 250, 251, 252 indicate success)
            return code in [250, 251, 252]
            
        except Exception as e:
            print(f"SMTP verification error: {e}")
            return False
    
    def get_mx_record(self, domain: str) -> str:
        """Get MX record for domain"""
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            if mx_records:
                # Return the MX record with lowest priority
                mx_record = min(mx_records, key=lambda x: x.preference)
                return str(mx_record.exchange).rstrip('.')
        except:
            # Fallback: try to connect directly to domain
            try:
                socket.gethostbyname(domain)
                return domain
            except:
                return None
        return None
    
    def verify_email(self, email: str) -> Dict[str, Any]:
        """Main verification function that returns all required information"""
        result = {
            'email': email,
            'email_verified': False,
            'is_disposable': False,
            'format_valid': False
        }
        
        # Check email format
        if not self.is_valid_email_format(email):
            return result
        
        result['format_valid'] = True
        
        # Check if disposable
        result['is_disposable'] = self.is_disposable_email(email)
        
        # Verify email using SMTP (port 25)
        result['email_verified'] = self.verify_email_smtp(email)
        
        return result

def main():
    """Main function to run the email verifier"""
    verifier = EmailVerifier()
    
    print("Email Verifier Application")
    print("=" * 30)
    
    while True:
        try:
            # Get email input from user
            email = input("\nEnter email address to verify (or 'quit' to exit): ").strip()
            
            if email.lower() == 'quit':
                print("Goodbye!")
                break
            
            if not email:
                print("Please enter a valid email address.")
                continue
            
            # Verify email
            print(f"\nVerifying: {email}")
            print("-" * 40)
            
            result = verifier.verify_email(email)
            
            # Display results
            print(f"Email: {result['email']}")
            print(f"Format Valid: {result['format_valid']}")
            print(f"Email Verified: {result['email_verified']}")
            print(f"Is Disposable: {result['is_disposable']}")
            
            # Display as JSON
            print(f"\nJSON Result:")
            print(json.dumps({
                'email_verified': result['email_verified'],
                'is_disposable': result['is_disposable']
            }, indent=2))
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
