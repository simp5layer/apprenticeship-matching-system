import smtplib  # SMTP library for sending emails
from jinja2 import Template  # Templating engine for dynamic HTML content
from email.mime.text import MIMEText  # To format email body as HTML
from email.mime.multipart import MIMEMultipart  # To combine subject and body

# Sends an HTML-formatted email to the recipient
# Uses Jinja2 template rendering and smtplib for delivery
def send_email(sender, recipient, subject, template_str, context, smtp_server='smtp.gmail.com', port=587, login=None, password=None):
    template = Template(template_str)  # Render the Jinja2 HTML template
    message = template.render(context)

    # Create a multipart email with HTML content
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()  # Secure the connection
            if login and password:
                server.login(login, password)  # Authenticate if credentials are provided
            server.send_message(msg)  # Send the email
            return True
    except Exception as e:
        print("Email send failed:", e)  # Log the error
        return False
