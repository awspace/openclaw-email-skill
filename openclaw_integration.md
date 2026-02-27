# OpenClaw Email Integration

This document explains how to use the email skill from within OpenClaw sessions.

## Prerequisites

1. Email configuration file created at `D:\clawd_workspace\email_config.json`
2. Python installed and accessible
3. Email skill enabled in OpenClaw config

## Using Email in OpenClaw Sessions

### Method 1: Direct Python Execution

You can call the email sender directly from OpenClaw:

```python
# In an OpenClaw session
import sys
sys.path.append('D:\\clawd_workspace\\skills\\email')
from email_sender import EmailSender

sender = EmailSender('D:\\clawd_workspace\\email_config.json')

result = sender.send_email(
    to_email='recipient@example.com',
    subject='Test from OpenClaw',
    body='This email was sent from OpenClaw!',
    attachments=['D:\\clawd_workspace\\report.pdf']
)

if result['success']:
    print(f"Email sent successfully!")
else:
    print(f"Failed to send email: {result['error']}")
```

### Method 2: Using exec Tool

You can use OpenClaw's `exec` tool to run the email sender:

```bash
# Send a simple email
python D:\clawd_workspace\skills\email\email_sender.py --to "recipient@example.com" --subject "Hello" --body "Message from OpenClaw"

# Send email with attachment
python D:\clawd_workspace\skills\email\email_sender.py --to "recipient@example.com" --subject "Report" --body "Please review" --attachment "D:\clawd_workspace\report.pdf"
```

### Method 3: Create Custom Commands

Add these to your `AGENTS.md` or create a custom skill:

```markdown
## Email Commands

- `send email to <address> with subject <subject> and body <body>` - Send basic email
- `email <file> to <address>` - Send file as attachment
- `test email configuration` - Send test email
```

## Example: Complete Email Function

Here's a complete function you can add to your OpenClaw setup:

```python
# Add this to a custom skill or your workspace
import os
import sys

def send_email_from_openclaw(to_email, subject, body, attachments=None):
    """
    Send email from within OpenClaw
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
        attachments: List of file paths (optional)
    """
    # Add email skill to path
    email_skill_path = 'D:\\clawd_workspace\\skills\\email'
    if email_skill_path not in sys.path:
        sys.path.append(email_skill_path)
    
    try:
        from email_sender import EmailSender
        
        sender = EmailSender('D:\\clawd_workspace\\email_config.json')
        
        result = sender.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            attachments=attachments or []
        )
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Example usage in OpenClaw:
# result = send_email_from_openclaw(
#     to_email='alan@example.com',
#     subject='Daily Report',
#     body='Here is your daily report.',
#     attachments=['D:\\clawd_workspace\\daily_report.pdf']
# )
```

## Common Use Cases

### 1. Sending Reports
```python
# After generating a report
report_path = 'D:\\clawd_workspace\\generated_report.pdf'
send_email_from_openclaw(
    to_email='team@company.com',
    subject='Daily Analytics Report',
    body='Please find attached the daily analytics report.',
    attachments=[report_path]
)
```

### 2. Notification Emails
```python
# Send notification when a task completes
send_email_from_openclaw(
    to_email='user@example.com',
    subject='Task Completed',
    body='Your scheduled task has completed successfully.'
)
```

### 3. Email with Multiple Attachments
```python
# Send multiple files
attachments = [
    'D:\\clawd_workspace\\data.csv',
    'D:\\clawd_workspace\\chart.png',
    'D:\\clawd_workspace\\summary.docx'
]

send_email_from_openclaw(
    to_email='manager@company.com',
    subject='Weekly Data Package',
    body='Attached are the weekly data files.',
    attachments=attachments
)
```

## Error Handling

```python
def safe_send_email(to_email, subject, body, attachments=None):
    """Send email with error handling"""
    try:
        result = send_email_from_openclaw(to_email, subject, body, attachments)
        
        if result['success']:
            return f"✅ Email sent to {to_email} with {len(attachments or [])} attachments"
        else:
            return f"❌ Failed to send email: {result['error']}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"
```

## Testing

Always test your configuration first:

```python
# Test function
def test_email_config():
    """Test email configuration"""
    result = send_email_from_openclaw(
        to_email='your-email@gmail.com',  # Send to yourself
        subject='OpenClaw Email Test',
        body='If you receive this, email configuration is working!'
    )
    
    if result['success']:
        print("Email test successful!")
    else:
        print(f"Email test failed: {result['error']}")
```

## Security Best Practices

1. **Never hardcode credentials** - Always use config file or environment variables
2. **Use app passwords** for services like Gmail (not your main password)
3. **Regularly rotate passwords** - Update your email_config.json periodically
4. **Limit attachment sizes** - Most providers have 25MB limits
5. **Validate recipients** - Always double-check email addresses before sending