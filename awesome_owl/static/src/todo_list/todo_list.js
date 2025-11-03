// awesome_owl/static/src/todo_list/todo_list.js
import { Component, xml, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "../todo_item/todo_item.js";

export class TodoList extends Component {
    static template = xml`
        <div>
            <h5 class="fw-bold mb-3 text-primary">Todo List</h5>

            <!-- Input with t-ref -->
            <input
                t-ref="inputRef"
                type="text"
                placeholder="Enter a new task"
                class="form-control mb-3"
                t-on-keyup="addTodo"
            />

            <div>
                <t t-foreach="state.todos" t-as="todo" t-key="todo.id">
                    <TodoItem todo="todo" onDelete.bind="deleteTodo" />
                </t>
            </div>
        </div>
    `;

    static components = { TodoItem };

    setup() {
        // ✅ State
        this.state = useState({
            todos: [],
            nextId: 1,
        });

        // ✅ Reference to the input element
        this.inputRef = useRef("inputRef");

        // ✅ When component mounts, focus the input
        onMounted(() => {
            this.inputRef.el.focus();
        });
    }

    addTodo(ev) {
        if (ev.key === "Enter") {
            const input = ev.target;
            const description = input.value.trim();
            if (!description) return;

            this.state.todos.push({
                id: this.state.nextId++,
                description,
                isCompleted: false,
            });

            input.value = "";
            input.focus(); // also refocus after adding a todo
        }
    }

    deleteTodo(id) {
        // find the index of the element to delete
        const index = this.state.todos.findIndex((elem) => elem.id === id);
        if (index >= 0) {
            // remove the element at index from list
            this.state.todos.splice(index, 1);
        }
    }
}
