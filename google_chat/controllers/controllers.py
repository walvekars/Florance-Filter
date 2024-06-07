# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http,_
from odoo.http import request
from odoo.tools import get_lang, is_html_empty, plaintext2html
import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from bs4 import BeautifulSoup
import inspect
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from google.oauth2.credentials import Credentials


class LivechatChatbotScriptController(http.Controller):
    @http.route('/website/chatwithus/googleauth', type="http", auth="public", website=True)
    def chatbot_restart(self, **kwargs):
        # return  request.redirect('/contactus')

        return request.render('google_chat.website_contactus_google_chat', {})

    @http.route('/website/chatwithus/googleauth/receive', type="http", methods=["POST"], auth="public", website=True
                )
    def google_chat_customer_info(self, **customer):
        SCOPES = ["https://www.googleapis.com/auth/chat.spaces.create","https://www.googleapis.com/auth/chat.memberships","https://www.googleapis.com/auth/chat.messages.create","https://www.googleapis.com/auth/chat.memberships.app"]

        # flow = InstalledAppFlow.from_client_secrets_file(
        #     '/home/ram/Downloads/client_secret_371504125361-54cee55t5kkje5ic6sp8dt2e4of92lru.apps.googleusercontent.com (2).json', SCOPES)
        chat_table=request.env['google.chat.customer.info'].sudo()
        info_details=chat_table.search([('email','=',customer.get('email'))])
        # sequence_number=None
        if  not info_details:
            sequence_number = request.env['ir.sequence'].sudo().next_by_code('google.chat.customer.info')
            info_details=chat_table.create({'ticket_no':sequence_number,'customer_name':customer.get('name'),'email':customer.get('email_from'),'phone':customer.get('phone')})

            CREDS=None
            directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            full_path = os.path.join(os.getcwd(), 'custom_addons/google_chat/static/referesh_token.json')
            creds = Credentials.from_authorized_user_file(full_path, SCOPES)



            chat = build('chat', 'v1', credentials=creds)
            #
            result = chat.spaces().create(

                # Details about the space to create.
                body={

                    # To create a named space, set spaceType to SPACE.
                    'spaceType': 'SPACE',

                    # The user-visible name of the space.
                    'displayName': sequence_number
                }

            ).execute()

            SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'custom_addons/google_chat/static/testprojectflorence111 - cec587533a5d.json')
            SCOPES = ['https://www.googleapis.com/auth/chat.bot',"https://www.googleapis.com/auth/chat.memberships.app"]

            # The room or user to send the message to
            CHAT_SPACE = result.get('name')  # Replace with your actual space ID

            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            result1 = chat.spaces().members().create(

                parent=result.get('name'),


                body={
                    'member': {
                        'name': 'users/app',
                        'type': 'BOT'
                    }
                }

            ).execute()
            live_chat_active=request.env['discuss.channel'].search([('livechat_active','=',True)]).write({'customer_info_id':info_details.id})
            info_details.write({'space_name': result.get('name')})
            service = build('chat', 'v1', credentials=credentials)
            data=info_details.get_template(result.get('description'))
            message = {
                "cards": data['cards']
            }
            response = service.spaces().messages().create(
                parent=CHAT_SPACE,
                body=message
            ).execute()

        # Prints details about the created space.
        username = customer.get("username", _("Visitor"))
        channel = request.env['im_livechat.channel'].sudo().browse(1)
        info = channel.get_livechat_info(username=username)
        info['channel']=channel

        return request.redirect('/im_livechat/support/1')




    @http.route('/Token/authenticate', type='json', auth="none",methods=['POST'], csrf=False, save_session=True)
    def google_seson_data_send(self,):
        byte_string = request.httprequest.data
        data = json.loads(byte_string.decode('utf-8'))
        if data['message']['quotedMessageMetadata']:
            replied_thread=data['message']['quotedMessageMetadata']['name']
            live_chat_active=request.env['mail.message'].sudo().search([('spaces','=',replied_thread)])
            request.env['mail.message'].sudo().create({'date':datetime.datetime.now(),'author_id':3,'model':'discuss.channel','res_id':live_chat_active.res_id,'body':f"<p>{data['message']['argumentText']}</p>",'message_type':'comment','subtype_id':1,'email_from':'''"Mitchell Admin" <admin@yourcompany.example.com>''','spaces':replied_thread})
            return json.dumps(data)
