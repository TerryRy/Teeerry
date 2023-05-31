<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">
      <div id="introduceWord">
          <p>车次信息</p>
      </div>
      <div id="secondFloor">
<!--        <p v-if="schedules.length===0">很抱歉，没有可以改签的车次</p>-->
        <div class="schedule-list" style="margin: 0 auto; text-align: center;">
          <el-table :resize-sensor="false" :data="schedules" style="width: 100%" stripe="true" border="true">
            <el-table-column type="index"></el-table-column>
            <el-table-column label="车次" width="100px">
              <template v-slot="{ row }">
                {{row.schedule_no}}
              </template>
            </el-table-column>
            <el-table-column label="途径站点" width="300px">
              <template v-slot="{ row }">
                <div class="stationsInfo" v-for="station in row.stations" :key="station.id">
                  {{station.station.name}}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="出发时间" width="200px">
              <template v-slot="{ row }">
                {{row.departure_time}}
              </template>
            </el-table-column>
            <el-table-column label="座位类型" width="500px">
              <template v-slot="{ row }">
                <el-button @click="showdetails(row,carriage.carriage.id)" type="primary" style="margin: 10px" v-for="carriage in row.carriages" :key="carriage.carriage.id">{{carriage.carriage.name}}&nbsp;余{{carriage.rest_seats}}张</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
<!--          <div class="schedule_grid">-->
<!--              <div class="schedule" v-for="schedule in schedules" :key="schedule.id">-->
<!--                  <div class="scheduleInfo">-->
<!--                      <div class="trainInfo">-->
<!--              <div>车次：{{schedule.schedule_no}}&nbsp;&nbsp;-->
<!--                出发时间：{{schedule.departure_time}}&nbsp;&nbsp;-->
<!--                  途径站点：-->
<!--              <div class="stationsInfo" v-for="station in schedule.stations" :key="station.id">-->
<!--             {{station.station.name}}-->
<!--              </div>-->
<!--                  <span>座位类型：&nbsp;</span>-->
<!--                  <el-select v-model="seatType" id="select-box" style="width: 300px" placeholder="座位类型" @change="updateRestNum(schedule)">-->
<!--                      <el-option :value="carriage.carriage.id" v-for="carriage in schedule.carriages" :key="carriage.carriage.id"-->
<!--                                 :label="carriage.carriage.name">-->
<!--                              <div>{{ carriage.carriage.name }}-->
<!--                                  <template v-if="carriage.rest_seats != 0">-->
<!--                                  <span>剩余：{{ carriage.rest_seats }}</span>-->
<!--                          </template>-->
<!--                          <template v-else>-->
<!--                              <div>{{ carriage.carriage.name }}<span style="color: red;">剩余：0</span></div>-->
<!--                          </template>-->
<!--                              </div>-->
<!--&lt;!&ndash;                          <div v-if="carriage.rest_seats!=0">{{carriage.carriage.name}}&ndash;&gt;-->
<!--&lt;!&ndash;                              剩余：{{carriage.rest_seats}}&ndash;&gt;-->
<!--&lt;!&ndash;                          </div>&ndash;&gt;-->
<!--                      </el-option>-->
<!--                  </el-select>-->
<!--                  <br><br>-->
<!--                  <el-button id="button1" @click="showdetails(schedule,seatType)">购买</el-button>-->
<!--&lt;!&ndash;                  <button id="button1" @click="showdetails(schedule,0)">商务座<span>&ndash;&gt;-->
<!--&lt;!&ndash;                      <div v-for="carriage in schedule.carriage" :key="carriage.id">&ndash;&gt;-->
<!--&lt;!&ndash;                          <div v-if="carriage.carriage.id==0">&ndash;&gt;-->
<!--&lt;!&ndash;                              {{carriage.carriage.rest_seats}}&ndash;&gt;-->
<!--&lt;!&ndash;                          </div>&ndash;&gt;-->
<!--&lt;!&ndash;                      </div>&ndash;&gt;-->
<!--&lt;!&ndash;                  </span>&ndash;&gt;-->

<!--&lt;!&ndash;                  </button>&ndash;&gt;-->
<!--&lt;!&ndash;                  <button id="button2" @click="showdetails(schedule,1)">一等座<span>&ndash;&gt;-->
<!--&lt;!&ndash;                      <div v-for="carriage in schedule.carriage" :key="carriage.id">&ndash;&gt;-->
<!--&lt;!&ndash;                          <div v-if="carriage.carriage.id==1">&ndash;&gt;-->
<!--&lt;!&ndash;                              {{carriage.carriage.rest_seats}}&ndash;&gt;-->
<!--&lt;!&ndash;                          </div>&ndash;&gt;-->
<!--&lt;!&ndash;                      </div>&ndash;&gt;-->
<!--&lt;!&ndash;                  </span>&ndash;&gt;-->
<!--&lt;!&ndash;                  </button>&ndash;&gt;-->
<!--&lt;!&ndash;                  <button id="button3" @click="showdetails(schedule,2)">二等座<span>&ndash;&gt;-->
<!--&lt;!&ndash;                      <div v-for="carriage in schedule.carriage" :key="carriage.id">&ndash;&gt;-->
<!--&lt;!&ndash;                          <div v-if="carriage.carriage.id==2">&ndash;&gt;-->
<!--&lt;!&ndash;                              {{carriage.carriage.rest_seats}}&ndash;&gt;-->
<!--&lt;!&ndash;                          </div>&ndash;&gt;-->
<!--&lt;!&ndash;                      </div>&ndash;&gt;-->
<!--&lt;!&ndash;                  </span>&ndash;&gt;-->
<!--&lt;!&ndash;                  </button>&ndash;&gt;-->
<!--              </div>-->
<!--                      </div>-->
<!--                  </div>-->

