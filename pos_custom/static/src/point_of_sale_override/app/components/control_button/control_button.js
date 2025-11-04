/** @odoo-module **/

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    /**
     * Called when user clicks "Delete" button.
     */
    onClickDeleteLine() {
        const order = this.pos.getOrder();
        const selectedLine = order?.getSelectedOrderline();

        if (!selectedLine) {
            this.notification.add("No line selected!", { type: "warning" });
            return;
        }

        order.removeOrderline(selectedLine);
        this.notification.add("Item deleted from order.", { type: "success" });
    },
});
