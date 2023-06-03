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
        <tr v-if="bill.schedule">
          <th class="vertical-header">乘坐车次</th>
          <td>{{bill.schedule.schedule_no}}</td>
        </tr>
        <tr v-if="bill.schedule">
          <th class="vertical-header">车厢号</th>
          <td>{{bill.carriage.name}}</td>
        </tr>
        <tr v-if="bill.schedule">
          <th class="vertical-header">座位号</th>
          <td>{{bill.seat_no}}</td>
        </tr>
        <tr v-if="bill.schedule">
          <th class="vertical-header">出发时间</th>
          <td>{{bill.schedule.departure_time}}</td>
        </tr>
        <tr v-if="bill.ori_station">
          <th class="vertical-header">出发地</th>
          <td>{{bill.ori_station.name}}</td>
        </tr>
        <tr v-if="bill.dst_station">
          <th class="vertical-header">目的地</th>
          <td>{{bill.dst_station.name}}</td>
        </tr>
        </tbody>
      </table>
      <div id="buttons">
        <button style="background-color: #f6bf0b; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="returnticket(bill)"  v-if="((!bill.schedule)||checktime(bill.schedule.departure_time)&&(bill.is_paid))">退票</button>
        &nbsp;
        <button @click="changeticket(bill)" style="background-color: #24c6e3; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"  v-if="((!bill.schedule)||checktime(bill.schedule.departure_time)&&(bill.is_paid))">改签</button>
        &nbsp;
        <a href="/orderlist"><button style="background-color: rgba(49,79,222,0.21); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">返回</button></a>
      </div>
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
import {ElMessage} from "element-plus";

export default {
  name: "OrderDetails",
  components: {NavLine, TopLine},
  computed: {
    bill() {
      return this.$store.getters.getBill;
    },
    username(){
      return this.$store.getters.getUser;
    },
    jwt(){
      return this.$store.getters.getJwt;
    }
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
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
      axios.delete(`/api/tickets/${bill.id}`, {headers:{'jwt': `${this.jwt}`}})
          .then((response)=>
          {
            switch (response.data.result){
              case 0:
                ElMessage({message:response.data.message,type:'success'});
                this.$router.push('/orderlist');
                break;
              default:
                ElMessage.error(response.data.message);
            }
          })
          .catch(()=>{ElMessage.error("出现一点问题……");})
    },
    changeticket()
    {
      this.$store.commit('setTicketID', this.bill.id);
      localStorage.setItem('ticketID',this.bill.id);
      this.$router.push('/ticketchangechoice');
    },
    checktime(time) {
      let currentTime = new Date();
      let inputDate = new Date(time);

      // 比较输入时间是否超过一小时
      return inputDate.getTime() > currentTime.getTime() + 60 * 60 * 1000;
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
  background-color: rgba(255, 255, 255, 0.8);
  top:150px;
  width:100%;
  text-align: center;
  z-index: 10;
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

#secondFloor{
  position: relative;
  top:50px;
  padding: 0;
  margin: 0;
}

table {
  border-collapse: collapse;
  width: 800px;
  margin: 0 auto;
  padding-top: 50px;
  position: relative;
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
  width: 100%;
  margin: 0 auto;
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