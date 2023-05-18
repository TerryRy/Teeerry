<template>
  <div id="topline"><TopLine/></div>
  <div id="all">
    <div id="welcomeWord"><p>欢迎使用畅游中国!</p></div>
    <div id="Dev">
      <form id="register-form" v-if="loginMode===0">
        <h3>注册</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username"/><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password"/><br><br>
        <input class="scn" type="password" placeholder="确认密码" v-model="confirmPassword"/><br><br>
        <input class="scn" type="email" placeholder="邮箱" v-model="email"/><br><br>
        <input type="submit" value="注册" @click="register" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <p>
          已有账号？<a href="#" @click="toggleForm(1)">去登录</a>
        </p>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>

      <form id="login-form" v-else-if="loginMode===1">
        <h3>登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="button" value="登录" @click="login" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <p>
          没有账号？<a href="#" @click="toggleForm(0)">去注册</a>
        </p>
        <input type="button" value="系统管理员入口" @click="toggleForm(2)" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        &nbsp;&nbsp;
        <input type="button" value="铁路系统员入口" @click="toggleForm(3)" style="background-color: rgb(7,231,145); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>

      <form id="login-form" v-else-if="loginMode===2">
        <h3>系统管理员登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="button" value="登录" @click="system_admin_login" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        &nbsp;&nbsp;
        <input type="button" value="返回用户登录" @click="toggleForm(1)" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>

      <form id="login-form" v-else-if="loginMode===3">
        <h3>铁路系统员登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="button" value="登录" @click="rail_admin_login" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        &nbsp;&nbsp;
        <input type="button" value="返回用户登录" @click="toggleForm(1)" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>

import axios from 'axios'
import TopLine from "@/components/common/TopLine.vue";
export default {
  name: "WelcomePage",
  components: {TopLine},
  computed: {
    user() {
      return this.$store.getters.getUser;
    }
  },
  props:{

  },
  data(){
    return{
      //登录模式：0-注册，1-用户登录，2-系统管理员登录，3-铁路系统员登录
      loginMode : 1, //默认的初始界面就是用户登录界面
      username : null,
      password : null,
      email:null,
      confirmPassword:null
    }
    },
  methods:{
    //设置登录模式
    toggleForm(mode){
      this.loginMode=mode;
    },

    //用户登录
    login(){
      if(this.username==null)
      {
        alert("用户名不能为空！");
        return;
      }
      if(this.password==null)
      {
        alert("密码不能为空！");
        return;
      }
      const user = this.username;
      alert(user);
      this.$store.dispatch('login', user);
      localStorage.setItem('username', user);
      this.$router.push('/homepage');
      /*
      axios.post('{{base_url}}/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then(function(response)
          {
            switch(response.data.result){
              case 0:
              {
                const user = this.username;
                this.$store.dispatch('login', user);\
                localStorage.setItem('username', user);
                this.$router.push('/homepage');
                break;
              }
              default:
                alert("用户名或密码错误，请检查后重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})*/
    },

    //注册
    register(){
      if(this.password!==this.confirmPassword)
      {
        alert("两次密码输入不一致！");
        return;
      }
      axios.post('{{base_url}}/users/register',
          {
            "name": this.username,
            "passwd":this.password,
            "email":this.email
          })
          .then(function(response){
            switch (response.status){
              case 200:
                alert("注册成功！");
                this.loginMode=1;
                break;
              case 500:
                alert("用户名已存在。");
                break;
              case 501:
                alert("服务器错误，请稍后重试。");
                break;
            }
          })
          .catch(function(){
            alert("网络错误，请稍后重试。");
          })
    },


    system_admin_login(){
      if(this.username==null)
      {
        alert("用户名不能为空！");
        return;
      }
      if(this.password==null)
      {
        alert("密码不能为空！");
        return;
      }
      const user = this.username;
      this.$store.dispatch('login', user);
      localStorage.setItem('username', user);
      this.$router.push('/userinfomanage');
      /*
      axios.post('{{base_url}}/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then(function(response)
          {
            switch(response.data.result){
              case 0:
              {
                const user = this.username;
                this.$store.dispatch('login', user);\
                localStorage.setItem('username', user);
                this.$router.push('/homepage');
                break;
              }
              default:
                alert("用户名或密码错误，请检查后重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})*/
    },

    //铁路系统员登录
    rail_admin_login(){
      if(this.username==null)
      {
        alert("用户名不能为空！");
        return;
      }
      if(this.password==null)
      {
        alert("密码不能为空！");
        return;
      }
      const user = this.username;
      this.$store.dispatch('login', user);
      localStorage.setItem('username', user);
      this.$router.push('/workspace');
      /*
      axios.post('{{base_url}}/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then(function(response)
          {
            switch(response.data.result){
              case 0:
              {
                const user = this.username;
                this.$store.dispatch('login', user);\
                localStorage.setItem('username', user);
                this.$router.push('/homepage');
                break;
              }
              default:
                alert("用户名或密码错误，请检查后重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})*/
    },
  }
}
</script>

<style scoped>
  #topline{
    position: relative;
    top:0px;
    padding-top: 0px;
  }
  #welcomeWord{
    position:absolute;
    width:100%;
    align-items:center;
    display: block;
    top:250px;
  }
  #welcomeWord p{
    margin-top: -15px;
    font-size: 47px;
    font-weight: bold;
    color: black;
    letter-spacing: 3px;
    font-family: 华光行书_CNKI, serif;
  }
  #buttons{
    display: flex;
    flex-wrap:wrap;
  }
  #input{
    position: absolute;
    width:100%;
    align-items:center;
    top:300px;
  }
  #Dev{
    font-size: 25px;
    margin: 30px;
    padding-top: 7px;
    padding-bottom: 13px;
    padding-left: 30px;
    padding-right: 30px;
    background-color: rgb(255, 255, 255, 0.6);
    position: absolute;
    top: 300px;
    width: 600px;
    /*vertical-align: middle;*/
    justify-content: center;
    align-items: center;
    display: flex;
    border-radius: 10px;
  }
  #all {
    justify-content: center;
    align-items: center;
    display: flex;
  }
  #input p{
    color: black;
  }
  #Dev a{
    text-decoration: none;
    color: black;
    font-family: Microsoft YaHei,serif;
  }
  #Dev a:visited{
    text-decoration: none;
    color: black;
  }
  #Dev a:hover{
    text-decoration: none;
    color: skyblue;
  }

  .scn {
    border: none;
    height: 30px;
    border-radius: 5px;
  }

  input::placeholder {
    color: rgba(0,0,0,0.3);
  }

  form p{
    font-size: 18px;
  }
</style>