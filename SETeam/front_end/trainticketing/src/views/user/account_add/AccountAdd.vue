<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
    <div id="introduceWord">
    <p>添加您的银行卡账户</p>
    </div>
    <div id="accountinput">
      <form id="register-form">
        <p>请设置账户名称</p><input class="scn" type="text" placeholder="账户名称" v-model="accountName"/><br><br>
        <p>请输入银行卡号</p><input class="scn" type="text" placeholder="银行卡号" v-model="accountID"/><br><br>
        <input type="button" value="添加" @click="addAccount" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
        <input type="button" value="返回" @click="turnToAccountManage" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";

export default {
  name: "AccountAdd",
  components: {
    NavLine,
    TopLine
  },
  methods:{
    addAccount()
    {
      alert("添加失败！");
    },
    logout()
    {
      this.$emit('logout');
    },
    turnToAccountManage()
    {
      this.$emit('turnToAccountManage');
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
  top:300px;
}
</style>