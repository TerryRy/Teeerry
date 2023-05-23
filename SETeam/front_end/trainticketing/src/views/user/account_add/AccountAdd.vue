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
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";

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
      if(this.user==="null")
      {
        alert("登录已过期，请重新登录");
        this.$store.dispatch('logout');
        localStorage.setItem('username', null);
        this.$router.push('/');
        return;
      }
      if(this.accountName===null)
      {
        alert("请填写账户名称");
      }
      if(this.accountID===null)
      {
        alert("请填写银行卡号");
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
              alert(response.data.message);
            }
            else
            {
              alert("添加成功！");
            }
          })
          .catch(function(){
            alert("网络错误，请稍后重试。");
          })
      /*
      axios.post('{{base_url}}/accounts/',
          {
            "account_name": this.accountName,
            "card_holder_name":this.user,
            "card_id":this.accountID
          })
          .then(function(response)
          {
            switch(response.data.result){
              case 0:
              {
                alert("账户添加成功！")
                break;
              }
              default:
                alert("出现问题，请重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})

       */
    }
  }
}
</script>

<style scoped>
#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);;
  width:1400px;
  height: 100vh;
  text-align: center;
}

#introduceWord{
  position: fixed;

  width:1400px;
  align-items:center;
  display: block;
  top:250px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#accountinput{
  position: fixed;
  width: 200px;
  padding-right: 600px ;
  padding-left: 600px ;
  align-items:center;
  display: block;
  top:300px;
}
</style>