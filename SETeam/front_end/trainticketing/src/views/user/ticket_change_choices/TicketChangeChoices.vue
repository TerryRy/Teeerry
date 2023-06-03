<template>
  <el-backtop :right="100" :bottom="100" />
    <div id="topline"><TopLine/></div>
    <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
    <div id="mainBlock">
        <div id="introduceWord">
            <p>可改签订单</p>
        </div>
        <div id="secondFloor">
                <p v-if="schedules.length===0">很抱歉，没有可以改签的车次</p>
          <div class="schedule-list" style="margin: 0 auto; text-align: center;">
            <el-table :data="schedules" style="width: 100%" stripe="true" border="true">
              <el-table-column label="车次" width="200px">
                <template v-slot="{ row }">
                  {{row.schedule_no}}
                </template>
              </el-table-column>
              <el-table-column label="出发时间" width="200px">
                <template v-slot="{ row }">
                  {{row.departure_time}}
                </template>
              </el-table-column>
              <el-table-column label="座位类型" width="500px">
                <template v-slot="{ row }">
                  <el-button @click="ticketchange(billid,row,carriage)" type="primary" style="margin: 10px" v-for="carriage in row.carriages" :key="carriage.carriage.id">{{carriage.carriage.name}}&nbsp;余{{carriage.rest_seats}}张</el-button>
                </template>
              </el-table-column>
            </el-table>
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
    name: "TicketChangeChoices",
    components: {NavLine, TopLine},
    computed:{
        jwt(){
          return this.$store.getters.getJwt;
        },
        billid(){
          return this.$store.getters.getTicketID;
        }
    },
    mounted() {
      const jwt = localStorage.getItem('jwt');
      if(jwt){
        this.$store.commit('setJwt', jwt);
      }
      const billID = localStorage.getItem('ticketID');
      if(billID){
        this.$store.commit('setTicketID', billID);
      }
      axios.get('/api/schedules/',
          {
            params: {
              "change":this.billid
            },
            headers:{'jwt':`${this.jwt}`}
          }
          )
          .then((response)=>{
            this.schedules=response.data.schedules;
          })
          .catch(function(){alert("不存在这样的车次！")})
    },
    data() {
        return {
            schedules: []
        }
    },
    methods:{
        // changeTicket(billid)
        // {
        //     let confirmPurchase = confirm("是否确认购买？");
        //     if (confirmPurchase) {
        //         this.$store.dispatch('storeBill', bill);
        //         localStorage.setItem('bill', bill);
        //         this.$router.push('/orderdetails');
        //     } else {
        //         this.$router.push('/orderdetails');
        //     }
        // },
      ticketchange(billid,row,carriage)
      {
        axios.put(`/api/tickets/${billid}`,
            {"new_schedule_id": row.id,
                  "carriage_id": carriage.carriage.id},{headers:{'jwt':`${this.jwt}`}})
            .then((response)=>
            {
              if(response.data.result===0)
              {
                ElMessage({message:response.data.message,type:'success'});
                this.$router.push('/orderlist');
              }
              else ElMessage.error(response.data.message);
            })
            .catch(function (){
              ElMessage.error("出现一些问题……");
            })
      }
    }
}


</script>

<style scoped>
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
    top: 70px;
}

#secondFloor{
    position: relative;
    top:50px;
    padding: 0;
    margin: 0;
    display: flex;
}
.schedule_grid div {
    background-color: lightcyan;
}
.schedule_grid {
    position: absolute;
    top:50px;
    left:200px;
    width:1000px;
    display: grid;
    grid-template-rows: repeat(7, 1fr);
    grid-gap: 3px; /* 网格之间的间距 */
    height: 550px;
    padding: 10px;
    border-top: 40px;
    overflow-y: scroll;
}

.schedule {
    background-color: rgba(112, 196, 232, 0.45);
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

.trainInfo{
    text-align: left;
    display: inline-block;
}

#choose_grid{
    display: inline-block;
    position: absolute;
    right:50px;
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