<template>
  <nav>
    <ul>
      <li id="leftblock"><a href="/">首页</a></li>
      <li><a @click="turnto('/messagelist')">通知公告</a></li>
      <li><a @click="turnto('/orderlist')">订单管理</a></li>
      <li><a @click="turnto('/accountmanage')">账户管理</a></li>
      <li id="rightblock"><a @click="turnto('/personalcenter')">联系人管理</a></li>

<!--      <li @click="dialogTableVisible = true">登录</li>-->
<!--      <li id="rightblock"><a @click="logout">退出登录</a></li>-->
    </ul>
  </nav>
</template>

<script>
import {ElMessage} from "element-plus";
import "@/assets/css/button.css";

export default {
  name: "NavLine",
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    jwt(){
      return this.$store.getters.getJwt;
    },
    isnotlogin(){
      return this.jwt==="null"||this.jwt===null;
    }
  },
  methods:{
    turnto(url){
      if(this.isnotlogin)
      {
        ElMessage({message:"请先登录",type:'warning'});
      }
      else this.$router.push(url);
    }

  }
}
</script>

<style scoped>
  nav {
    background-color: #66b9de;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    position:relative;
    width: 100%;
  }

  nav ul {
    list-style: none;
    margin: 0;
    padding:0;
    display: flex;
    justify-content: space-between;
  }

  nav li {
    width:25%;
    margin: 0 10px;
  }

  nav a {
    color: #fff;
    text-decoration: none;
    padding: 10px;
    display: inline-block;
  }

  nav a:hover {
    background-color: #0c96cb;
    padding-left: 12%;
    padding-right: 12%;
    display: block;
    font-size:20px;
  }

  #leftblock {
    padding-left: 10%;
  }
  #rightblock {
    padding-right: 10%;
  }
</style>