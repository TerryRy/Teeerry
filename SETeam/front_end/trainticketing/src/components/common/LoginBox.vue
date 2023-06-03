<template>
      <h2>要旅行，就来畅游中国！</h2>
      <form id="register-form" v-if="loginMode===0">
        <h3>注册</h3>
        <input class="scn" type="text" placeholder="用户名(2-10个字符)" v-model="username"/><br><br>
        <input class="scn" type="password" placeholder="密码(6-10个字符)" v-model="password"/><br><br>
        <input class="scn" type="password" placeholder="确认密码" v-model="confirmPassword"/><br><br>
        <input class="scn" type="email" placeholder="邮箱" v-model="email"/><br><br>
        <input type="button" value="注册" @click="register" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <p>
          已有账号？<a href="#" @click="toggleForm(1)">去登录</a>
        </p>
      </form>

      <form id="login-form" v-else-if="loginMode===1">
        <h3>登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="button" value="登录" @click="login" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <p>
          没有账号？<a href="#" @click="toggleForm(0)">去注册</a>
        </p>
        <input type="button" value="系统管理员入口" @click="toggleForm(2)" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" />
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
      </form>

      <form id="login-form" v-else-if="loginMode===3">
        <h3>铁路系统员登录</h3>
        <input class="scn" type="text" placeholder="用户名" v-model="username" /><br><br>
        <input class="scn" type="password" placeholder="密码" v-model="password" /><br><br>
        <input type="button" value="登录" @click="rail_admin_login" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        &nbsp;&nbsp;
        <input type="button" value="返回用户登录" @click="toggleForm(1)" style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
      </form>
</template>

<script>

