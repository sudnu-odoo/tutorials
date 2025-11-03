import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import { PieChart } from "./pie_chart";
// Import registry definition (so it’s initialized)
import { dashboardItemsRegistry } from "./dashboard_items";
import { DashboardSettingsDialog } from "./dashboard_settings_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup(){
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.statisticsService = useService("statistics_service");
        this.state = useState(this.statisticsService.stats)
        // Collect all items from registry
        this.items = [...dashboardItemsRegistry.getAll()];
        this.removedIds = this.loadConfig();
        // fetch data before rendering
        // onWillStart(async () => {
        //     this.state.stats = await this.statisticsService.loadStatistics();
        // });
    }

    get filteredItems() {
        return this.items.filter((item) => !this.removedIds.includes(item.id));
    }

    // --- SETTINGS LOGIC ---
    openSettings() {
        this.dialog.add(DashboardSettingsDialog, {
            items: this.items,
            removedIds: this.removedIds,
            onApply: (uncheckedIds) => {
                this.removedIds = uncheckedIds;
                this.saveConfig();
            },
        });
    }

    loadConfig() {
        try {
            return JSON.parse(localStorage.getItem("awesome_dashboard_removed_items") || "[]");
        } catch {
            return [];
        }
    }

    saveConfig() {
        localStorage.setItem("awesome_dashboard_removed_items", JSON.stringify(this.removedIds));
    }

    // Button handlers
    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Leads',
            res_model: 'crm.lead',
            views: [[false, 'kanban'], [false, 'form']],
            target: 'current',
        })
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
