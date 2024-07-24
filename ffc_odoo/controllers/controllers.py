import importlib

from odoo import SUPERUSER_ID,_
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br, nl2br_enclose

mail_tracking = importlib.import_module('odoo.addons.website')
class MailTrackingController(mail_tracking.controllers.form.WebsiteForm):
    def insert_record(self, request, model, values, custom, meta=None):
        res =super(MailTrackingController,self).insert_record( request, model, values, custom, meta=None)
        print(model.name,custom,'eeeeeeeee',meta,values)

        body=""
        if(not values.get('job_id')):
            for key,key_value in values.items():

                body+=(f'<p><span>{key}</span> : <span>{key_value}</span></p>')
            body += f"<p><span>{custom}</span></p>"
            mail=request.env['mail.mail'].create({'email_from':'abcd@gmail.com','email_to':'abcde@primemindsconsulting.com','body_html':body,'subject':'Contact Form'})
            mail.send()
        # print('ddhddhdih',values)
        return res
        # print('ccccccccccccccccddddddddd',request,model,values,custom)
        # model_name = model.sudo().model
        # if model_name == 'mail.mail':
        #     email_from = _('"%s form submission" <%s>') % (request.env.company.name, request.env.company.email)
        #     values.update({'reply_to': values.get('email_from'), 'email_from': email_from,'email_to':'testing@gmail.com'})
        # record = request.env[model_name].with_user(SUPERUSER_ID).with_context(
        #     mail_create_nosubscribe=True,
        # ).create(values)
        # print('vrecordrecordrecordrecordrecordrecordrecordrecordrecordrecordrecordrecord',record)
        #
        # if custom or meta:
        #     _custom_label = "%s\n___________\n\n" % _("Other Information:")  # Title for custom fields
        #     if model_name == 'mail.mail':
        #         _custom_label = "%s\n___________\n\n" % _("This message has been posted on your website!")
        #     default_field = model.website_form_default_field_id
        #     default_field_data = values.get(default_field.name, '')
        #     custom_content = (default_field_data + "\n\n" if default_field_data else '') \
        #                      + (_custom_label + custom + "\n\n" if custom else '') \
        #                      + (self._meta_label + "\n________\n\n" + meta if meta else '')
        #
        #     # If there is a default field configured for this model, use it.
        #     # If there isn't, put the custom data in a message instead
        #     if default_field.name:
        #         if default_field.ttype == 'html' or model_name == 'mail.mail':
        #             custom_content = nl2br(custom_content)
        #         record.update({default_field.name: custom_content})
        #     elif hasattr(record, '_message_log'):
        #         record._message_log(
        #             body=nl2br_enclose(custom_content, 'p'),
        #             message_type='comment',
        #         )
        #
        # return record.id
