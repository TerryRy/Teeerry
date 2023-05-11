<template>
  <div id="content" v-if="pageno===1"><HomePage/></div>
  <div id="content" v-else-if="pageno===0"><WelcomePage :loginstatus="loginstatus" @login="loginstatus = 1"/></div>
  <div id="content" v-else-if="pageno===1100"><AccountAdd/></div>
</template>

<script>
import WelcomePage from "@/views/welcome_page/WelcomePage.vue";
import HomePage from "@/views/user/homepage/HomePage.vue";
import '@/assets/css/backgroundimage.css'
import AccountAdd from "@/views/user/account_add/AccountAdd.vue";

export default {
  name: 'App',
  components: {
    AccountAdd,
    WelcomePage,
    HomePage
  },
  data(){
    return{
      /*pageno表示我们显示哪个页面，规定：
      * 0-未登录状态下的欢迎页面
      *
      * */
      pageno:1100,
      //以下是当前用户信息，适用于用户、管理员、铁路员
      cur_username:null,
      cur_email:null
    }
  },
  methods:{
    login(){
      this.pageno = 1000
    },
    logout(){
      this.pageno = 0;
      this.cur_username = null;
      this.cur_email = null;
    }
  }
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
