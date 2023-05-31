<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToWorkspace="turnToWorkspace" @turnToTrainAdd="turnToTrainAdd" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
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
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";
import axios from "axios";
import depositMoney from "@/views/user/deposit_money/DepositMoney.vue";
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
                            alert("删除成功!");
                            break;
                        default:
                            alert("出现一些问题……");
                    }
                    this.$router.go(0);
                })
                .catch(function () {
                    alert("网络错误");
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
    max-width: 800px;
    margin: 0 auto;
    padding: 50px;
}

.schedule-list {
    max-height: 400px;
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
</style>