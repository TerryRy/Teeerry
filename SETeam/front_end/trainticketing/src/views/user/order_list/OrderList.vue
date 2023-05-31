<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>订单管理</p>
      <!--<div>
        <button @click="removeUselssBills">一键清除无效订单</button>
      </div>-->
    </div>
    <div id="secondFloor">
      <div class="bill-grid">
        <p v-if="this.bills.length===0">您当前暂无订单，快去买票吧！</p>
        <a href="/homepage">
          <button v-if="this.bills.length===0" style="background-color: rgb(102,185,222); color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">去买票</button>
        </a>
        <div class="bill" v-for="bill in bills" :key="bill.id">
          <div class="billInfo">
            <p class="id">{{bill.id}}</p>
            <div class="seatInfo">
              <span>车次：{{bill.schedule.schedule_no}}&nbsp;&nbsp;
                车厢号：{{bill.carriage.name}}&nbsp;&nbsp;
                座位号：{{bill.seat_no}}&nbsp;&nbsp;<br>

                出发时间：{{bill.schedule.departure_time}}&nbsp;&nbsp;
                票价：{{bill.amount}}元
              </span><br>
              <span>
<!--                {{bill.ori_station.station_no}}&#45;&#45;&#45;&#45;&ndash;&gt;{{bill.dst_station}}-->
<!--                出发车站：{{bill.schedule.departure_station.name}}&nbsp;&nbsp;-->
<!--                目的车站：{{bill.schedule.destination_station.name}}-->
              </span>
            </div>
          </div>
            <button id="button3" v-if="!bill.is_paid" @click="pay(bill)">支付</button>
            <button id="button2" @click="deletebill(bill)" v-if="checktime(bill.schedule.departure_time)||(!bill.is_paid)">删除</button>
            <button id="button1" @click="showdetails(bill)">详情</button>
        </div>
      </div>
    </div>
    <div class="footer">
      <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
    </div>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import {toDisplayString} from "vue";
import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";

export default {
  name: "OrderList",
  components: {NavLine, TopLine},
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
      bills:[]
    }
  },
  mounted() {
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
    }
    const jwt = localStorage.getItem('jwt');
    if (jwt) {
      this.$store.commit('setJwt', jwt);
    }
    axios.get('api/tickets/',{headers:{'jwt': `${this.jwt}`}})
        .then((response) => { // 使用箭头函数
          this.bills=response.data.tickets;
        })
        .catch(function(){alert("网络异常，请稍后重试。");})
  },
  methods:{
    toDisplayString,
    showdetails(bill)
    {
      this.$store.dispatch('storeBill', bill);
      localStorage.setItem('bill', bill);
      this.$router.push('/orderdetails');
    },
    pay(bill)
    {
      this.$store.dispatch('storeTicketID', bill.id);
      localStorage.setItem('ticketID', bill.id);
      this.$router.push('/ticketpay');
    },
    deletebill(bill)
    {
      ElMessageBox.confirm('确定要删除这个订单吗?',
          '删除订单',
          {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }
      )
          .then(()=>{
            axios.delete(`/api/tickets/${bill.id}`,{headers:{'jwt': `${this.jwt}`}})
                .then((response)=>
                {
                  if(response.data.result===0)
                  {
                    ElMessage({message:response.data.message,type:'success'});
                    this.$router.go(0);
                  }
                  else ElMessage.error(response.data.message);
                })
                .catch(function (){ElMessage.error("出现一点问题……")})

          })
          .catch(()=>{})

    },
    checktime(time) {
      let currentTime = new Date();
      let inputDate = new Date(time);

      // 比较输入时间是否超过一小时
      if (inputDate.getTime() > currentTime.getTime()) {
        return false;
      } else {
        return true;
      }
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
  width:1400px;
  text-align: center;
  z-index: 10;
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
  position: relative;
  top:0px;
  padding: 0;
  margin: 0;
  display: flex;
}


.bill-grid {
  position: relative;
  top:50px;
  left:200px;
  width:1000px;
  display: grid;
  grid-template-rows: repeat(7, 1fr);
  grid-gap: 3px; /* 网格之间的间距 */
  max-height: 550px;
  padding: 10px;
  border-top: 40px;
  overflow-y: scroll;
}

.bill {
  background-color: rgb(103, 186, 222,0.45);
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  font-size: 16px;
  height: 70px;
  display: flex;
  border-radius: 10px;

}

.id{
  margin: 0;
  padding: 0;
  top:0;
  left:0;
  font-size: 10px;
}

.seatInfo{
  text-align: left;
  display: inline-block;
}

#button1{
  display: inline-block;
  position: absolute;
  right:50px;
  background-color: #ff8102;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#button2{
  display: inline-block;
  position: absolute;
  right:120px;
  background-color: #ec2f16;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#button3{
  display: inline-block;
  position: absolute;
  right:190px;
  background-color: #38b7e8;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
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
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 80px; /* 底边栏的高度 */
  background-color: #333;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>