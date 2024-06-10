# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http,_
from odoo.http import request
from odoo.tools import get_lang, is_html_empty, plaintext2html
import os.path
from werkzeug.utils import redirect
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
import webbrowser


class LivechatChatbotScriptController(http.Controller):
    @http.route('/website/chatwithus/googleauth', type="http", auth="public", website=True)
    def chatbot_restart(self, **kwargs):
        # return  request.redirect('/contactus')

        return request.render('google_chat.website_contactus_google_chat', {})

    @http.route('/website/chatwithus/googleauth/receive', type="http", methods=["POST"], auth="public", website=True
                )
    def google_chat_customer_info(self, **customer):
        # prin=webbrowser.open_new_tab("https://www.javatpoint.com/traffic-flow-simulation-in-python")

        # print('printttttttttttttttttttt',prin)
        print('customerrrrrrrrrrrr',customer)
        SCOPES = ["https://www.googleapis.com/auth/chat.spaces.create","https://www.googleapis.com/auth/chat.memberships","https://www.googleapis.com/auth/chat.messages.create","https://www.googleapis.com/auth/chat.memberships.app"]

        flow = InstalledAppFlow.from_client_secrets_file(
            '/home/ram/Downloads/client_secret_371504125361-54cee55t5kkje5ic6sp8dt2e4of92lru.apps.googleusercontent.com (2).json', SCOPES)
        chat_table=request.env['google.chat.customer.info'].sudo()
        info_details=chat_table.search([('email','=',customer.get('email'))])
        # sequence_number=None
        if  not info_details:
            sequence_number = request.env['ir.sequence'].sudo().next_by_code('google.chat.customer.info')
            info_details=chat_table.create({'ticket_no':sequence_number,'customer_name':customer.get('name'),'email':customer.get('email_from'),'phone':customer.get('phone')})
            # creds = flow.run_local_server(port=8080)
            # creds = flow.run_local_server(port=8080 )

            creds=None
            # print(os.getcwd())
            # directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            # full_path = os.path.join(os.getcwd(), 'custom_addons/google_chat/static/referesh_token.json')
            # print('full_path',full_path)
            # creds = Credentials.from_authorized_user_file(full_path, SCOPES)
            creds = Credentials.from_authorized_user_file('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/refresh.json', SCOPES)
            # creds['refresh_token']=creds['token']
            # with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/refresh.json', 'r') as url:
            #     creds=url.read()
            print('credscredscreds',creds,type(creds))
            # Build a service endpoint for Chat API.
            chat = build('chat', 'v1', credentials=creds)
            #
            # Use the service endpoint to call Chat API.
            result = chat.spaces().create(

                # Details about the space to create.
                body={

                    # To create a named space, set spaceType to SPACE.
                    'spaceType': 'SPACE',

                    # The user-visible name of the space.
                    'displayName': sequence_number
                }

            ).execute()

            # info_details.get_template(result.get('description'))
            # chat = build('chat', 'v1', credentials=creds)

            print(info_details.get_template(customer.get('description')))

            SERVICE_ACCOUNT_FILE = '/home/ram/Downloads/testprojectflorence111-cec587533a5d.json'
            SCOPES = ['https://www.googleapis.com/auth/chat.bot',"https://www.googleapis.com/auth/chat.memberships.app"]

            # The room or user to send the message to
            CHAT_SPACE = result.get('name')  # Replace with your actual space ID

            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            result1 = chat.spaces().members().create(

                # The space in which to create a membership.
                parent=result.get('name'),

                # Set the Chat app as the entity that gets added to the space.
                # 'app' is an alias for the Chat app calling the API.
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
            current_visitor=request.env['website.visitor']._get_visitor_from_request()
            for current in current_visitor:
                current.write({'space':CHAT_SPACE})
        # Prints details about the created space.
        print(result)
        username = customer.get("username", _("Visitor"))
        channel = request.env['im_livechat.channel'].sudo().browse(1)
        print('==---------------------------------------------------=====================')
        print(channel.script_external)
        info = channel.get_livechat_info(username=username)
        print('infoinhhhhhhhhhhhhfo',info)
        info['channel']=channel
        print('vvvvvvvvvvvvvvv',request.session)
        dmmm=request.env['discuss.channel'].sudo().create({'name':"Visitor","channel_type":"livechat",'active':True,'livechat_channel_id':1,'livechat_operator_id':3,'country_id':233})
        print('dmmmdmmmdmmm',dmmm)
        print('request.env.user',request.env['website.visitor']._get_visitor_from_request())
        return request.redirect('/im_livechat/support/1')
        # return request.render('im_livechat.loader',  {'channel': channel})
        # return request.render('google_chat.loader_new',  {'channel': channel})





    @http.route('/Token/authenticate', type='json', auth="none",methods=['POST'], csrf=False, save_session=True)
    def google_seson_data_send(self,):
        byte_string = request.httprequest.data
        print('byte_string',byte_string)
        data = json.loads(byte_string.decode('utf-8'))
        if data['message']['quotedMessageMetadata']:
            replied_thread=data['message']['quotedMessageMetadata']['name']
            print('replied_thread',replied_thread)
            live_chat_active=request.env['mail.message'].sudo().search([('spaces','=',replied_thread)],limit=1)
            print('live_chat_active',live_chat_active)
            # live_chat_active = request.env['discuss.channel'].sudo().search([('livechat_active', '=', True)], order="id desc",limit=1)
            request.env['mail.message'].sudo().create({'date':datetime.datetime.now(),'author_id':3,'model':'discuss.channel','res_id':live_chat_active.res_id,'body':f"<p>{data['message']['argumentText']}</p>",'message_type':'comment','subtype_id':1,'email_from':'''"Mitchell Admin" <admin@yourcompany.example.com>''','spaces':replied_thread})
            return json.dumps(data)



    @http.route('/authenticate/url', type="json", methods=["POST"], auth="none", website=True
                )
    def google_chat_customer_inddddfo(self, **customer):
        print('6666666666666666666666666')
        with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/url.txt', 'r') as url:
            data=url.read()
            print('dateeeeeeeeeeeeeeeeeeeeee',data)
        request.env['chat.config'].sudo().browse(1).write({'log_date':data})