<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>为您的账户充值</p>
    </div>
    <div id="accountinput">
      <form id="register-form">
        <div>
          <p>充值账户：{{this.account.name}}</p>
          <label for="recharge-amount">充值金额：</label>
          <input type="number" class="scn" id="recharge-amount" v-model="rechargeAmount"><br><br>
        </div>
        <input type="button" value="充值" @click="depositMoney(this.account,this.rechargeAmount)" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
        <a href="/accountmanage"><input type="button" value="返回" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/></a>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import axios from "axios";

export default {
  name: "DepositMoney",
  components: {NavLine, TopLine},
  computed: {
    account() {
      return this.$store.getters.getAccount;
    },
    jwt(){
      return this.$store.getters.getJwt;
    }
  },
  data(){
    return{
      rechargeAmount:0
    }
  },
  mounted() {
    const jwt = localStorage.getItem('jwt');
    if (jwt) {
      this.$store.commit('setJwt', jwt);
    }
  },
  methods:{
    depositMoney(account,amount)
    {
      if(amount<=0)
      {
        alert("请输入合法的金额。");
      }
      axios.put(`/api/accounts/${account.id}`,{"amount":amount},{headers:{'jwt': `${this.jwt}`}})
          .then((response)=>{
            alert(response.data.message);
          })
          .catch(function (){alert("网络错误")});
      //this.$router.push('/accountmanage');
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
  background-color: rgba(255, 255, 255, 0.8);;
  width:100%;
  text-align: center;
  height: calc(100vh - 150px);
}

#introduceWord{
  position: relative;

  width:100%;
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
  width: 100%;
  align-items:center;
  display: block;
  top:100px;
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