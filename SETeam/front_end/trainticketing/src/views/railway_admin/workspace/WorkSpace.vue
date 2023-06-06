<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToWorkspace="turnToWorkspace" @turnToTrainAdd="turnToTrainAdd" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="main">
        <div class="container">
            <h2>列车时刻表</h2>
            <div class="schedule-list">
                <el-table :data="schedules" style="width: 100%">
                    <el-table-column prop="schedule_no" label="车次编号"></el-table-column>
                    <el-table-column prop="departure_time" label="出发时间"></el-table-column>
                    <el-table-column label="站点信息">
                        <template v-slot="{ row }">
                            <ul>
                                <li v-for="station in row.stations" :key="station.station.id">
                                    <span>{{ station.station.station_no }}</span>
                                    <span>{{ station.station.name }}</span>
                                </li>
                            </ul>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作">
                        <template v-slot="{ row }">
                            <el-button @click="deleteTrain(row.id)" type="text" class="red">删除车次</el-button>
                            <el-button @click="changeTrain(row.id)" type="text" class="green">调整车次</el-button>
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
import railway_Navline from "@/components/common/railway_Navline.vue";
import axios from "axios";
import depositMoney from "@/views/user/deposit_money/DepositMoney.vue";
import {ElMessage} from "element-plus";
export default {
    name: "WorkSpace",
    components: {railway_Navline, TopLine},
    data() {
        return {
            schedules:[]
        }
    },
    mounted(){
        const jwt = localStorage.getItem('jwt');
        if(jwt){
            this.$store.commit('setJwt', jwt);
        }
        axios.get('api/schedules/',
            {
                headers:{'jwt': `${this.jwt}`}
            })
            .then((response)=>
            {
                this.schedules=response.data.schedules;
            })
    },
    computed: {
        depositMoney() {
            return depositMoney
        },
        user() {
            return this.$store.getters.getUser;
        },
        jwt(){
            return this.$store.getters.getJwt;
        }
    },
    methods :{
        deleteTrain(id) {
            axios.delete(`/api/schedules/${id}`,{headers:{'jwt': `${this.jwt}`}})
                .then((response)=>
                {
                    switch (response.data.result)
                    {
                        case 0:
                            ElMessage({message:response.data.message,type:'success'});
                            break;
                        default:
                            ElMessage({message:"出现一些问题……，请重试！",type:'warning'});
                    }
                    this.$router.go(0);
                })
                .catch(function () {
                    ElMessage({message:"删除成功，请刷新！！",type:'success'});
                })
        },
        changeTrain(schedule_id){
            this.$store.dispatch('storeSchedule_id', schedule_id);
            localStorage.setItem('schedule_id', schedule_id);
            this.$router.push('/trainchange')
        }
    }
};
</script>

<style scoped>
.container {
    height: calc(100vh - 150px);
    max-width: 800px;
    margin: 0 auto;
    padding: 50px;
}
.main{
    width: 100%;
    height: 100vh;
    background-color:rgba(255,255,255,0.15);
}
.schedule-list {
    margin: 0px auto;
    max-height: calc(100vh - 200px);
    overflow-y: scroll;
    scrollbar-width: thin;
    scrollbar-color: #888888 #f1f1f1;
}

.schedule-item {
    margin-bottom: 20px;
}

.stations ul,
.carriages ul {
    list-style: none;
    padding: 0;
}

.stations li,
.carriages li {
    margin-bottom: 10px;
}

.green {
    background-color: green;
    color: white;
}

.red {
    background-color: red;
    color: white;
}

.carriages span {
    margin-right: 10px;
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
