<template>
  <nav>
    <ul>
      <li id="leftblock"><a href="#">车票预订</a></li>
      <li><a href="#">订单管理</a></li>
      <li><a href="#">账户管理</a></li>
      <li><a href="#">个人中心</a></li>
      <li id="rightblock"><a href="#" @click="logout">退出登录</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: "NavLine",
  methods:{
    logout(){
      this.$emit('logout');
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