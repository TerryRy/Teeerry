<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>订单详情</p>
    </div>
    <div id="secondFloor">
      <table>
        <tbody>
        <tr>
          <th class="vertical-header">乘车人姓名</th>
          <td>{{username}}</td>
        </tr>
        <tr>
          <th class="vertical-header">乘坐车次</th>
          <td>{{bill.schedule.schedule_no}}</td>
        </tr>
        <tr>
          <th class="vertical-header">车厢号</th>
          <td>{{bill.carriage.name}}</td>
        </tr>
        <tr>
          <th class="vertical-header">座位号</th>
          <td>{{bill.seat_no}}</td>
        </tr>
        <tr>
          <th class="vertical-header">出发时间</th>
          <td>{{bill.schedule.departure_time}}</td>
        </tr>
        <tr>
          <th class="vertical-header">出发地</th>
          <td>{{bill.schedule.departure_station.name}}</td>
        </tr>
        <tr>
          <th class="vertical-header">目的地</th>
          <td>{{bill.schedule.destination_station.name}}</td>
        </tr>
        </tbody>
      </table>
      <div id="buttons">
        <button style="background-color: #f6bf0b; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="returnticket(bill)"  v-if="!(bill.is_expired)">退票</button>
        &nbsp;
        <a href="/ticketchangechoice"><button style="background-color: #24c6e3; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"  v-if="!(bill.is_expired)">改签</button></a>
        &nbsp;
        <a href="/orderlist"><button style="background-color: rgba(49,79,222,0.21); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">返回</button></a>
      </div>
    </div>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import axios from "axios";

export default {
  name: "OrderDetails",
  components: {NavLine, TopLine},
  computed: {
    bill() {
      return this.$store.getters.getBill;
    },
    username(){
      return this.$store.getters.getUser;
    }
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
    }
    const bill = localStorage.getItem('Bill');
    if(bill) {
      this.$store.commit('setBill',bill);
    }
  },
  data(){
    return{
      valid:true
    }
  },
  methods:{
    returnticket(bill)
    {
      axios.delete(`/api/schedules/tickets/${bill.id}`, {headers:{'jwt': `${this.jwt}`}})
          .then((response)=>
          {
            switch (response.data.result){
              case 0:
                alert("退票成功！");
                this.$router.push('/orderlist');
                break;
              default:
                alert("出现一个问题……");
            }
          })
          .catch(function (){alert("网络错误。")});

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

table {
  border-collapse: collapse;
  width: 800px;
  margin-left: 300px;
  margin-right: 300px;
  padding-top: 50px;
  position: absolute;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #66b9de;
  font-weight: bold;
  width: 300px;
}

td{
  width: 500px;
  background-color: lightcyan;
}

#buttons{
  position: relative;
  width: 1400px;
  top:350px;
}
</style>