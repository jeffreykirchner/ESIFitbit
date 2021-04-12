
'''
send email via ESI mass email service
'''
import logging
import requests

from django.conf import settings
# from django.core.mail import send_mass_mail
# from smtplib import SMTPException

# import random
# from django.template.loader import render_to_string
# from django.utils.crypto import get_random_string
# from main.models import Parameters
# from django.utils.html import strip_tags
# from django.core.mail import send_mail



# def sendMassInvitations(subjectList,subject,message):
#     logger = logging.getLogger(__name__)
#     logger.info("Send mass email to list")

#     p = Parameters.objects.first()

#     message_list = []
#     message_list.append(())
#     from_email = getFromEmail()   

#     block_count = 0
#     c = 0
#     for s in subjectList:

#         if c == 100:
#             c = 0
#             block_count += 1
#             message_list.append(())

#         new_message = message.replace("[subject name]",s.name)
#         new_message = new_message.replace("[log in link]",p.siteURL + "subjectHome/" +str(s.login_key))

#         #fill in subject parameters

#         if settings.DEBUG:
#             message_list[block_count] += ((subject, new_message,from_email,[getTestSubjectEmail()]),)   #use for test emails
#         else:
#             message_list[block_count] += ((subject, new_message,from_email,[s.contact_email]),)  

#         c+=1
    
#     return sendMassEmail(block_count,message_list)

# #return the test account email to be used
# def getTestSubjectEmail():
#     p = Parameters.objects.get(id=1)
#     s = p.testEmailAccount

#     return s

# #return the from address
# def getFromEmail():    
#     return f'"{settings.EMAIL_HOST_USER_NAME}" <{settings.EMAIL_HOST_USER }>'

# #send mass email to list,takes a list
# def sendMassEmail(block_count,message_list):
#     logger = logging.getLogger(__name__)
#     logger.info("Send mass email to list")

#     errorMessage = ""
#     mailCount=0
#     if len(message_list)>0 :
#         try:
#             for x in range(block_count+1):            
#                 logger.info("Sending Block " + str(x+1) + " of " + str(block_count+1))
#                 mailCount += send_mass_mail(message_list[x], fail_silently=False) 
#         except SMTPException as e:
#             logger.info('There was an error sending email: ' + str(e)) 
#             errorMessage = str(e)
#     else:
#         errorMessage="Message list empty, no emails sent."

#     return {"mailCount":mailCount,"errorMessage":errorMessage}

def send_mass_email_service(user_list, message_subject, message_text):
    '''
    send mass email through ESI mass pay service
    user_list : [{email:email, variables:[{name:text},{name:text}}, ]
    message_subject : string subject header of message
    message_text : string message template, variables : [name]
    '''

    data = {"user_list" : user_list, "message_subject" : message_subject, "message_text" : message_text}

    logger = logging.getLogger(__name__)
    logger.info(f"ESI mass email API: users: {user_list}, message_subject : {message_subject}, message_text : {message_text}")

    headers = {'Content-Type' : 'application/json', 'Accept' : 'application/json'}

    request_result = requests.post(f'{settings.EMAIL_MS_HOST}/send-email/',
                        json=data,
                        auth=(str(settings.EMAIL_MS_USER_NAME), str(settings.EMAIL_MS_PASSWORD)),
                        headers=headers)

    logger.info(f"ESI mass email API response: {request_result.json()}")

    return request_result.json()