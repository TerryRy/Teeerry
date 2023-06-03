<template>
    <nav>
			<ul>
        <li id="leftblock"><a href="/useradd" @click="turnToUserAdd">新增用户</a></li>
        <li id="rightblock"><a href="/userlist" @click="turnToUserList">用户管理</a></li>
<!--        <li id="rightblock"><a href="/userchange" @click="turnToUserChange">修改用户信息</a></li>-->
      </ul>
    </nav>
  </template>
  
  <script>
  export default {
    name: "NavLine",
    methods:{
      turnToUserList(){
        this.$emit('turnToUserList');
      },
      turnToUserAdd(){
        this.$emit('turnToUserAdd');
      },
      turnToUserChange(){
        this.$emit('turnToUserChange');
      },
    }
  }
  </script>
  
  <style scoped>
    nav {
      background-color: #66b9de;
      color: #fff;
      font-size: 18px;
      font-weight: bold;
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
      width:60%;
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