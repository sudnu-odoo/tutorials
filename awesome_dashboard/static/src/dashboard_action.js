import { Component, xml } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { LazyComponent } from "@web/core/assets";

export class AwesomeDashboardLoader extends Component {
    static components = { LazyComponent };
    static template = xml/* xml */`
        <LazyComponent
            bundle="'awesome_dashboard.dashboard'"
            Component="'awesome_dashboard.dashboard'"
        />
    `;
}

// Register this one as the *action* entry point
registry.category("actions").add("awesome_dashboard.dashboard_action", AwesomeDashboardLoader);
