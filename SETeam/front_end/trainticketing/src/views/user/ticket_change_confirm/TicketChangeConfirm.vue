<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord" style="margin: 0 auto; text-align: center">
      <p style="margin: 0 auto; text-align: center">畅游中国————收银台</p>
    </div>
    <div id="secondFloor" style="width: 100%">
      <div class="schedule-list" style="margin: 0 auto; text-align: center; width:1100px">
        <el-table :data="tickets" style="width: 100%" stripe="true" border="true">
          <el-table-column label="乘车人姓名" width="100px">
            <template v-slot="{ row }">
              <!--              {{row}}-->
              {{row.contact.name}}
            </template>
          </el-table-column>
          <el-table-column label="公民身份号码" width="200px">
            <template v-slot="{ row }">
              {{row.contact.id_card}}
            </template>
          </el-table-column>
          <el-table-column label="车次" width="100px">
            <template v-slot="{ row }">
              {{row.schedule.schedule_no}}
            </template>
          </el-table-column>
          <el-table-column label="出发时间" width="100px">
            <template v-slot="{ row }">
              {{row.schedule.departure_time}}
            </template>
          </el-table-column>
          <el-table-column label="行程" width="300px">
            <template v-slot="{ row }">
              {{row.ori_station.name}}------------------->{{row.dst_station.name}}
            </template>
          </el-table-column>
          <el-table-column label="车厢号" width="100px">
            <template v-slot="{ row }">
              {{row.carriage.id}}
            </template>
          </el-table-column>
          <el-table-column label="座位号" width="100px">
            <template v-slot="{ row }">
              {{row.seat_no}}
            </template>
          </el-table-column>
          <el-table-column label="票价" width="100px">
            <template v-slot="{ row }">
              {{row.amount}}元
            </template>
          </el-table-column>
        </el-table>
      </div>
      <br><br>
      <div :key="ticketAmount" style="margin: 0 auto; text-align: center">
        <span>付款账户：</span>
        <el-select v-model="account" placeholder="请选择一个账户" :key="ticketAmount">
          <el-option
              v-for="item in accounts"
              :key="item.id"
              :label="item.name"
              :value="item.id"
          />
        </el-select>
      </div>
      <div style="position: relative;margin: 0 auto;top:100px">
        <button @click="pay(ticket_id)" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">支付</button>&nbsp;&nbsp;&nbsp;&nbsp;
        <a href="/orderlist"><button style="background-color: rgb(255,255,255); color: rgb(0,0,0); padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;">返回</button></a>
      </div>
    </div>
  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
  name: "TicketChangeConfirm",
  components: {TopLine, NavLine},
  computed: {
    jwt(){
      return this.$store.getters.getJwt;
    },
    ticket_id(){
      return this.$store.getters.getTicketID;
    },
    ticketAmount() {
      if (this.ticket) {
        return this.ticket.amount;
      }
      return 0; // 或者其他默认值
    }
  },
  data(){
    return{
      accounts:[],
      tickets:[],
      ticket:null,
      account:null
    }
  },

  mounted() {
    const jwt = localStorage.getItem('jwt');
    if(jwt){
      this.$store.commit('setJwt', jwt);
    }
    const ticket_id=localStorage.getItem('ticketID');
    if(ticket_id){
      this.$store.commit('setTicketID', ticket_id);
    }
    axios.get(`/api/tickets/${this.ticket_id}`,
        {
          headers:{'jwt': `${this.jwt}`}
        })
        .then((response)=>
        {
          this.ticket=response.data;
          this.tickets.push(this.ticket);
        })
        .catch(function(){alert("网络异常，请稍后重试！")})
    axios.get('/api/accounts/',
        {
          headers:{'jwt': `${this.jwt}`}
        })
        .then((response)=>
        {
          this.accounts=response.data.accounts;
        })
        .catch(function(){alert("网络异常，请稍后重试！")})
  },

  methods:{
    // eslint-disable-next-line no-unused-vars
    pay(id)
    {
      axios.patch(`/api/tickets/${id}`,{"account_id":this.account},{headers:{'jwt': `${this.jwt}`}})
          .then((response)=>
          {
            if(response.data.result===0)
            {
              ElMessage({message: response.data.message,type:'success',zIndex:'20000'});
              this.$router.push('/orderlist');
            }
            else
            {
              ElMessage.error({message:response.data.message,zIndex:20000});
            }
          })
          .catch(function (){ElMessage.error({message:"出现一些问题……",zIndex:20000});})
    }

  }
}
</script>

<style scoped>
#topline{
  position: relative;
  top:0;
}
#nav{
  position: relative;
}

#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);
  top:0px;
  width:100%;
  height: 100vh;
  text-align: center;
  z-index: 10;
}

#introduceWord{
  position: relative;
  margin: 0 auto;
  text-align: center;
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
  position: relative;
  top:300px;
  padding: 0;
  margin: 0;
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
  grid-template-rows: repeat(7, 1fr); /* 三列网格 */
  grid-gap: 3px; /* 网格之间的间距 */
  height: 500px;
  padding: 10px;
  border-top: 40px;
  overflow-y: scroll;
}

.card {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 15px;
  text-align: left;
  font-size: 16px;
  height: 100px;
  display: flex;
  border-radius: 10px;
}

.cardInfo{
  width: 450px;
}


#button1{
  position: absolute;
  right:50px;
  background-color: #ec1616;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#button2
{
  position: absolute;
  right:150px;
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.text {
  font-size: 14px;
}

.item {
  margin-bottom: 18px;
}

.box-card {
  width: 450px;
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
  position: relative;
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