# Part of Odoo. See LICENSE file for full copyright and licensing details.
# from . import Flow_Object
import google_auth_oauthlib
# from /snap/pycharm-community/383/plugins/python-ce/helpers/typeshed/stubs/requests/requests/sessions.pyi import requests.
# from requests.sessions import re

from odoo import http, _
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
import webbrowser
import wsgiref.simple_server
import wsgiref.util
import wsgiref
from ..models.models import Flow_Object
import requests



from google_auth_oauthlib.flow import _WSGIRequestHandler, InstalledAppFlow, _RedirectWSGIApp, Flow


class LivechatChatbotScriptController(http.Controller):
    @http.route('/website/chatwithus/googleauth', type="http", auth="public", website=True)
    def chatbot_restart(self, **kwargs):
        # return  request.redirect('/contactus')

        return request.render('google_chat.website_contactus_google_chat', {})

    @http.route('/website/chatwithus/googleauth/receive', type="http", methods=["POST"], auth="public", website=True
                )
    def google_chat_customer_info(self, **customer):
        creditentials_path=request.env['ir.config_parameter'].sudo().get_param('google.chat.creditentials.path', "")
        print('creditentials_pathcreditentials_path',creditentials_path)
        SCOPES = ["https://www.googleapis.com/auth/chat.spaces.create",
                  "https://www.googleapis.com/auth/chat.memberships",
                  "https://www.googleapis.com/auth/chat.messages.create",
                  "https://www.googleapis.com/auth/chat.memberships.app"]

        # flow = InstalledAppFlow.from_client_secrets_file(
        #     '/home/ram/Downloads/client_secret_371504125361-54cee55t5kkje5ic6sp8dt2e4of92lru.apps.googleusercontent.com (2).json',
        #     SCOPES)
        flow = InstalledAppFlow.from_client_secrets_file(
                    creditentials_path+'client_secret.json',
            SCOPES)
        chat_table = request.env['google.chat.customer.info'].sudo()
        info_details = chat_table.search([('email', '=', customer.get('email'))])
        # sequence_number=None
        if not info_details:
            sequence_number = request.env['ir.sequence'].sudo().next_by_code('google.chat.customer.info')
            info_details = chat_table.create({'ticket_no': sequence_number, 'customer_name': customer.get('name'),
                                              'email': customer.get('email_from'), 'phone': customer.get('phone')})
            # creds = flow.run_local_server(port=8080)
            # creds = flow.run_local_server(port=8080 )

            CREDS = None
            # print(os.getcwd())
            # directory_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            # full_path = os.path.join(os.getcwd(), 'custom_addons/google_chat/static/referesh_token.json')
            # print('full_path',full_path)
            creds = Credentials.from_authorized_user_file(
                request.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")
                +'refresh.json', SCOPES)

            # with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/refresh.json', 'w') as url:
            #     url.write(creds.to_json())
            print('credscredscreds', creds)
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

            SERVICE_ACCOUNT_FILE = request.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")+"florence_service.json"
            SCOPES = ['https://www.googleapis.com/auth/chat.bot',
                      "https://www.googleapis.com/auth/chat.memberships.app"]

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
            live_chat_active = request.env['discuss.channel'].search([('livechat_active', '=', True)]).write(
                {'customer_info_id': info_details.id})
            info_details.write({'space_name': result.get('name')})
            service = build('chat', 'v1', credentials=credentials)
            data = info_details.get_template(result.get('description'))
            message = {
                "cards": data['cards']
            }
            response = service.spaces().messages().create(
                parent=CHAT_SPACE,
                body=message
            ).execute()
            current_visitor = request.env['website.visitor']._get_visitor_from_request()
            for current in current_visitor:
                current.write({'space': CHAT_SPACE})
        # Prints details about the created space.
        print(result)
        username = customer.get("username", _("Visitor"))
        channel = request.env['im_livechat.channel'].sudo().browse(1)
        print('==---------------------------------------------------=====================')
        print(channel.script_external)
        info = channel.get_livechat_info(username=username)
        print('infoinhhhhhhhhhhhhfo', info)
        info['channel'] = channel
        print('vvvvvvvvvvvvvvv', request.session)
        dmmm = request.env['discuss.channel'].sudo().create(
            {'name': "Visitor", "channel_type": "livechat", 'active': True, 'livechat_channel_id': 1,
             'livechat_operator_id': 3, 'country_id': 233})
        print('dmmmdmmmdmmm', dmmm)
        print('request.env.user', request.env['website.visitor']._get_visitor_from_request())
        return request.redirect('/im_livechat/support/1')
        # return request.render('im_livechat.loader',  {'channel': channel})
        # return request.render('google_chat.loader_new',  {'channel': channel})

    @http.route('/Token/authenticate', type='json', auth="none", methods=['POST'], csrf=False, save_session=True)
    def google_seson_data_send(self, ):
        byte_string = request.httprequest.data
        print('byte_string', byte_string)
        data = json.loads(byte_string.decode('utf-8'))
        if data['message']['quotedMessageMetadata']:
            replied_thread = data['message']['quotedMessageMetadata']['name']
            print('replied_thread', replied_thread)
            live_chat_active = request.env['mail.message'].sudo().search([('spaces', '=', replied_thread)], limit=1)
            print('live_chat_active', live_chat_active)
            # live_chat_active = request.env['discuss.channel'].sudo().search([('livechat_active', '=', True)], order="id desc",limit=1)
            request.env['mail.message'].sudo().create(
                {'date': datetime.datetime.now(), 'author_id': 3, 'model': 'discuss.channel',
                 'res_id': live_chat_active.res_id, 'body': f"<p>{data['message']['argumentText']}</p>",
                 'message_type': 'comment', 'subtype_id': 1,
                 'email_from': '''"Mitchell Admin" <admin@yourcompany.example.com>''', 'spaces': replied_thread})
            return json.dumps(data)

    @http.route('/authenticate/url', type="http", methods=["GET"], auth="none", website=True
                )
    def google_chat_customer_indddfo(self, **customer):
        creditentials_path=request.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")

        print(request.httprequest.host_url,"request.httprequest.url")
        print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj', customer)
        if(customer.get('code',False)):
            auth=None
            with open(creditentials_path+'client_secret.json','r') as clients:
                clients_data=json.loads(clients.read())

                # auth_data = {'username': clients_data['web']['client_id'], 'password': clients_data['web']['client_secret']}
                auth = requests.auth.HTTPBasicAuth(clients_data['web']['client_id'], clients_data['web']['client_secret'])
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            url = "https://oauth2.googleapis.com/token"
            data_param = {'grant_type': 'authorization_code',
                          'code': customer.get('code'),
                          'client_id': clients_data['web']['client_id'],
                          'client_secret': clients_data['web']['client_secret'],
                          'redirect_uri':'https://florencefilter.com/authenticate/url'

                          }
            auth_cert = {'timeout': None, 'auth': auth, 'verify': None, 'proxies': None, 'cert': None}
            data_response = requests.post(url=url, headers=headers, data=data_param)
            print('data_responsedata_response', data_response.text)
            dictiionary=json.loads(data_response.text)

            with open(creditentials_path+'refresh.json', 'w') as url:
                print('creds.to_json()',data_response.text,creditentials_path)
                creds_val=json.loads(data_response.text)
                print('creds.to_json()',data_response.text)
                dictiionary['refresh_token']=dictiionary['access_token']
                dictiionary['client_id']=clients_data['web']['client_id']
                dictiionary['client_secret']= clients_data['web']['client_secret']
                # creds_val.update({'refresh_token':creds_val['access_token'],'client_id':clients_data['web']['client_id'],'client_secret':clients_data['web']['client_secret'],"universe_domain": "googleapis.com", "account": "","token_uri": "https://oauth2.googleapis.com/token"})
                url.write(json.dumps(dictiionary))

        # wsgi_app = _RedirectWSGIApp("Authenticated")
        # print('flowwwwwwwwwwwwwwobjecttttttttttttt',Flow_Object)
        return 'authenticated'
        # flow_local,client_config_val=request.env['chat.config'].print_flow_config()
        # # print('flow_localflow_localflow_local',flow_local.__dict__['oauth2session'].__dict__)
        # flow_local.authorized_session()
        # # dataaaaa=google_auth_oauthlib.helpers.credentials_from_session(
        # #     flow_local.__dict__['oauth2session'], client_config_val)
        #
        # print('dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        # # print(flow_local.)
        # # wsgiref.simple_server.WSGIServer.allow_reuse_address = False
        # #
        # # local_server = wsgiref.simple_server.make_server(
        # #     None or "localhost", 8080, wsgi_app, handler_class=_WSGIRequestHandler
        # # )
        # # authorization_response = flow_local.redirect_uri
        # # print(authorization_response,'authorization_response'
        # # )
        # # aaaaa=flow_local.fetch_token(
        # #     authorization_response="https://localhost:8080/authenticate/url?state="+customer.get('state')+"&code="+customer.get('code'), audience=None
        # # )
        # # print(flow_local.__dict__['oauth2session'].__dict__)
        # # print(InstalledAppFlow.pass_creditentials.__dict__, 'InstalledAppFlow.credentials')
        # # with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/refresh.json', 'w') as url:
        # # # print('creds.to_json()',creds)
        # #     creds_val=json.loads(InstalledAppFlow.credentials)
        # #     print('creds.to_json()',creds_val)
        #
        #     # creds_val.update({'refresh_token':creds_val['token']})
        #     # url.write(json.dumps(creds_val))
        #
        # return "authenticated"
        #
        # # wsgi_app = _RedirectWSGIApp("Authenticated")
        # # # Fail fast if the address is occupied
        # # wsgiref.simple_server.WSGIServer.allow_reuse_address = False
        # # local_server = wsgiref.simple_server.make_server(
        # #     None or "localhost", 8080, wsgi_app, handler_class=_WSGIRequestHandler
        # # )
        # # print('local_serverlocal_server', local_server)
        # #
        # # redirect_uri_format = (
        # #     "http://{}:{}/"
        # # )
        # # self.redirect_uri = redirect_uri_format.format('localhost', local_server.server_port)
        # # auth_url, _ = InstalledAppFlow.authorization_url({})
        # # print('6666666666666666666666666')
        # # url_data = request.httprequest.data
        # # url_data = json.loads(url_data.decode('utf-8'))
        # # print('6666666666666666666666666')
        # #
        # return request.redirect(url_data['url'])
        # data=request.httprequest.data
        # with open('/home/ram/Downloads/odoo-17.0/custom_addons/google_chat/controllers/url.txt', 'r') as url:
        #     data=url.read()
        #     print('dateeeeeeeeeeeeeeeeeeeeee',data)
        #     request.env['chat.config'].sudo().browse(1).write({'log_date':data})

    @http.route('/chat_authenticate/user', type="http", methods=["POST","GET"], auth="none", website=True,csrf=False, save_session=True
                )
    def google_chat_auth_acess_token_google(self, **customer):
        byte_string = request.httprequest.data
        print('byte_string', byte_string)
        data = json.loads(byte_string.decode('utf-8'))
        # if data['message']['quotedMessageMetadata']:
        #     replied_thread = data['message']['quotedMessageMetadata']['name']
        #     print('replied_thread', replied_thread)
        #     live_chat_active = request.env['mail.message'].sudo().search([('spaces', '=', replied_thread)], limit=1)
        #     print('live_chat_active', live_chat_active)
        #     # live_chat_active = request.env['discuss.channel'].sudo().search([('livechat_active', '=', True)], order="id desc",limit=1)
        #     # operator_details=request.env['website.visitor'].search([('space','=')])
        #     request.env['mail.message'].sudo().create(
        #         {'date': datetime.datetime.now(), 'author_id': 3, 'model': 'discuss.channel',
        #          'res_id': live_chat_active.res_id, 'body': f"<p>{data['message']['argumentText']}</p>",
        #          'message_type': 'comment', 'subtype_id': 1,
        #          'email_from': '''"Mitchell Admin" <admin@yourcompany.example.com>''', 'spaces': replied_thread})
        #     print('dateeeeeeeeeeeeeeeeeeeee', data['space']['name'])
        #
        #     print('google_chat_auth_acess_token', customer)

            #
                # live_chat_active = request.env['discuss.channel'].sudo().search([('livechat_active', '=', True)], order="id desc",limit=1)
        operator_details=request.env['website.visitor'].sudo().search([('space','=',data['space']['name'])])
        replied_space_name=data['space']['name']
        live_chat_active = request.env['mail.message'].sudo().search([('spaces', '=', replied_space_name)], limit=1)
        live_chat_discussion_channel = request.env['discuss.channel'].sudo().search([('livechat_visitor_id', '=', operator_details.id),('livechat_active','=',True)], limit=1)

        request.env['mail.message'].sudo().create(
            {'date': datetime.datetime.now(), 'author_id': operator_details.partner_id.id, 'model': 'discuss.channel',
             'res_id': live_chat_discussion_channel.id, 'body': f"<p>{data['message']['argumentText']}</p>",
             'message_type': 'comment', 'subtype_id': 1,
             # 'email_from': "\\"+operator_details.name+"\\ <"+operator_details.partner_id.email+">", 'spaces': replied_space_name})
             'email_from':f''''\"{operator_details.name}" <{operator_details.partner_id.email}>''', 'spaces': replied_space_name})
            # return json.dumps(data)


    @http.route('/authenticate/urls', type="json", methods=["POST"], auth="none", website=True
                )
    def google_chat_customeskjsr_indfkfddfo(self, **customer):
        creditentials_path=self.env['ir.config_parameter'].sudo().get_param('google.chat.credentials.path', "")

        data = request.httprequest.data
        with open(creditentials_path+'url.txt', 'r') as url:
            data = url.read()
            request.env['chat.config'].sudo().browse(1).write({'log_date': data})

    @http.route('/get_data', type='http', auth="none", methods=['POST'], csrf=False, save_session=True)
    def google_chat_custome_get_data(self, **customer):

        # data = request.httprequest.da6ta
        print('authauathautah')

