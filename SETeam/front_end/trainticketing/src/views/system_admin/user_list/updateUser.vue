<template>
    <h2>要旅行，就来畅游中国！</h2>
    <form id="register-form">
        <h3>更改信息</h3>
        <input className="scn" type="text" placeholder="用户名(2-10个字符)" v-model="username"/><br><br>
        <input className="scn" type="email" placeholder="邮箱" v-model="email"/><br><br>
        <input type="button" value="提交修改" @click="updateUser"
               style="background-color: rgba(102,185,222,1); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
    </form>

</template>

<script>

import axios from 'axios'
import {ElMessage, ElMessageBox} from "element-plus";

export default {
    name: "updateUser",
    computed: {
        user() {
            return this.$store.getters.getUser;
        },
      jwt(){
        return this.$store.getters.getJwt;
      }
    },
    props: {},
    data() {
        return {
            //注册登录时涉及的用户信息，初始化为null
            username: '',
            password: '',
            confirmPassword: '',
            email: ''
        }
    },
    methods: {
        updateUser() {
          // alert(this.username);
            if (this.username === null || this.username === "null"||this.username.length===0) {
                this.username = this.$store.getters.getUserName;
            }
            if (this.email === null || this.email === "null"||this.email.length===0) {
                this.email = this.$store.getters.getUserEmail;
            }

            if (this.username === null || this.username === "null") {
                ElMessageBox.alert("error");
                return;
            }
            // alert(this.username);
        //    alert(this.username.length);
            //要求用户名为2-10个字符
            if (!(this.username.length >= 2 && this.username.length <= 10)) {
                ElMessageBox.alert("用户名应为2-10个字符！");
                return;
            }

            axios.put('/api/users/' + this.$store.getters.getUserId,
                {
                    "name": this.username,
                    "email": this.email
                },{headers:{'jwt': `${this.jwt}`}})
                .then(function (response) {
                    if (response.data.result === 0)
                        ElMessage({message: response.data.message, type: 'success'});
                    else
                        ElMessage({message: response.data.message, type: 'warning'});
                    this.$emit('updated');
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
                    }
                })
        },
    },

    mounted() {
      const jwt = localStorage.getItem('jwt');
      if(jwt){
        this.$store.commit('setJwt', jwt);
      }
    }
}
</script>

<style scoped>

p {
    color: black;
}

a {
    text-decoration: none;
    color: black;
    font-family: Microsoft YaHei, serif;
}

a:visited {
    text-decoration: none;
    color: black;
}

a:hover {
    text-decoration: none;
    color: skyblue;
    transition: 0.7s all;
    -webkit-transition: 0.7s all;
}

/*.scn {*/
/*    height: 30px;*/
/*    border-color: #cccccc;*/
/*    border-width: 2px;*/
/*    border-radius: 5px;*/
/*    padding: 2px;*/
/*    width: 300px;*/
/*}*/

input::placeholder {
    color: rgba(0, 0, 0, 0.3);
}

form p {
    font-size: 18px;
}
</style>