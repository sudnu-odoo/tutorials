import { Component, markup, useState } from "@odoo/owl";
import { Counter } from "./counter/counter.js";
import { Card } from "./card/card.js";
import { TodoList } from "./todo_list/todo_list.js";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card, TodoList };
    
    setup() {
        this.html_content = markup("<div><span class='fw-bold text-success'>HTML content rendered!</span></div>");

        this.state = useState({
            counter1: 0,
            counter2: 0,
            sum: 0,
        });
    }

    onCounter1Change(newValue) {
        this.state.counter1 = newValue;
        this.updateSum();
    }

    onCounter2Change(newValue) {
        this.state.counter2 = newValue;
        this.updateSum();
    }

    updateSum() {
        this.state.sum = this.state.counter1 + this.state.counter2;
    }

}
