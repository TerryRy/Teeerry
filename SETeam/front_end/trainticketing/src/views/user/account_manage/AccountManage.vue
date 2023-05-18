<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>账户管理</p>
    </div>
    <div id="secondFloor">
      <div id="money">
        <div><h3>{{username}},您好!<br>您的账户情况如下:</h3></div>
        <div><p>账户余额:{{money}}元</p></div>
        <div><p>账户数量:{{amount}}</p></div>
        <div>
          <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="turnToDepositMoney">充值</button>
          &nbsp;&nbsp;
          <button style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="add">添加账户</button>
        </div>
      </div>
      <div class="card-grid">
        <div class="card">
          <div class="cardInfo">
            <p3>我的银行卡</p3>
            <p>6210000000000006666</p>
          </div>
          <div><button>删除账户</button></div>
        </div>
        <div class="card">银行卡账户 1</div>
        <div class="card">银行卡账户 1</div>
        <div class="card">银行卡账户 1</div>
        <div class="card">银行卡账户 1</div>
        <div class="card">银行卡账户 1</div>
        <div class="card">银行卡账户 1</div>
      </div>
    </div>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";

export default {
  name: "AccountManage",
  components: {TopLine, NavLine},
  data(){
    return{
      money:0,
      amount:0,
      username:"尊敬的用户"
    }
  },

  methods:{
    turnToAccountManage()
    {
      this.$emit('turnToAccountManage');
    },
    logout()
    {
      this.$emit('logout');
    },
    add()
    {
      this.$emit('turnToAccountAdd')
    },
    turnToDepositMoney()
    {
      this.$emit('turnToDepositMoney');
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
#topline{
  position: fixed;
  z-index: 9999;
}
#nav{
  position: fixed;
  z-index: 9999;
}

#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);
  top:150px;
  width:1400px;
  height: 100vh;
  text-align: center;
  z-index: 10;
}

#introduceWord{
  position: fixed;
  width:1400px;
  align-items:center;
  display: block;
  top:200px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#secondFloor{
  position: fixed;
  top:300px;
  padding: 0;
  margin: 0;
  display: flex;
}

#money{
  position: absolute;
  top:0px;
  left:50px;
  width:600px;
  padding-top: 100px;
}

#money p{
  font-size: 20px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#money h3{
  font-family: 华光行书_CNKI, serif;
  font-size: 30px;
}

.card-grid {
  position: absolute;
  top:0px;
  left:750px;
  width:600px;
  display: grid;
  grid-template-rows: repeat(3, 1fr); /* 三列网格 */
  grid-gap: 10px; /* 网格之间的间距 */
  height: 400px;
  padding: 10px;
  padding-top: 40px;
  overflow-y: scroll;
}

.card {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 20px;
  text-align: center;
  font-size: 16px;
  height: 50px;
  display: flex;
}

.cardInfo{
  width: 450px;
}

.card button{
  background-color: #ec1616;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}
</style>