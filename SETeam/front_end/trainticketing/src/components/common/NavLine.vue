<template>
  <nav>
    <ul>
      <li id="leftblock"><a href="/homepage" @click="turnToTicketBooking">车票预订</a></li>
      <li><a href="/orderlist" @click="turnToBillsManage">订单管理</a></li>
      <li><a href="/accountmanage" @click="turnToAccountManage">账户管理</a></li>
      <li><a href="/personalcenter" @click="turnToPersonalCenter">个人中心</a></li>
      <li id="rightblock"><a @click="logout">退出登录</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavLine",
  methods:{
    logout(){
      if(confirm('确定要退出登录吗?'))
      {
        this.$store.dispatch('logout');
        localStorage.setItem('username', null);
        this.$router.push('/');
      }
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
    position:fixed;
    top:80px;
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