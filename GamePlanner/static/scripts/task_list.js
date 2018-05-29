import {ajaxOption, getCookie} from "scripts/csrf"
import Vddl from 'vddl';
import Vue from "vue";
import kanban from 'vue_components/kanban.vue';

Vue.use(Vddl);

var categories = {
  "PLANNED": "Planned",
  "IN_PROGRESS": "board-in-progress",
  "TESTING": "board-testing",
  "COMPLETED": "board-completed",
}


var app = new Vue({
  el: '#task-list-app',
  delimiters: ["[[","]]"],
  components: {
    kanban: kanban
  },
  methods: {
    set_nodes: function(nodes) {
      for (var category_i in this.categories) {
        var category = this.categories[category_i]
        var final_nodes = nodes.filter(x => x.fields.stage == category.name)
        category.nodes = final_nodes
      }
    }
  },
  data: {
    categories: [
      {
        name: "PLANNED",
        display_name: "Planed",
        nodes: []
      },
      {
        name: "IN_PROGRESS",
        display_name: "In progress",
        nodes: []
      },
      {
        name: "TESTING",
        display_name: "Testing",
        nodes: []
      },
      {
        name: "COMPLETED",
        display_name: "Completed",
        nodes: []
      }
    ],
  }
})
window.set_tasks = function (tasks) {
  app.set_nodes(tasks)
}
