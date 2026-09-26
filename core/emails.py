import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_templated(subject, template, context, to, reply_to=None):
    """Render emails/<template>.txt (+ optional .html) and send. Never raises."""
    if not to:
        return False
    try:
        text = render_to_string(f"emails/{template}.txt", context)
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=list(to),
            reply_to=[reply_to] if reply_to else None,
        )
        try:
            msg.attach_alternative(render_to_string(f"emails/{template}.html", context), "text/html")
        except Exception:
            pass
        msg.send()
        return True
    except Exception:
        logger.exception("Failed to send email %r to %s", subject, to)
        return False


def notify_school(subject, template, context, reply_to=None):
    return send_templated(subject, template, context, settings.SCHOOL_NOTIFY_EMAILS, reply_to)
