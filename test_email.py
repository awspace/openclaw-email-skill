#!/usr/bin/env python3
"""
Test script for email functionality
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from email_sender import EmailSender

def main():
    print("Testing Email Configuration")
    print("=" * 50)
    
    # Check for config file argument
    config_path = "email_config.json"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    
    if not os.path.exists(config_path):
        print(f"[ERROR] Config file not found: {config_path}")
        print("\nPlease create the config file with your email credentials.")
        print("Template is available at: config_template.json")
        print("\nUsage: python test_email.py [config_file_path]")
        print("Example: python test_email.py email_config.json")
        print("Example: python test_email.py /path/to/your/config.json")
        return
    
    print(f"[OK] Config file found: {config_path}")
    
    # Initialize sender
    try:
        sender = EmailSender(config_path)
        print("[OK] EmailSender initialized successfully")
        
        # Validate config
        if sender.validate_config():
            print("[OK] Configuration is valid")
            
            # Show config (hide password)
            safe_config = sender.config.copy()
            if 'password' in safe_config:
                safe_config['password'] = '***' + safe_config['password'][-4:] if safe_config['password'] else '***'
            
            print("\nCurrent Configuration:")
            for key, value in safe_config.items():
                print(f"  {key}: {value}")
            
            print("\n[READY] Ready to send emails!")
            print("\nUsage examples:")
            print("1. Send test email: python email_sender.py --to your@email.com --test")
            print("2. Send email with attachment: python email_sender.py --to recipient@example.com --subject 'Hello' --body 'Message' --attachment file.pdf")
            
        else:
            print("[ERROR] Configuration is invalid")
            print("Please check your SMTP server, port, username, and password")
            
    except Exception as e:
        print(f"[ERROR] Error initializing EmailSender: {e}")
        print("\nCommon issues:")
        print("1. Make sure Python is installed (python --version)")
        print("2. Check that the config file has valid JSON")
        print("3. Verify all required fields are present")

if __name__ == '__main__':
    main()