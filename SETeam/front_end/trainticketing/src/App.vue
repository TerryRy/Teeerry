<template>
  <!--<div id="content" v-if="pageno===1"><HomePage/></div>
  <div id="content" v-else-if="pageno===0"><WelcomePage @login="loginstatus = 1"/></div>
  <div id="content" v-else-if="pageno===1100"><AccountAdd @turnToAccountManage="pageno=1101" @turnToBillsManage="pageno=1200" @logout="logout"/></div>
  <div id="content" v-else-if="pageno===1101"><AccountManage @turnToDepositMoney="pageno=1102" @turnToAccountAdd="pageno=1100" @turnToAccountManage="pageno=1101" @turnToBillsManage="pageno=1200" @logout="logout"/></div>
  <div id="content" v-else-if="pageno===1102"><DepositMoney @turnToAccountManage="pageno=1101" @logout="logout" @turnToBillsManage="pageno=1200"/></div>
  <div id="content" v-else-if="pageno===1200"><OrderList @turnToAccountManage="pageno=1101" @logout="logout" @turnToBillsManage="pageno=1200" @turnToOrderDetails="pageno=1201"/></div>
  <div id="content" v-else-if="pageno===1201"><OrderDetails @turnToAccountManage="pageno=1101" @logout="logout" @turnToBillsManage="pageno=1200"/></div>
-->
  <router-view></router-view>
</template>

<script>
//import WelcomePage from "@/views/welcome_page/WelcomePage.vue";
//import HomePage from "@/views/user/homepage/HomePage.vue";
import '@/assets/css/backgroundimage.css'
//import AccountAdd from "@/views/user/account_add/AccountAdd.vue";
//import AccountManage from "@/views/user/account_manage/AccountManage.vue";
//import DepositMoney from "@/views/user/deposit_money/DepositMoney.vue";
//import OrderList from "@/views/user/order_list/OrderList.vue";
//import OrderDetails from "@/views/user/order_details/OrderDetails.vue";

export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#content{
  position: absolute;
  border-top: 0px;
  padding-top: 0px;
  top:0px;
  width:100%;
}

</style>
