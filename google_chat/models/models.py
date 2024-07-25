from odoo import models, fields, api
from googleapiclient.discovery import build
from google.oauth2 import service_account
import html2text
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
import inspect
import io
import sys
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from .Overridegoogle import InstalledAppFlow
import webbrowser
import wsgiref.simple_server
import wsgiref.util
import wsgiref
import requests

from  google_auth_oauthlib.flow import _WSGIRequestHandler,InstalledAppFlow,_RedirectWSGIApp,Flow

import webbrowser
import oauth2client
Flow_Object=None

client_config_val=None
#=========================================
from base64 import urlsafe_b64encode
import hashlib
import json
import logging

try:
    from secrets import SystemRandom
except ImportError:  # pragma: NO COVER
    from random import SystemRandom
from string import ascii_letters, digits
import webbrowser
import wsgiref.simple_server
import wsgiref.util

import google.auth.transport.requests
import google.oauth2.credentials

import google_auth_oauthlib.helpers



class Chatbot(models.Model):
    _inherit = 'im_livechat.channel'

    @api.model
    def get_mail_channel(self, uuid):
        channel = super(Chatbot, self).get_mail_channel(uuid)
        print('ddddddddddddddddddddddd', channel)
        self.env['mail.channel'].browse(channel['id']).message_post(body="Hello! How can I assist you today?")
        return channel

    @api.model
    def post_message(self, uuid, message_content, custom_data):
        channel = self.env['mail.channel'].search([('uuid', '=', uuid)])
        print('channekllllll', channel)
        if channel:
            response = self.get_bot_response(message_content)
            channel.message_post(body=response)
        return True

    def get_bot_response(self, message_content):
        # Implement your bot logic here
        # For simplicity, echo the user's message
        return f"You said: {message_content}"


class DiscussChannelNew(models.Model):
    """ Chat Session
        Reprensenting a conversation between users.
        It extends the base method for anonymous usage.
    """

    _inherit = 'discuss.channel'

    channel_type = fields.Selection(
        selection_add=[('livechat', 'Livechat Conversation'), ('google_chat', "Google Chat Conversation")],
        ondelete={'google_chat': 'cascade'})
    customer_info_id=fields.Many2one('google.chat.customer.info',sting="chat info")

    def _message_post_after_hook(self, message, msg_vals):
        res=super(DiscussChannelNew,self)._message_post_after_hook(message, msg_vals)
      
        if msg_vals['body'] and "The chat request has been canceled" not in msg_vals['body'] and "itchell Admin started a conversation" not in msg_vals['body'] and "left the conversation" not in msg_vals['body'] :
            result = message.send_chat(message=html2text.html2text(msg_vals["body"]))
            print(result)
            # if result.get("space").get("name"):
            #     print(result["space"].get("name"))
            # if result.get("message").get("quotedMessageMetadata"):
            #     print(result["message"].get("quotedMessageMetadata"))
            message.write({'spaces': result['name']})
        return res


class DiscussChannelNewshsh(models.Model):
    _inherit = "mail.message"
    spaces=fields.Char(string="spaces")


    def send_chat(self, message):
 
        current_visitor = self.env['website.visitor']._get_visitor_from_request()
        # for current in current_visitor:
        live_chat_id=self.env['discuss.channel'].search([('livechat_active','=',True),('livechat_visitor_id','=',current_visitor.id)],limit=1)

        SCOPES = ['https://www.googleapis.com/auth/chat.bot']
        creditentials_path=self.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")

        CREDENTIALS = service_account.Credentials.from_service_account_file(
            creditentials_path+'florence_service.json', scopes=SCOPES)
        print('===============================================')
        # data=request.env['mail.message'].create({'email_from':'sjsjj@gmail.com'})
        # return request.render('google_chat.website.contactus',{})
        chat = build('chat', 'v1', credentials=CREDENTIALS)
        # print(inspect.signature(chat.spaces().messages().create().execute))
        # Use the service endpoint to call Chat API.
        result = chat.spaces().messages().create(

            # The space to create the message in.
            #
            # Replace SPACE with a space name.
            # Obtain the space name from the spaces resource of Chat API,
            # or from a space's URL.
            parent=live_chat_id.livechat_visitor_id.space,
            body={'text':message}

        ).execute()
        print('resultresultresultresultresult',result)
        return result


