<template>
  <div id="TopLine">
    <div v-if="dialogTableVisible" id="dia">
    <el-dialog class="custom-dialog"  style="height:500px;width: 800px;border-radius: 30px;" v-model="dialogTableVisible" modal:false>
      <el-row style="width: 100%">
        <el-col :span="12">
          <img src="@/assets/images/loginbk.gif" height="400" width="750">
        </el-col>
        <el-col :span="12" style="background-color: rgba(255,255,255,0.8)">
          <login-box @logined="dialogTableVisible=false"></login-box>
        </el-col>
      </el-row>

    </el-dialog>
    </div>
    <el-row style="width: 100%;height: 100%">
      <el-col :span="1">

      </el-col>
      <el-col :span="2" >
        <img src="@/assets/images/icon.png" style="width: 60px;height:60px;margin: 10px 0">
      </el-col>
      <el-col :span="10" style="text-align: left;height: 100%">
        <p style="font-size: 26px;font-family: Microsoft YaHei,serif;font-weight: bold;color: black;height: 80px">畅游中国铁路售票官方网站</p>
      </el-col>
      <el-col :span="8" style="text-align: left;height: 100%">

      </el-col>
      <el-col :span="2" style="text-align: left;height: 100%">
        <el-button v-if="isnotlogin" text style="height: 80px" @click="dialogTableVisible=true" type="primary">登录/注册</el-button>
        <el-button v-else text style="height: 80px" @click="logout" type="primary">退出登录</el-button>
      </el-col>
      <el-col :span="1" style="text-align: left;height: 100%">

      </el-col>
    </el-row>



  </div>
</template>

<script>

import {ElMessageBox} from "element-plus";
import LoginBox from "@/components/common/LoginBox.vue";

export default {
  name: "TopLine",
  components: {LoginBox},
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
  data(){
    return{
      dialogTableVisible:false,
    }
  },
  mounted() {
    // 从本地存储中恢复用户名到 Vuex 的 state 中
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
    }
    const jwt = localStorage.getItem('jwt');
    if(jwt){
      this.$store.commit('setJwt', jwt);
    }
  },
  methods:{
    logout(){
      ElMessageBox.confirm('确定要退出登录吗?',
          '退出登录',
          {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }
      )
          .then(()=>{
            this.$store.dispatch('logout');
            localStorage.setItem('username', null);
            localStorage.setItem('jwt',null);
            this.$router.push('/');
          })
          .catch(()=>{})
    }
  }
}
</script>

<style scoped>
  #TopLine{
    background-color: whitesmoke;
    overflow:hidden;
    display: flex;
    align-items: center;
    flex-wrap:wrap;
    position:relative;
    top:0px;
    width: 100%;
    height: 80px;
  }

  el-button:hover{
    color: #0c96cb;
  }



</style>