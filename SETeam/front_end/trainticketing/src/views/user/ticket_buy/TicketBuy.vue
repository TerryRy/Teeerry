<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
    <div id="mainBlock">
        <div id="introduceWord">
            <p>购买车票</p>
        </div>
        <div id="ticketInfo">
            <form id="register-form">
                <table>
                    <tbody>
                    <tr>
                        <th class="vertical-header">乘车人</th>
                        <td>
<!--                            <select v-model="contact" id="select-box" style="width: 300px">-->
<!--                                <option :value="contact.id" v-for="contact in contacts" :key="contact.id">{{contact.name}}</option>-->
<!--                            </select>-->
                            <el-select v-model="contactID" id="select-box" style="width: 300px" placeholder="联系人">
                                <el-option :value="contact.id" v-for="contact in contacts" :key="contact.id" :label="contact.name">
                                    {{contact.name}}
                                </el-option>
                            </el-select>
                        </td>
                    </tr>
                    <tr>
                        <th class="vertical-header">乘坐车次</th>
                        <td>{{schedule.schedule_no}}</td>
                    </tr>
                    <tr>
                        <th class="vertical-header">出发车站</th>
                        <td>
                            <div v-for="station in stations" :key="station.id">
                                <div v-if="station.id==departure">
                                    {{station.name}}
                                </div>
                            </div>
                            </td>
                    </tr>
                    <tr>
                        <th class="vertical-header">到达车站</th>
                    <td>
                        <div v-for="station in stations" :key="station.id">
                            <div v-if="station.id==destination">{{station.name}}</div>
                        </div>
                    </td>
                    </tr>
                    <tr>
                        <th class="vertical-header">座位类型</th>
                        <td>
                            <div v-for="carriage in schedule.carriages" :key="carriage.carriage.id">
                                <div v-if="carriage.carriage.id==seatType">
                                    {{carriage.carriage.name}}
                                </div>
                            </div>
<!--                            <div v-if="seatType==0">商务座</div>-->
<!--                            <div v-if="seatType==1">一等座</div>-->
<!--                            <div v-if="seatType==2">二等座</div>-->
                        </td>
                    </tr>
                    <tr>
                        <th class="vertical-header">价格</th>
                        <td>
                            <div v-for="carriage in schedule.carriages" :key="carriage.carriage.id">
                                <div v-if="carriage.carriage.id==seatType">
                                    {{carriage.price}}
                                </div>
                            </div>
                            </td>
                    </tr>
                    </tbody>
                </table>
                <div id="buttons">
                    <input type="button" value="确认购买" @click="confirmPurchase" style="margin-right:10px; background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 20px; cursor: pointer;"/>&nbsp;&nbsp;
                    <input type="button" value="返回" @click="turnToQueryTrain" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 20px; cursor: pointer;"/>
                </div>
            </form>
        </div>
      <div class="footer">
        <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
      </div>
    </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import axios from "axios";
import {ElMessage, ElMessageBox} from "element-plus";


export default {
    name: "TicketBuy",
    components: {NavLine, TopLine},
    data(){
        return{
            contacts:[],
            stations:[],
            contactID:null

        }
    },
    mounted() {
        const jwt = localStorage.getItem('jwt');
        if(jwt){
            this.$store.commit('setJwt', jwt);
        }
        axios.get('api/schedules/stations',
            {
                headers:{'jwt': `${this.jwt}`}
            })
            .then((response)=>
            {
                this.stations=response.data.stations;
            })
            .catch(function(){ElMessage.error("站点错误！")})
        axios.get('api/contacts/',
            {
                headers:{'jwt': `${this.jwt}`}
            })
            .then((response)=>
            {
                this.contacts=response.data.contacts;
            })
            .catch(function(){ElMessage.error("网络异常，请稍后重试！")})
    },
    computed:{
        departure() {
            return this.$store.getters.getDeparture;
        },
        destination() {
            return this.$store.getters.getDestination;
        },
        seatType(){
            return this.$store.getters.getSeatType;
        },
        schedule(){
            return this.$store.getters.getSchedule;
        },
        jwt(){
          return this.$store.getters.getJwt;
        }
    },

    methods:{
        confirmPurchase()
        {
            if(this.contactID==null)
            {
                ElMessageBox.alert("请选择联系人！");
                return;
            }
            axios.post('/api/tickets/',
                {
                    "schedule_id": this.schedule.id,
                    "contact_id": this.contactID,
                    "carriage_id": this.seatType,
                    "ori_station_id": this.departure,
                    "dst_station_id": this.destination
                },
          {headers:{'jwt':`${this.jwt}`}
            })
                .then((response)=>
                {
                    if(response.data.result===0)
                    {
                      this.$store.dispatch('storeTicketID', response.data.ticket_id);
                      localStorage.setItem('ticketID', response.data.ticket_id);
                      ElMessage({message:response.data.message,type:'success'});
                      this.$router.push('/orderlist');
                    }
                    else{
                      ElMessage({message:response.data.message,type:'error'});
                    }

                })
                .catch(function(){ElMessage.error("购买失败，请重试！")});

        },
        turnToQueryTrain()
        {
            this.$router.push('/querytrain');
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
    top:50px;
    width:100%;
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
    font-size: 40px;
    font-weight: bold;
    font-family: 华光行书_CNKI, serif;
}

#ticketInfo{
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
    padding: 15px;
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

tr {
    font-size: 20px;
}

#buttons{
    position: relative;
    align-items:center;
    width: 100%;
    top:40px;
}

#select-box {
    position:relative;
    padding: 5px;
    font-size: 20px;
    align-items: center;
    width: 515px;
    border: none;
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