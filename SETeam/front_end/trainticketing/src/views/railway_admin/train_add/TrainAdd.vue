<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="main">
        <div class="add-schedule">
            <h1>添加车次</h1>
            <el-steps :active="a" finish-status="success">
                <el-step title="填写基本信息" style="text-align: left"></el-step>
                <el-step title="选择站点" style="text-align: left"></el-step>
                <el-step title="选择车厢" style="text-align: left"></el-step>
                <el-step title="设置时间" style="text-align: left"></el-step>
            </el-steps>
            <div class="form-container">
                <form @submit.prevent="submitForm">
                    <div v-if="a === 0">
                        <form @submit.prevent="submitFormStep1">
                            <label for="scheduleNo"><b>车次编号：</b></label>
                            <input type="text" id="scheduleNo" v-model="schedule.scheduleNo" required>
                        </form>
                    </div>
                    <div v-if="a === 1">
                        <form @submit.prevent="submitFormStep2">
                            <label for="stationIds"><b>车站名：</b></label>
                            <div v-for="(fieldIndex, index) in stationFields" :key="index">
                                <div class="button-container">
                                    <select v-model="schedule.stationIds[fieldIndex]" id="select-box" style="width: 400px; padding: 10px">
                                        <option :value="station.id" v-for="station in stations" :key="station.id">{{ station.name }}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="button-container">
                                <input type="button" value="增加车站" @click="addStationField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                                <span class="button-spacing"></span>
                                <input type="button" value="删除车站" @click="deleteStationField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                            </div>
                        </form>
                    </div>
                    <div v-if="a === 2">
                        <form @submit.prevent="submitFormStep3">
                            <label for="carriageIds"><b>车厢编号：</b></label>
                            <div v-for="(fieldIndex, index) in carriageFields" :key="index">
                                <div class="button-container">
                                    <select v-model="schedule.carriageIds[fieldIndex]" id="select-box" style="width: 400px; padding: 10px">
                                        <option :value="carriage.id" v-for="carriage in carriages" :key="carriage.id">{{ carriage.name }}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="button-container">
                                <input type="button" value="增加车厢" @click="addCarriageField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                                <span class="button-spacing"></span>
                                <input type="button" value="删除车厢" @click="deleteCarriageField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                            </div>
                        </form>
                    </div>
                    <div v-if="a === 3">
                        <form @submit.prevent="submitFormStep4">
                            <label for="departureTime"><b>出发时间：</b></label>
                            <input type="datetime-local" id="departureTime" v-model="schedule.departureTime" required>

                            <label for="arrivalTimes"><b>到达时间：</b></label>
                            <div v-for="(arrivalTime, index) in schedule.arrivalTimes" :key="index">
                                <input type="datetime-local" v-model="schedule.arrivalTimes[index]" required>
                            </div>
                            <div class="button-container">
                                <input type="button" value="增加到达时间" @click="addArrivalTimeField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" />
                                <span class="button-spacing"></span>
                                <input type="button" value="删除到达时间" @click="deleteArrivalTimeField()" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>
                            </div>
                            <input type="button" value="添加车次" @click="addTrain" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
                        </form>
                    </div>
                    <el-button v-if="a!==0" style="margin-top: 12px" @click="last()" >上一步</el-button>
                    <el-button v-if="a!==3" style="margin-top: 12px" @click="next()" >下一步</el-button>
                    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
                </form>
            </div>
        </div>
    </div>
    <div class="footer">
        <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p >
    </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";
import axios from "axios";
import {ElMessage} from "element-plus";

export default {
    components: {railway_Navline, TopLine},
    computed: {
        user() {
            return this.$store.getters.getUser;
        },
        jwt(){
            return this.$store.getters.getJwt;
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
            a: 0,
            i:0,
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
        next(){
            this.a++;
            if (this.a > 3)
                this.a = 0;
        },
        last(){
            this.a--;
        },
        getMinTime(index) {
            if (index === 0) {
                // 第一个到达时间没有限制，返回一个空字符串
                return '';
            } else {
                // 获取前一个到达时间的值，作为当前时间的最小值
                const prevTime = this.schedule.arrivalTimes[index - 1];
                return this.incrementTime(prevTime);
            }
        },
        addArrivalTimeField(index) {
            this.schedule.arrivalTimes.splice(index + 1, 0, '');
            //const lastArrivalTime = this.schedule.arrivalTimes[this.schedule.arrivalTimes.length - 1];
            //const newTime = this.incrementTime(lastArrivalTime);
            //this.schedule.arrivalTimes.push(newTime);
        },
        incrementTime(time) {
            const currentTime = new Date(time);
            const incrementedTime = new Date(currentTime.getTime() + 60000); // Increment by 1 minute
            return incrementedTime.toISOString().slice(0, -8); // Format as datetime-local string
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
        addTrain() {
            if(this.user==="null"){
                ElMessage({message:"登录已过期，请重新登录",type:'warning'});
                this.$store.dispatch('logout');
                localStorage.setItem('username', null);
                this.$router.push('/');
                return;
            }
            /*if(this.schedule.scheduleNo==='') {
                alert("请填写车次编号");
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
            }*/
            if(this.schedule.arrivalTimes[0]!==this.schedule.departureTime){
                ElMessage({message:"请确保第一个到达时间与出发时间相同",type:'warning'});
                return;
            }
            if(this.stationFields.length!==this.schedule.arrivalTimes.length){
                ElMessage({message:"请保证站点数量与到达时间对应",type:'warning'});
                return;
            }
            for (let i = 1; i < this.schedule.arrivalTimes.length; i++) {
                const current = new Date(this.schedule.arrivalTimes[i]);
                const previous = new Date(this.schedule.arrivalTimes[i - 1]);
                if (current <= previous) {
                    ElMessage({ message: "请确保到达时间递增", type: 'warning' });
                    return;
                }
            }
            axios.post('api/schedules/',
                {
                    "schedule_no":this.schedule.scheduleNo,
                    "station_ids":this.schedule.stationIds,
                    "carriage_ids":this.schedule.carriageIds,
                    "departure_time":this.schedule.departureTime,
                    "arrival_times":this.schedule.arrivalTimes
                },{headers:{'jwt': `${this.jwt}`}})
                .then(function(response){
                    if(response.data.result!==0) {
                        ElMessage.error(response.data.message);
                    }
                    else {
                        ElMessage({message:response.data.message,type:'success'});
                    }

                })
          this.$router.push('/workspace');
        }
    }
}
</script>

<style scoped>
el-steps{
    margin: 0;
}
.main{
    width: 100%;
    height: 100vh;
    background-color:rgba(255,255,255,0.15);
}
.add-schedule {
    max-width: 450px;
    margin: 0px auto;
    padding: 20px;
//border: 1px solid #ccc;
//border-radius: 4px;
}

.form-container {
    max-height: 60vh; /* 设置适当的高度 */
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














