/** @odoo-module **/

import { Component, useState } from 'web.OwlCompat';

class ChatPopup extends Component {
    constructor() {
        super(...arguments);
        this.state = useState({
            isVisible: false,
        });
    }

    togglePopup() {
        this.state.isVisible = !this.state.isVisible;
    }
}

ChatPopup.template = 'google_chat.ChatPopupTemplate';

export default ChatPopup;
