/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class DashboardSettingsDialog extends Component {
    static template = "awesome_dashboard.DashboardSettingsDialog";
    static components = { Dialog };
    static props = ["items", "removedIds", "onApply", "close"];

    setup() {
        // Copy of selection state for dialog
        this.state = useState({
            selected: this.props.items.reduce((acc, item) => {
                acc[item.id] = !this.props.removedIds.includes(item.id);
                return acc;
            }, {}),
        });
    }

    toggleItem(id) {
        this.state.selected[id] = !this.state.selected[id];
    }

    apply() {
        const uncheckedIds = Object.entries(this.state.selected)
            .filter(([_, checked]) => !checked)
            .map(([id]) => id);

        this.props.onApply(uncheckedIds);
        this.props.close();
    }
}