class GoogleChatCustomerInfo(models.Model):
    _name = "google.chat.customer.info"

    ticket_no = fields.Char(string="Ticket no")

    customer_name = fields.Char(string="Customer Name")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    space_name = fields.Char(String="Space name")

    def get_template(self, question):
        card = {
            "cards": [
                {
                    "header": {
                        "title": f"{self.customer_name} accepted Live chat from Florence Filter support",
                        "subtitle": question,
                        "imageUrl": "https://developers.google.com/chat/images/chat-product-icon.png"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"<b>Email:</b> {self.email}"
                                    }
                                },
                                {
                                    "textParagraph": {
                                        "text": f"<b>Name:</b> {self.customer_name}"
                                    }
                                },
                                {
                                    "textParagraph": {
                                        "text": f"<b>Phone:</b> {self.phone}"
                                    }
                                },
                                {
                                    "textParagraph": {
                                        "text": f"<b>Location:</b> Dharmavaram,India"
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        return card



class ChatConfig(models.Model):
    """ Chat Session
        Reprensenting a conversation between users.
        It extends the base method for anonymous usage.
    """

    _name = 'chat.config'
    name=fields.Char(string="Name")
    log_date=fields.Char()

    # customer_info_id=fields.Many2one('google.chat.customer.info',sting="chat info")

    def action_approve_scopes(self):
        base_url=self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        creditentials_path=self.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")


        SCOPES = ["https://www.googleapis.com/auth/chat.spaces.create",
                  "https://www.googleapis.com/auth/chat.memberships",
                  "https://www.googleapis.com/auth/chat.messages.create",
                  "https://www.googleapis.com/auth/chat.memberships.app", 'https://www.googleapis.com/auth/adwords']

        with open(creditentials_path+'client_secret.json', "r") as json_file:
            client_config = json.load(json_file)
            print('client_configclient_config',client_config)
        data=Flow.from_client_config(client_config,SCOPES)

        wsgi_app = _RedirectWSGIApp("Authenticated")
        wsgiref.simple_server.WSGIServer.allow_reuse_address = False
        local_server = wsgiref.simple_server.make_server(
            None or "florencefilter.com", 8080, wsgi_app, handler_class=_WSGIRequestHandler
        )
        print('local_serverlocal_server', local_server,local_server.__dict__['application'].__dict__)


        auth_url, state = data.authorization_url()
        main_url=auth_url+'&redirect_uri=https://florencefilter.com/authenticate/url'
        print('main_urlmain_url',main_url)

        global Flow_Object
        global client_config_val

        Flow_Object = data
        client_config_val=client_config

        return {'type': 'ir.actions.act_url',
                'url':main_url,
                'target': 'new',
                # 'res_id': self.id,
                }

        # # webbrowser.open_new("https://www.javatpoint.com/pyqt-library-in-python")
        # # # print("""        webbrowser.open_new("https://www.javatpoint.com/pyqt-library-in-python")""")
        #
        # sco=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
        #
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     '/home/ram/Downloads/client_secret_371504125361-54cee55t5kkje5ic6sp8dt2e4of92lru.apps.googleusercontent.com (3).json',
        #     scopes=SCOPES)
        # creds = flow.run_local_server(port=8080,redirect_uri_trailing_slash=False)
        # # # # # # session = flow.authorized_session()
        # with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/refresh.json','w') as url:
        #     print('creds.to_json()',creds)
        #     creds_val=json.loads(creds.to_json())
        #     print('creds.to_json()',creds_val)
        #
        #     creds_val.update({'refresh_token':creds_val['token']})
        #     url.write(json.dumps(creds_val))
        # #
    # print('customerrrrrrrrrrrr')
        # directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # full_path = os.path.join(directory_path, 'sjsjjs.json')
        # print('full_path', full_path)

        # SCOPES = ["https://www.googleapis.com/auth/chat.spaces.create",
        #           "https://www.googleapis.com/auth/chat.memberships",
        #           "https://www.googleapis.com/auth/chat.messages.create",
        #           "https://www.googleapis.com/auth/chat.memberships.app"]
        #
        # flow = InstalledAppFlow.from_client_secrets_file(
        #     '/home/ram/Downloads/client_secret_371504125361-54cee55t5kkje5ic6sp8dt2e4of92lru.apps.googleusercontent.com (2).json',
        #     SCOPES)

        # sequence_number = request.env['ir.sequence'].sudo().next_by_code('google.chat.customer.info')
        # info_details = chat_table.create({'ticket_no': sequence_number, 'customer_name': customer.get('name'),
        #                                   'email': customer.get('email_from'), 'phone': customer.get('phone')})
        # creds = flow.run_local_server(port=8080).authorized_session()
        # v = flow.run_local_server(port=8080, open_browser=True,redirect_uri_trailing_slash=True).credentials

        # print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv',v,flow.credentials)
    def print_flow_config(self):
        print('Flow_ObjectFlowdduhduhdhdhud_Object', Flow_Object)
        return Flow_Object,client_config_val

    def get_credentials(self):
        creditentials_path=self.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")

        """Gets google api credentials, or generates new credentials
        if they don't exist or are invalid."""
        scope = 'https://www.googleapis.com/auth/blogger'
        flow = oauth2client.client.flow_from_clientsecrets(
            creditentials_path+'client_secret.json', scope,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        storage = oauth2client.file.Storage('credentials.dat')
        credentials = storage.get()
        if not credentials or credentials.invalid:
            auth_uri = flow.step1_get_authorize_url()
            webbrowser.open(auth_uri)
            auth_code = input('Enter the auth code: ')
            credentials = flow.step2_exchange(auth_code)
            storage.put(credentials)
        return credentials

class WebsiteVisitorTrack(models.Model):
    _inherit = 'website.visitor'

    space=fields.Char(string='Google chat space')

class weOcn(models.TransientModel):
    _inherit = "res.config.settings"
    enable_ocn=fields.Char()
    disable_redirect_firebase_dynamic_link=fields.Char()
    map_box_token=fields.Char()
