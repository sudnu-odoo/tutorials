/** @odoo-module **/

import { Component, onWillStart, onMounted, useRef } from "@odoo/owl";
import { loadJS } from "@web/core/assets";
import { memoize } from "@web/core/utils/functions";

// Lazy-load Chart.js only once
const loadChartJs = memoize(async () => {
    await loadJS("/web/static/lib/Chart/Chart.js");
    return window.Chart;
});

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = ["data"];
    

    canvasRef = useRef("canvas");

    setup() {
        onWillStart(async () => {
            this.Chart = await loadChartJs();
        });

        onMounted(() => {
            this.renderChart();
        });
    }

    renderChart() {
        const ctx = this.canvasRef.el.getContext("2d");
        const chartData = this.props.data || {};

        const labels = Object.keys(chartData);
        const values = Object.values(chartData);

        new this.Chart(ctx, {
            type: "pie",
            data: {
                labels,
                datasets: [
                    {
                        data: values,
                        borderWidth: 1,
                        backgroundColor: [
                            "#FF6384",
                            "#36A2EB",
                            "#FFCE56",
                            "#4BC0C0",
                            "#9966FF",
                        ],
                    },
                ],
            },
            options: {
                plugins: {
                    legend: { position: "top" },
                    title: { display: true, text: "Orders by Size" },
                },
            },
        });
    }
}
