import { Component, useState, xml } from "@odoo/owl";

export class Counter extends Component {
    static template = xml`
        <div>
            Counter: <span t-esc="state.value"/> 
            <button class="ms-3 mb-3 bg-primary text-white border border-primary rounded-2" t-on-click="increment">Increment</button>
        </div>
    `;

    static props = {
        onChange: { type: Function, optional: true },  
    };

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value++;

        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}