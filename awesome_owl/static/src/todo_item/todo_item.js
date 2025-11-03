// awesome_owl/static/src/todo_item/todo_item.js
import { Component, xml } from "@odoo/owl";

export class TodoItem extends Component {
    static template = xml`
         <div 
            class="border rounded-2 p-2 mb-2 d-flex justify-content-between"
            t-att-class="props.todo.isCompleted ? 'border rounded-2 p-2 mb-2 d-flex justify-content-between text-muted text-decoration-line-through' : 'border rounded-2 p-2 mb-2 d-flex justify-content-between'"
        >
            <span class="d-flex align-items-center gap-2"> 
                <strong>#[<t t-esc="props.todo.id"/>]</strong>
                <t t-esc="props.todo.description"/>
                 <i class="fa fa-times text-danger btn" t-on-click="() => props.onDelete(props.todo.id)"></i>
            </span>
        </div>
    `;

    static props = {
        todo: { type: Object, optional: false },
        onDelete: { type: Function, optional: false },
    };
}