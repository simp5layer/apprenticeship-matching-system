from jinja2 import Template

def send_email_dummy(sender, recipient, subject, template_str, context):
    template = Template(template_str)
    message = template.render(context)

    print(f"\nFrom: {sender}")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print("Message Body (HTML):")
    print("=" * 50)
    print(message)
    print("=" * 50)
    print(" Email generated successfully (dry run — not sent).\n")

# Test case for simulated email
if __name__ == '__main__':
    template = """
    <h2>Hello {{ name }}!</h2>
    <p>You’ve been matched to <strong>{{ role }}</strong> in <em>{{ company }}</em>.</p>
    """

    context = {
        "name": "Dummy Student",
        "role": "Backend Developer Intern",
        "company": "FutureTech Ltd"
    }

    send_email_dummy(
        sender="noreply@ams.com",
        recipient="student@example.com",
        subject=" Your Apprenticeship Match!",
        template_str=template,
        context=context
    )