<!--              </div>-->
<!--          </div>-->
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
import {ElMessage} from "element-plus";

export default {
  name: "QueryTrain",
  components: {NavLine, TopLine},
    data(){
        return{
            // departTime: null,
            // departure: null,
            // destination: null,
            schedules:[],
            seatType: null,
            restNum: 0
        }
    },
    computed:{
        departTime() {
            return this.$store.getters.getDepartTime;
        },
        departure() {
            return this.$store.getters.getDeparture;
        },
        destination() {
            return this.$store.getters.getDestination;
        },
      jwt(){
        return this.$store.getters.getJwt;
      },
      isnotlogin(){
        return this.jwt==="null"||this.jwt===null;
      }
    },
    mounted() {
        const username = localStorage.getItem('username');
        if (username) {
            this.$store.commit('setUser', username);
        }
        const departTime = localStorage.getItem('departTime');
        if (departTime) {
            this.$store.commit('setDepartTime', departTime);
        }
        const departure = localStorage.getItem('departure');
        if (departure) {
            this.$store.commit('setDeparture', departure);
        }
        const destination = localStorage.getItem('destination');
        if (username) {
            this.$store.commit('setDestination', destination);
        }
        // let dateTime_first=new Date(this.departTime);
        // let dateTime_next=new Date();
        // dateTime_next=dateTime_next.setDate(dateTime_first.getDate()+1);
        // dateTime_next=new Date(dateTime_next);
      let dateTime_first = new Date(this.departTime);
      let dateTime_next = new Date(dateTime_first);
      dateTime_next.setDate(dateTime_first.getDate() + 1);

      axios.get('/api/schedules/',
            {
                params: {
                    "after": this.departTime,
                    "before": dateTime_next,
                    "ori": this.departure,
                    "dst": this.destination,
                },
                headers:{'jwt':`${this.jwt}`}
            }
        )
            .then((response)=>{
                this.schedules=response.data.schedules;
            })
            .catch(function(){alert("不存在这样的车次！")})

    },
    methods:{
        toDisplayString,
        updateRestNum(schedule){
            // console.log("yes");
            const carriage = schedule.carriages.find(c => c.carriage.id === this.seatType);
            if (carriage) {
                // alert("yes");
                this.restNum = carriage.rest_seats;
            }
        },
        showdetails(schedule,seatType)
        {
          if(this.isnotlogin)
          {
            ElMessage({message:"请先登录",type:'warning'});
            return;
          }
          this.$store.dispatch('storeSchedule', schedule);
            // alert(schedule.schedule_no);
            localStorage.setItem('schedule', schedule);
            // alert(seatType);
            this.$store.dispatch('storeSeatType', seatType);
            localStorage.setItem('seatType', seatType);
            // if(this.seatType==null)
            // {
            //     ElMessage.error("请选择座位类型！");
            //     return;
            // }
            // if(this.restNum==0)
            // {
            //     ElMessage.error("该类型座位车票已售空，请重新选择！");
            //     return;
            // }
            this.$router.push('/ticketbuy');
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
  background-color: rgba(255, 255, 255, 0.8);;
  width:100%;
  text-align: center;
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
    top:50px;
    padding: 0;
    margin: 0 auto;
    display: flex;
}


.schedule_grid {
    position: relative;
    top:50px;
    width:1200px;
    margin: 0 auto;
    display: grid;
    grid-template-rows: repeat(7, 3fr);
    grid-gap: 3px; /* 网格之间的间距 */
    max-height: 500px;
    padding: 10px;
    border-top: 40px;
    overflow-y: scroll;
    line-height: 35px;
}

.schedule {
    background-color: rgba(214, 232, 239, 0.45);
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
    font-size: 20px;
}

.stationsInfo{
    display: inline-block;
    margin-right: 10px;
}

#button1{
    display: inline-block;
    position: absolute;
    right:80px;
    background-color: #628ede;
    color: #ffffff;
    padding: 10px 10px;
    border: none;
    border-radius: 4px;
    font-size: 16px;
    top: 50px;
    width:300px;
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