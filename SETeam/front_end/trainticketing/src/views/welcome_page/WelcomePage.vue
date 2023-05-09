<template>
  <div id="topline"><TopLine/></div>
  <div id="all">
    <div id="welcomeWord"><p>欢迎使用畅游中国!</p></div>
    <div id="Dev">
      <form id="register-form" v-if="isRegister">
        <h3>注册</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username"/><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password"/><br><br>
        <input class="scn" type="password" placeholder="确认密码" v-model="confirmPassword"/><br><br>
        <input class="scn" type="email" placeholder="邮箱" v-model="email"/><br><br>
        <input type="submit" value="注册" @click="register" />
        <p>
          已有账号？<a href="#" @click="toggleForm">去登录</a>
        </p>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>

      <form id="login-form" v-else>
        <h3>登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="submit" value="登录" @click="login" />
        <p>
          没有账号？<a href="#" @click="toggleForm">去注册</a>
        </p>
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
  props:{
    loginstatus: {
      type:Boolean,
      require:true
    }
  },
  data(){
    return{
      isRegister : false
    }
    },
  methods:{
    toggleForm(){
      this.isRegister=!(this.isRegister)
    },
    login(){
      axios.post('/users/login',
          {
            "name": this.username,
            "passwd":this.password,
          })
          .then(function(response)
          {
            switch(response.status){
              case 200:
                this.$emit('login');
                break;
              case 404:
                alert("用户名或密码错误，请检查后重试。");
                break;
              case 500:
                alert("用户信息查询异常，请稍后重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})

    },
    register(){
      if(this.password!==this.confirmPassword)
      {
        alert("两次密码输入不一致！");
        return;
      }
      //axios.get('/users/register/<code>')
      //    .then(() =>{alert("注册成功！");this.isRegister=false;})
      //    .catch(() =>alert("注册失败，请稍后重试！"))
      axios.post('/users/register',
          {
            "name": this.username,
            "passwd":this.password,
            "email":this.email
          })
          .then(function(response){
            switch (response.status){
              case 200:
                alert("注册成功！");
                this.isRegister=false;
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
    }

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
  }

  input::placeholder {
    color: rgba(0,0,0,0.3);
  }

</style>