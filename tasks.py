import os
import requests
import jinja2
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.getenv("MAILGUN_DOMAIN")
template_loader=jinja2.FileSystemLoader('templates')
template_env = jinja2.Environment(loader=template_loader)

def render_template(template_filename, **context):
    return template_env.get_template(template_filename).render(**context)


def send_simple_message(to, subject, body, html):
    return requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN}/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={"from": f"Your Name <mailgun@{DOMAIN}>",
            "to": [to],
            "subject": subject,
            "text": body,
            "html": html}
    )
    
def send_user_registration_email(email, username):
    return send_simple_message(
        email,
        "Successfully signed up",
        f"Hi {username}! You have successfully registered to the Stores REST API. Thank you for trying it out! "
        f"Use the log in/authenticate endpoint to get an access token for using the other endpoints. "
        f"Use the access token in the Authorization header of your requests by clicking the 'Authorize' button on the top of the swagger-ui docs page and pasting the token into the input on the displayed modal.",
        render_template("email/action.html", username=username)
    )