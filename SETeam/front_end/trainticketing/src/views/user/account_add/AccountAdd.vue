<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
    <p>添加您的银行卡账户</p>
    </div>
    <div id="accountinput">
      <form id="register-form">
        <p>请设置账户名称</p><input class="scn" type="text" placeholder="账户名称" v-model="accountName"/><br><br>
        <p>请输入银行卡号</p><input class="scn" type="text" placeholder="银行卡号" v-model="accountID"/><br><br>
        <input type="button" value="添加" @click="addAccount" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
        <a href="/accountmanage"><input type="button" value="返回" @click="turnToAccountManage" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/></a>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  name: "AccountAdd",
  components: {
    NavLine,
    TopLine
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    jwt(){
      return this.$store.getters.getJwt;
    }
  },
  data(){
    return{
      accountName:null,
      accountID:null
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
    addAccount()
    {
      if(this.user==="null"||this.jwt==="null")
      {
        ElMessage({message:"登录已过期，请重新登录",type:'warning'});
        this.$store.dispatch('logout');
        localStorage.setItem('username', null);
        this.$router.push('/');
        return;
      }
      if(this.accountName===null)
      {
        ElMessage({message:"请填写账户名称",type:'warning'});
      }
      if(this.accountID===null)
      {
        ElMessage({message:"请填写银行卡号",type:'warning'});
      }
      axios.post('api/accounts/',
          {
            "account_name": this.accountName,
            "card_holder_name": this.user,
            "card_id": this.accountID
          },{headers:{'jwt': `${this.jwt}`}})
          .then(function(response){
            if(response.data.result!==0)
            {
              ElMessage.error(response.data.message);
            }
            else
            {
              ElMessage({message:response.data.message,type:'success'});
            }
          })
          .catch(function(){
            ElMessage.error("网络错误，请稍后重试。");
          })
    }
  }
}
</script>

<style scoped>
#topline{
  position: relative;
}
#nav{
  position: relative;
}
#mainBlock{
  margin:0 auto;
  height: calc(100vh - 150px);
  background-color: rgba(255, 255, 255, 0.8);;
  width:100%;
  text-align: center;
}

#introduceWord{
  position: relative;

  width:500px;
  margin: 0 auto;
  align-items:center;
  display: block;
  top:50px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#accountinput{
  position: relative;
  width: 200px;
  padding:0;
  margin: 0 auto;
  align-items:center;
  display: block;
  top:50px;
}

.footer p {
  margin: 0;
  font-size: 14px;
}

.footer a {
  color: #fff;
  text-decoration: none;
  margin-left: 10px;
}

.footer {
  left: 0;
  bottom: 0;
  width: 100%;
  height: 80px; /* 底边栏的高度 */
  background-color: #333;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>