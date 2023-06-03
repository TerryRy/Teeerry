//import { createApp } from 'vue'
//import App from './App.vue'

//createApp(App).mount('#app')
import { createApp } from 'vue';
import App from './App.vue';
import store from './store';
import { createRouter, createWebHistory } from 'vue-router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
// import WelcomePage from "@/views/welcome_page/WelcomePage.vue";
import HomePage from "@/views/user/homepage/HomePage.vue";
import AccountManage from "@/views/user/account_manage/AccountManage.vue";
import DepositMoney from "@/views/user/deposit_money/DepositMoney.vue";
import orderList from "@/views/user/order_list/OrderList.vue";
import orderDetails from "@/views/user/order_details/OrderDetails.vue";
import accountAdd from "@/views/user/account_add/AccountAdd.vue";
import PersonalCenter from "@/views/user/personal_center/PersonalCenter.vue";
import QueryTrain from "@/views/user/query_train/QueryTrain.vue";
import ticketBuy from "@/views/user/ticket_buy/TicketBuy.vue";
import TicketChangeChoices from "@/views/user/ticket_change_choices/TicketChangeChoices.vue";
import TicketChangeConfirm from "@/views/user/ticket_change_confirm/TicketChangeConfirm.vue";
import TrainAdd from "@/views/railway_admin/train_add/TrainAdd.vue";
import trainChange from "@/views/railway_admin/train_change/TrainChange.vue";
import workSpace from "@/views/railway_admin/workspace/WorkSpace.vue";
import StationAdd from "@/views/railway_admin/station_add/StationAdd.vue";
import CarriageAdd from "@/views/railway_admin/carriage_add/CarriageAdd.vue";
import TrainDelete from "@/views/railway_admin/train_delete/TrainDelete.vue";
import ContactAdd from "@/views/user/personal_center/ContactAdd.vue";
import TicketPay from "@/views/user/ticket_buy/TicketPay.vue";
import UserAdd from "@/views/system_admin/user_add/userAdd.vue";
import UserChange from "@/views/system_admin/user_change/userChange.vue";
import UserList from "@/views/system_admin/user_list/userList.vue";
import MessageList from "@/views/user/message_list/MessageList.vue";


// ...
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: HomePage },
        { path: '/homepage', component: HomePage },
        { path: '/accountmanage', component: AccountManage },
        { path: '/depositmoney', component: DepositMoney },
        { path: '/orderlist', component: orderList },
        { path: '/orderdetails', component: orderDetails },
        { path: '/accountadd', component: accountAdd },
        { path: '/personalcenter', component: PersonalCenter },
        { path: '/querytrain', component: QueryTrain },
        { path: '/ticketbuy', component: ticketBuy },
        { path: '/ticketchangechoice', component: TicketChangeChoices },
        { path: '/ticketchangeconfirm', component: TicketChangeConfirm },
        { path: '/trainadd', component: TrainAdd },
        { path: '/stationadd', component: StationAdd },
        { path: '/carriageadd', component: CarriageAdd },
        { path: '/traindelete', component: TrainDelete },
        { path: '/trainchange', component: trainChange },
        { path: '/workspace', component: workSpace },
        { path: '/contactadd', component: ContactAdd },
        { path: '/ticketpay', component: TicketPay },
        { path: '/useradd',component:UserAdd},
        { path: '/userchange',component:UserChange},
        { path: '/userlist',component:UserList},
        { path: '/messagelist',component:MessageList},
        { path: '/:pathMatch(.*)*',redirect:'/'}
        // ... 其他路由规则
    ]
});

const debounce = (fn, delay) => {
    let timer = null;
    return function () {
        let context = this;
        let args = arguments;
        clearTimeout(timer);
        timer = setTimeout(function () {
            fn.apply(context, args);
        }, delay);
    }
}

const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver{
    constructor(callback) {
        callback = debounce(callback, 16);
        super(callback);
    }
}


const app = createApp(App);
app.use(router);
app.use(store);
app.use(ElementPlus)
app.mount('#app');
