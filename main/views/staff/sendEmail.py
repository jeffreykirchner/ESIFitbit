
from django.conf import settings
from django.core.mail import send_mass_mail
from smtplib import SMTPException
import logging
import random
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from main.models import parameters
from django.utils.html import strip_tags
from django.core.mail import send_mail

def sendMassInvitations(subjectList,subject,message):
    logger = logging.getLogger(__name__)
    logger.info("Send mass email to list")

    message_list = []
    message_list.append(())
    from_email = settings.EMAIL_HOST_USER    

    block_count = 0
    c = 0
    for s in subjectList:

        if c == 100:
            c = 0
            block_count += 1
            message_list.append(())

        new_message = s.name + ",\n\n" + message

        #fill in subject parameters

        if settings.DEBUG:
            message_list[block_count] += ((subject, new_message,from_email,["TestSubject" + str(random.randrange(1, 50)) + "@esirecruiter.net"]),)   #use for test emails
        else:
            message_list[block_count] += ((subject, new_message,from_email,[s['email']]),)  

        c+=1
    
    sendMassEmail(block_count,message_list)

#send mass email to list,takes a list
def sendMassEmail(block_count,message_list):
    logger = logging.getLogger(__name__)
    logger.info("Send mass email to list")

    errorMessage = ""
    mailCount=0
    if len(message_list)>0 :
        try:
            for x in range(block_count+1):            
                logger.info("Sending Block " + str(x+1) + " of " + str(i+1))
                mailCount += send_mass_mail(message_list[x], fail_silently=False) 
        except SMTPException as e:
            logger.info('There was an error sending email: ' + str(e)) 
            errorMessage = str(e)
    else:
        errorMessage:"Message list empty, no emails sent."

    return {"mailCount":mailCount,"errorMessage":errorMessage}