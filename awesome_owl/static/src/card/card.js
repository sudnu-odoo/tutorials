import { Component, xml, useState } from "@odoo/owl";

export class Card extends Component {
    static template = xml`
        <div class="card d-inline-block m-2" style="width: 18rem;">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="m-0" t-esc="props.title"/>
                <button 
                    class="btn btn-sm btn-outline-secondary"
                    t-on-click="toggleOpen"
                >
                    <t t-esc="state.isOpen ? '−' : '+'"/>
                </button>
            </div>

            <!-- Content only visible when open -->
            <t t-if="state.isOpen">
                <div class="card-body">
                    <t t-slot="default"/>
                </div>
            </t>
        </div>
    `;

     // 1. Add props validation
    static props = {
        title: {
            type: String,
            optional: false, // Explicitly required
        },
        slots: {
            type: Object,
            optional: true,
        }
    };

     setup() {
        // Track open/closed state
        this.state = useState({ isOpen: true });
    }

    toggleOpen() {
        this.state.isOpen = !this.state.isOpen;
    }
}