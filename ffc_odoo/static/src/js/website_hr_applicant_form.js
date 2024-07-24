/* @odoo-module */


import { patch } from "@web/core/utils/patch";
//import { hrRecruitment } from "@website_hr_recruitment/static/src/js/website_hr_applicant_form";

import publicWidget from "@web/legacy/js/public/public_widget";



patch(publicWidget.registry.hrRecruitment.prototype, {
  _onClickApplyButton (ev) {
  const $linkedin_profile = $('#recruitment4');
        const $resume = $('#recruitment6');
        if ($linkedin_profile.val().trim() === '' &&
            !$resume[0].files.length) {
            $linkedin_profile.attr('required', true);
            $resume.attr('required', true);
        } else {
            $linkedin_profile.attr('required', false);
            $resume.attr('required', false);
        }
  }
});