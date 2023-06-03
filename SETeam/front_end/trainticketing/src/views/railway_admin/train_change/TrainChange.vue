<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="add-schedule">
        <h1>调整车次</h1>
        <div class="form-container">
            <form @submit.prevent="submitForm">
                <label for="scheduleNo">车次编号：</label>
                {{schedule_id}}
                <br><br>

                <label for="makesure">请确认是否调整 如不修改请点击返回</label>
                <div class="button-container">
                    <a href="/workspace"><input type="button" value="返回" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/></a>
                </div>

                <label for="stationIds">车站编号：</label>
                <div v-for="(fieldIndex, index) in stationFields" :key="index">
                    <div class="button-container">
                        <select v-model="schedule.stationIds[fieldIndex]" id="select-box" style="width: 320px; padding: 10px">
                            <option :value="station.id" v-for="station in stations" :key="station.id">{{ station.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="button-container">
                    <input type="button" value="增加车站" @click="addStationField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                    <span class="button-spacing"></span>
                    <input type="button" value="删除车站" @click="deleteStationField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                </div>

                <label for="carriageIds">车厢编号：</label>
                <div v-for="(fieldIndex, index) in carriageFields" :key="index">
                    <div class="button-container">
                        <select v-model="schedule.carriageIds[fieldIndex]" id="select-box" style="width: 320px; padding: 10px">
                            <option :value="carriage.id" v-for="carriage in carriages" :key="carriage.id">{{ carriage.name }}</option>
                        </select>
                    </div>
                </div>
                <div class="button-container">
                    <input type="button" value="增加车厢" @click="addCarriageField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                    <span class="button-spacing"></span>
                    <input type="button" value="删除车厢" @click="deleteCarriageField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                </div>

                <label for="departureTime">出发时间：</label>
                <input type="datetime-local" id="departureTime" v-model="schedule.departureTime" required>

                <label for="arrivalTimes">到达时间：</label>
                <div v-for="(arrivalTime, index) in schedule.arrivalTimes" :key="index">
                    <input type="datetime-local" v-model="schedule.arrivalTimes[index]" required>
                </div>

                <div class="button-container">
                    <input type="button" value="增加到达时间" @click="addArrivalTimeField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" />
                    <span class="button-spacing"></span>
                    <input type="button" value="删除到达时间" @click="deleteArrivalTimeField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                </div>

                <input type="button" value="修改车次" @click="changeTrain" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
                <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            </form>
        </div>
    </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";
import axios from "axios";

export default {
    components: {railway_Navline, TopLine},
    computed: {
        user() {
            return this.$store.getters.getUser;
        },
        jwt(){
            return this.$store.getters.getJwt;
        },
        schedule_id(){
            return this.$store.getters.getSchedule_id;
        }
    },
    data() {
        return {
            schedule: {
                scheduleNo: '',
                stationIds: [''],
                carriageIds: [''],
                departureTime: '',
                arrivalTimes: [''],
            },
            stationFields: [0],
            carriageFields:[0],
            stations:[],
            carriages:[],
        };
    },
    mounted() {
        const username = localStorage.getItem('username');
        if (username) {
            this.$store.commit('setUser', username);
        }
        const jwt = localStorage.getItem('jwt');
        if(jwt){
            this.$store.commit('setJwt', jwt);
        }
        const schedule_id = localStorage.getItem('schedule_id');
        if(schedule_id){
            this.$store.commit('setSchedule_id',schedule_id);
        }
        axios.get('api/schedules/stations',
            {
                headers:{'jwt': `${this.jwt}`}
            })
            .then((response)=>
            {
                this.stations=response.data.stations;
            })
        axios.get('api/schedules/carriages',
            {
                headers:{'jwt': `${this.jwt}`}
            })
            .then((response)=>
            {
                this.carriages=response.data.carriages;
            })
    },
    methods: {
        addArrivalTimeField(index) {
            this.schedule.arrivalTimes.splice(index + 1, 0, '');
        },
        deleteArrivalTimeField(index) {
            this.schedule.arrivalTimes.splice(index , 1);
        },
        addStationField() {
            const lastIndex = this.stationFields[this.stationFields.length - 1];
            this.stationFields.push(lastIndex + 1);
            this.schedule.stationIds.push('');
        },
        deleteStationField() {
            this.stationFields.splice(this.stationFields.length - 1, 1);
            this.schedule.stationIds.splice(this.schedule.stationIds.length - 1, 1);
        },
        addCarriageField() {
            const lastIndex = this.carriageFields[this.carriageFields.length - 1];
            this.carriageFields.push(lastIndex + 1);
            this.schedule.carriageIds.push('');
        },
        deleteCarriageField() {
            this.carriageFields.splice(this.carriageFields.length - 1, 1);
            this.schedule.carriageIds.splice(this.schedule.carriageIds.length - 1, 1);
        },
        changeTrain() {
            if(this.user==="null"){
                alert("登录已过期，请重新登录");
                this.$store.dispatch('logout');
                localStorage.setItem('username', null);
                this.$router.push('/');
                return;
            }
            if(this.schedule.stationIds===null) {
                alert("请填写车站编号");
            }
            if(this.schedule.carriageIds===null) {
                alert("请填写车厢编号");
            }
            if(this.schedule.departureTime===null) {
                alert("请填写出发时间");
            }
            if(this.schedule.arrivalTimes===null) {
                alert("请填写到达时间");
            }
            if(this.schedule.arrivalTimes[0]!==this.schedule.departureTime) {
                alert("请确保第一个到达时间与出发时间相同");
            }
            if(this.stationFields.length!==this.schedule.arrivalTimes.length){
                alert("请保证站点数量与到达时间对应");
            }
            axios.put(`api/schedules/${this.schedule_id}`,
                {
                    "schedule_no":this.schedule.scheduleNo,
                    "station_ids":this.schedule.stationIds,
                    "carriage_ids":this.schedule.carriageIds,
                    "departure_time":this.schedule.departureTime,
                    "arrival_times":this.schedule.arrivalTimes
                },{headers:{'jwt': `${this.jwt}`}})
                .then(function(response){
                    if(response.data.result!==0) {
                        alert(response.data.message);
                    }
                    else {
                        alert("修改成功！");
                    }
                })
                .catch(function(){
                    alert("网络错误，请稍后重试。");
                })
        }
    }
}
</script>

<style scoped>
.add-schedule {
  height: calc(100vh - 150px);
    max-width: 350px;
    margin: 150px auto;
    padding: 40px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

.form-container {
    max-height: 350px; /* 设置适当的高度 */
    overflow-y: auto;
}

.green {
    background-color: white;
    color: green;
}


label {
    display: block;
    margin-bottom: 20px;
}

input[type="text"],
input[type="datetime-local"] {
    width: 90%;
    padding: 10px;
    font-size: 14px;
    border-radius: 4px;
    border: 1px solid #ccc;
    box-sizing: border-box;
    margin-bottom: 10px;
}

.button-container {
    margin-bottom: 20px;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 5px;
}



.button-spacing {
    margin-left: 10px;
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









