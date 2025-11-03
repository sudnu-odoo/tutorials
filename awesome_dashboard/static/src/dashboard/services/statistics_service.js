import { registry } from "@web/core/registry";
import { reactive } from "@odoo/owl";
import { rpc } from "@web/core/network/rpc";

const statisticsService = {
    async start (env) {
        const stats = reactive({data: null})

        async function loadStatistics() {
            const result = await rpc("/awesome_dashboard/statistics");
            stats.data = result;
        }

        await loadStatistics();

        setInterval(loadStatistics, 10 * 1000)

        return {
            stats,
            loadStatistics,
            reload: loadStatistics
        }
    }
}

registry.category("services").add("statistics_service", statisticsService);