import axios from 'axios'
import {ElMessage, ElMessageBox} from "element-plus";
export default {
  name: "LoginBox",
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

      //注册登录时涉及的用户信息，初始化为null
      username : null,
      password : null,
      confirmPassword:null,
      email:null
    }
  },
  methods:{

    is_common_user(groups)
    {
      let i;
      for(i=0;i<groups.length;i++)
      {
        if(groups[i].name==="Common User") return true;
      }
      return false;
    },
    is_rail_admin(groups)
    {
      let i;
      for(i=0;i<groups.length;i++)
      {
        if(groups[i].name==="Train Admin") return true;
      }
      return false;
    },
    is_sys_admin(groups)
    {
      let i;
      for(i=0;i<groups.length;i++)
      {
        if(groups[i].name==="System Admin") return true;
      }
      return false;
    },
    //设置登录模式
    toggleForm(mode){
      this.loginMode=mode;
    },

    /*0-普通用户注册*/
    register(){
      //要求用户名为2-10个字符
      if (!(this.username.length >= 2 && this.username.length <= 10))
      {
        ElMessageBox.alert("用户名应为2-10个字符！");
        return;
      }

      //确保密码一致
      if(this.password!==this.confirmPassword)
      {
        ElMessageBox.alert("两次密码输入不一致！");
        return;
      }

      //要求密码必须是6-10位字符
      if (!(this.password.length >= 6 && this.password.length <= 10))
      {
        ElMessageBox.alert("密码应为6-10个字符！");
        return;
      }

      axios.post('/api/users/register',
          {
            "name": this.username,
            "passwd":this.password,
            "email":this.email
          })
          .then(function(response){
            if(response.data.result===0)
              ElMessage({message: response.data.message,type:'success'});
            else
              ElMessage({message: response.data.message,type:'warning'});
            this.toggleForm(1); //切换到用户登录模式
          })
          .catch(error => {
            // 处理请求过程中的错误
            console.error('请求出错：', error);

            // 检查错误的类型
            if (error.response) {
              // 服务器返回错误状态码
              console.error('响应状态码：', error.response.status);
              console.error('响应数据：', error.response.data);
            } else if (error.request) {
              // 请求已发送但没有收到响应
              console.error('没有收到响应');
            } else {
              // 发送请求时发生了错误
              console.error('请求发送失败：', error.message);
            }})
    },

    //1-普通用户登录函数
    login(){
      if(this.username==null)
      {
        ElMessage.error("用户名不能为空！");
        return;
      }
      if(this.password==null)
      {
        ElMessage.error("密码不能为空！");
        return;
      }
      //const user = this.username;
      //this.$store.dispatch('login', user);
      //localStorage.setItem('username', user);
      //this.$router.push('/homepage');
      axios.post('/api/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then((response) => { // 使用箭头函数
            if (response.data.result !== 0)
            {
              ElMessage.error(response.data.message);
              return;
            }
            else
            {
              ElMessage({message:response.data.message,type:'success'});
            }
            const user = this.username;
            const jwt = response.data.jwt;
            this.$store.dispatch('login', user, jwt);
            localStorage.setItem('username', user);
            localStorage.setItem('jwt', jwt);
            axios.get('/api/users/me',{headers:{'jwt': `${jwt}`}})
                .then((response)=>
                {
                  if(this.is_common_user(response.data.groups))
                  {
                    this.$emit('logined');
                  }
                  else if(this.is_sys_admin(response.data.groups))
                  {
                    this.$router.push('/userlist');
                  }
                  else if(this.is_rail_admin(response.data.groups))
                  {
                    this.$router.push('/workspace');
                  }
                })
          })
          .catch(function(){ElMessage.error("网络异常，请稍后重试。");})
    },

    //2-系统管理员登录函数
    system_admin_login(){
      if(this.username==null)
      {
        ElMessage.error("用户名不能为空！");
        return;
      }
      if(this.password==null)
      {
        ElMessage.error("密码不能为空！");
        return;
      }
      //const user = this.username;
      //this.$store.dispatch('login', user);
      //localStorage.setItem('username', user);
      //this.$router.push('/homepage');
      axios.post('/api/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then((response) => { // 使用箭头函数
            if (response.data.result !== 0) return;
            const user = this.username;
            const jwt = response.data.jwt;
            if(jwt===null||jwt===undefined) return;
            this.$store.dispatch('login', user, jwt);
            localStorage.setItem('username', user);
            localStorage.setItem('jwt', jwt);
            axios.get('/api/users/me',{headers:{'jwt': `${jwt}`}})
                .then((response)=>
                {
                  if(this.is_sys_admin(response.data.groups))
                  {
                    this.$router.push('/userlist');
                    return;
                  }
                  else if(this.is_rail_admin(response.data.groups))
                  {
                    this.$router.push('/workspace');
                    return;
                  }
                  ElMessage.warning("普通用户无权访问管理员界面！");
                })

          })
          .catch(function(){ElMessage.error("网络异常，请稍后重试。");})
    },

    //3-铁路系统员登录函数
    rail_admin_login(){
      axios.post('/api/users/login',
          {
            "name": this.username,
            "passwd":this.password
          })
          .then((response) => { // 使用箭头函数
            if (response.data.result !== 0) return;
            const user = this.username;
            const jwt = response.data.jwt;
            this.$store.dispatch('login', user, jwt);
            localStorage.setItem('username', user);
            localStorage.setItem('jwt', jwt);
            axios.get('/api/users/me',{headers:{'jwt': `${jwt}`}})
                .then((response)=>
                {
                  if(this.is_rail_admin(response.data.groups))
                  {
                    this.$router.push('/workspace');
                    return;
                  }
                  else if(this.is_sys_admin(response.data.groups))
                  {
                    this.$router.push('/userlist');
                    return;
                  }
                  ElMessage.warning("普通用户无权访问管理员界面！");
                })
          })
          .catch(function(){ElMessage.error("网络异常，请稍后重试。");})
    },

  }
}
</script>

<style scoped>

p{
  color: black;
}
a{
  text-decoration: none;
  color: black;
  font-family: Microsoft YaHei,serif;
}
a:visited{
  text-decoration: none;
  color: black;
}
a:hover{
  text-decoration: none;
  color: skyblue;
  transition: 0.7s all;
  -webkit-transition: 0.7s all;
}

.scn {
  height: 30px;
  border-color: #cccccc;
  border-width: 2px;
  border-radius: 5px;
  padding: 2px;
  width: 300px;
}

input::placeholder {
  color: rgba(0,0,0,0.3);
}

form p{
  font-size: 18px;
}
</style>