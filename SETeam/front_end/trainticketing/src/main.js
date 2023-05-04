import { createApp } from 'vue'
import { Button } from 'vant'
import { Cell, CellGroup } from 'vant';
import 'vant/lib/index.css'
import App from "./App.vue"

createApp(App).mount('#app');
App.use(Button);
App.use(Cell);
App.use(CellGroup);