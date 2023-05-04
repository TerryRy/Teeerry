<template>
  <div id="welcomeWord"><p>欢迎使用畅游中国！</p></div>
  <div id="input">
    <form id="register-form" v-if="isRegister">
      <h3>注册</h3>
      <input type="text" placeholder="用户名" v-model="username" /><br><br>
      <input type="password" placeholder="密码" v-model="password" /><br><br>
      <input type="password" placeholder="确认密码" v-model="confirmPassword" /><br><br>
      <input type="email" placeholder="邮箱" v-model="email" /><br><br>
      <input type="submit" value="注册" @click="register" />
      <p>
        已有账号？<a href="#" @click="toggleForm">去登录</a>
      </p>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>

    <form id="login-form" v-else>
      <h3>登录</h3>
      <input type="text" placeholder="用户名" v-model="username" /><br><br>
      <input type="password" placeholder="密码" v-model="password" /><br><br>
      <input type="submit" value="登录" @click="login" />
      <p>
        没有账号？<a href="#" @click="toggleForm">去注册</a>
      </p>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>
  </div>
</template>

<script>
import '@/assets/css/welcomepage.css'
export default {
  name: "WelcomePage",
  props:{
    loginstatus: {
      type:Boolean,
      require:true
    }
  },
  data(){
    return{
      isRegister : true
    }
    },
  methods:{
    toggleForm(){
      this.isRegister=!(this.isRegister)
    },
    login(){
      this.$emit('1000');
    }

  }
}
</script>

<style scoped>
  #welcomeWord{
    position:absolute;
    width:100%;
    align-items:center;
    display: block;
    top:250px;
  }
  #welcomeWord p{
    font-size: 26px;
    font-family: Microsoft YaHei,serif;
    font-weight: bold;
    color: white;
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
  #input p{
    color:white;
  }
  #input a{
    text-decoration: none;
    color: white;
    font-family: Microsoft YaHei,serif;
  }
  #input a:visited{
    text-decoration: none;
    color: white;
  }
  #input a:hover{
    text-decoration: none;
    color: orangered;
  }
</style>