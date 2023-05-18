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
          <label for="account-name">账户名称：</label>
          <input type="text" class="scn" id="account-name" v-model="rechargeAmount"><br><br>
        </div>
        <!--<p>请设置账户名称</p><input class="scn" type="text" placeholder="账户名称" v-model="accountName"/><br><br>-->
        <div>
          <label for="recharge-amount">充值金额：</label>
          <input type="number" class="scn" id="recharge-amount" v-model="rechargeAmount"><br><br>
        </div>
        <input type="button" value="充值" @click="depositMoney" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
        <input type="button" value="返回" @click="turnToAccountManage" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";

export default {
  name: "DepositMoney",
  components: {NavLine, TopLine},
  methods:{
    turnToAccountManage()
    {
      this.$emit('turnToAccountManage');
    },
    depositMoney()
    {
      alert("充值失败");
    },
    logout()
    {
      this.$emit('logout');
    },
    turnToTicketBooking(){
      this.$emit('turnToTicketBooking');
    },
    turnToBillsManage(){
      this.$emit('turnToBillsManage');
    },
    turnToPersonalCenter(){
      this.$emit('turnToPersonalCenter');
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