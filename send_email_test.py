# ENV
SMTP_HOST = southeastaddiction.org
SMTP_PORT = 465
SMTP_USERNAME = marina.richter@southeastaddiction.org
SMTP_PASSWORD = Workmode@25
SMTP_FROM_EMAIL = marina.richter@southeastaddiction.org
https://drive.google.com/drive/folders/1G-74vQpO_iEQ-xqXMijCQW7dSsn0HDB-?usp=sharing
# Req
python-dotenv>=0.19.0
secure-smtplib>=0.1.1


import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    # Get SMTP settings from environment variables
    smtp_host = os.getenv('SMTP_HOST')
    if smtp_host:
        smtp_host = smtp_host.strip('"\'')
    else:
        raise ValueError("SMTP_HOST not found in .env file")
        
    smtp_port = os.getenv('SMTP_PORT')
    if smtp_port:
        smtp_port = int(smtp_port.strip('"\''))
    else:
        raise ValueError("SMTP_PORT not found in .env file")
        
    smtp_username = os.getenv('SMTP_USERNAME')
    if smtp_username:
        smtp_username = smtp_username.strip('"\'')
    else:
        raise ValueError("SMTP_USERNAME not found in .env file")
        
    smtp_password = os.getenv('SMTP_PASSWORD')
    if smtp_password:
        smtp_password = smtp_password.strip('"\'')
    else:
        raise ValueError("SMTP_PASSWORD not found in .env file")
        
    smtp_from_email = os.getenv('SMTP_FROM_EMAIL')
    if smtp_from_email:
        smtp_from_email = smtp_from_email.strip('"\'')
    else:
        # Default to username if from_email not specified
        smtp_from_email = smtp_username

    print(f"Using SMTP server: {smtp_host}:{smtp_port}")
    print(f"Username: {smtp_username}")
    print(f"From email: {smtp_from_email}")

    # Email details
    recipient_email = "kojakeugenio@gmail.com"
    subject = "Test Email from Python - aapanel SMTP"
    body_text = "This is a test email sent from Python using aapanel SMTP details from .env file."
    body_html = """
    <html>
      <body>
        <h2>Test Email from aapanel SMTP Server</h2>
        <p>This is a test email sent from Python using aapanel SMTP details from .env file.</p>
        <p>If you received this, the email sending functionality is working properly!</p>
      </body>
    </html>
    """

    # Create a multipart message
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = smtp_from_email
    message["To"] = recipient_email

    # Add text/plain and text/html parts to the message
    part1 = MIMEText(body_text, "plain")
    part2 = MIMEText(body_html, "html")
    message.attach(part1)
    message.attach(part2)

    # Try multiple connection methods to ensure compatibility with aapanel
    exception_messages = []

    # Method 1: SSL connection (usually port 465)
    if smtp_port == 465:
        try:
            print("\nAttempting direct SSL connection (port 465)...")
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=15) as server:
                server.set_debuglevel(1)  # Enable debug output for troubleshooting
                print("Connected, attempting login...")
                server.login(smtp_username, smtp_password)
                print("Login successful, sending email...")
                server.sendmail(smtp_from_email, recipient_email, message.as_string())
                print(f"✓ Email successfully sent to {recipient_email}")
                exit(0)  # Exit on success
        except Exception as e:
            print(f"✗ SSL connection failed: {e}")
            exception_messages.append(f"SSL connection (465): {str(e)}")

    # Method 2: STARTTLS connection (usually port 587 or 25)
    try:
        print("\nAttempting STARTTLS connection...")
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.set_debuglevel(1)  # Enable debug output for troubleshooting
            print("Connected, starting TLS...")
            server.ehlo()
            server.starttls(context=ssl.create_default_context())
            server.ehlo()
            print("TLS established, attempting login...")
            server.login(smtp_username, smtp_password)
            print("Login successful, sending email...")
            server.sendmail(smtp_from_email, recipient_email, message.as_string())
            print(f"✓ Email successfully sent to {recipient_email}")
            exit(0)  # Exit on success
    except Exception as e:
        print(f"✗ STARTTLS connection failed: {e}")
        exception_messages.append(f"STARTTLS connection: {str(e)}")

    # Method 3: Plain connection (usually port 25, not secure!)
    try:
        print("\nAttempting plain SMTP connection (not secure)...")
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.set_debuglevel(1)  # Enable debug output for troubleshooting
            print("Connected, attempting login...")
            server.ehlo()
            server.login(smtp_username, smtp_password)
            print("Login successful, sending email...")
            server.sendmail(smtp_from_email, recipient_email, message.as_string())
            print(f"✓ Email successfully sent to {recipient_email}")
            exit(0)  # Exit on success
    except Exception as e:
        print(f"✗ Plain connection failed: {e}")
        exception_messages.append(f"Plain connection: {str(e)}")

    # If we got here, all methods failed
    print("\n⚠️ All connection methods failed to send email.")
    print("\nDetailed error messages:")
    for i, msg in enumerate(exception_messages, 1):
        print(f"{i}. {msg}")

    print("\nTroubleshooting tips for aapanel SMTP servers:")
    print("1. Verify your .env file contains the correct SMTP settings")
    print("2. Check if your aapanel mail server is running correctly")
    print("3. Ensure your Contabo server's firewall allows outgoing connections on the SMTP port")
    print("4. Check if your mail server has authentication requirements")
    print("5. Try changing the port (465, 587, or 25)")
    print("6. Check if your hosting provider blocks outgoing SMTP connections")
    print("7. Verify your aapanel mail domain and server configuration")

except Exception as e:
    print(f"Setup error: {e}")
    
    print("\nMake sure your .env file exists and contains the following variables:")
    print("SMTP_HOST=your_mail_server_hostname")
    print("SMTP_PORT=your_mail_server_port (usually 465, 587, or 25)")
    print("SMTP_USERNAME=your_email_username")
    print("SMTP_PASSWORD=your_email_password")
    print("SMTP_FROM_EMAIL=your_from_email_address (optional)")
