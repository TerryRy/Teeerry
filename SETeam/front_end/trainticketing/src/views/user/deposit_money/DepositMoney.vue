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
        <input type="button" value="充值" @click="depositMoney" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
        <a href="/accountmanage"><input type="button" value="返回" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/></a>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
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
    }
  },
  data(){
    return{
      rechargeAmount:0
    }
  },
  methods:{
    depositMoney()
    {
      alert("充值成功！");
      axios({
        "method": "PUT",
        "header": [],
        "body": {
          "mode": "raw",
          "raw": "{\r\n    \"amount\": {{amount}}\r\n}",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "{{base_url}}/accounts/1",
          "host": [
            "{{base_url}}"
          ],
          "path": [
            "accounts",
            "1"
          ]
        }
      });
      this.$router.push('/accountmanage');
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
  width: 1400px;
  align-items:center;
  display: block;
  top:350px;
}
</style>