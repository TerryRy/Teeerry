<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>订单管理</p>
      <div>
        <button @click="removeUselssBills">一键清除无效订单</button>
      </div>
    </div>
    <div id="secondFloor">
      <div class="bill-grid">
        <div class="bill" @click="turnToOrderDetails">订单 1</div>
        <div class="bill">订单 1</div>
        <div class="bill">订单 1</div>
        <div class="bill">订单 1</div>
        <div class="bill">订单 1</div>
        <div class="bill">订单 1</div>
        <div class="bill">订单 1</div>
      </div>
    </div>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";

export default {
  name: "OrderList",
  components: {NavLine, TopLine},
  methods:{
    turnToAccountManage()
    {
      this.$emit('turnToAccountManage');
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
    },
    removeUselssBills()
    {
      alert("此功能尚未开发");
    },
    turnToOrderDetails()
    {
      this.$emit("turnToOrderDetails");
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

#introduceWord button{
  position: absolute;
  right:200px;
  background-color: #ec1616;
  color: #ffffff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#secondFloor{
  position: fixed;
  top:300px;
  padding: 0;
  margin: 0;
  display: flex;
}


.bill-grid {
  position: absolute;
  top:0px;
  left:200px;
  width:1000px;
  display: grid;
  grid-template-rows: repeat(3, 1fr);
  grid-gap: 10px; /* 网格之间的间距 */
  height: 500px;
  padding: 10px;
  padding-top: 40px;
  overflow-y: scroll;
}

.bill {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 20px;
  text-align: center;
  font-size: 16px;
  height: 50px;
}
</style>