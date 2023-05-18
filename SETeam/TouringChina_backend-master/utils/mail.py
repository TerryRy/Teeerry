from django.core.mail import EmailMultiAlternatives


def send_mail(subject, text_content, html_content, **email_kwargs):
    msg = EmailMultiAlternatives(subject, text_content, **email_kwargs)
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
