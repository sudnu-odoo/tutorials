/** @odoo-module **/

import { registry } from "@web/core/registry";
import { NumberCard } from "./number_card";
import { PieChartCard } from "./pie_chart_card";

// Create a new registry category for dashboard items
export const dashboardItemsRegistry = registry.category("awesome_dashboard_items");

// Register each item
dashboardItemsRegistry.add("average_quantity", {
    id: "average_quantity",
    description: "Average amount of t-shirt",
    Component: NumberCard,
    props: (data) => ({
        title: "Average amount of t-shirt by order this month",
        value: data.average_quantity,
    }),
});

dashboardItemsRegistry.add("average_time", {
    id: "average_time",
    description: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
    Component: NumberCard,
    props: (data) => ({
        title: "Average time for an order to go from 'new' to 'sent' or 'cancelled'",
        value: data.average_time,
    }),
});

dashboardItemsRegistry.add("nb_new_orders", {
    id: "nb_new_orders",
    description: "Number of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of new orders this month",
        value: data.nb_new_orders,
    }),
});

dashboardItemsRegistry.add("nb_cancelled_orders", {
    id: "nb_cancelled_orders",
    description: "Number of cancelled orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: "Number of cancelled orders this month",
        value: data.nb_cancelled_orders,
    }),
});

dashboardItemsRegistry.add("total_amount", {
    id: "total_amount",
    description: "Total amount of new orders this month",
    Component: NumberCard,
    props: (data) => ({
        title: "Total amount of new orders this month",
        value: data.total_amount,
    }),
});

dashboardItemsRegistry.add("orders_by_size", {
    id: "orders_by_size",
    description: "Orders by size",
    Component: PieChartCard,
    size: 2,
    props: (data) => ({
        data: data.orders_by_size,
    }),
});
