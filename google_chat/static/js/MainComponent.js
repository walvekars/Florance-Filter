import { Component, tags, mount } from '@odoo/owl';
import Popup from './Popup';

class MainComponent extends Component {
    static template = tags.xml`
        <div>
            <button class="btn btn-primary" t-on-click="openPopup">Open Popup</button>
        </div>
    `;

    openPopup() {
        const popupContainer = document.createElement('div');
        document.body.appendChild(popupContainer);
        mount(Popup, { target: popupContainer });
    }
}

export default MainComponent;
