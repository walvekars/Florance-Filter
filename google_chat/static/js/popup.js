import { Component, tags } from '@odoo/owl';

class Popup extends Component {
    static template = tags.xml`
        <div class="modal fade show" tabindex="-1" role="dialog" style="display: block;">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Popup Title</h5>
                        <button type="button" class="close" aria-label="Close" t-on-click="close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>This is a popup content.</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" t-on-click="close">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    close() {
        this.el.remove();
    }
}

export default Popup;
