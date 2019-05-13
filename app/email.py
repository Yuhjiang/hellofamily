from tasks import send_async
from flask import render_template, current_app


def send_email(to, subject, template, **kwargs):
    html_body = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()

    send_async.delay(subject=subject,
                     author=app.config['FLASK_MAIL_SENDER'],
                     to=to,
                     plain=html_body)