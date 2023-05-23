<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="container">
        <h2>列车时刻表</h2>
        <div class="schedule-list">
            <div v-for="schedule in schedules" :key="schedule.id" class="schedule-item">
                <h3>{{ schedule.schedule_no }}</h3>
                <p>出发时间: {{ schedule.departure_time }}</p>
                <div class="stations">
                    <h4>站点信息:</h4>
                    <ul>
                        <li v-for="station in schedule.stations" :key="station.id">
                            <span>{{ station.station_no }}</span>
                            <span>{{ station.name }}</span>
                        </li>
                    </ul>
                </div>
                <div class="carriages">
                    <h4>车厢信息:</h4>
                    <ul>
                        <li v-for="carriage in schedule.carriage" :key="carriage.carriage.id">
                            <span>{{ carriage.carriage.name }}</span>
                            <span>座位数: {{ carriage.carriage.seat_num }}</span>
                            <span>数量: {{ carriage.num }}</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";
export default {
    setup() {
        const schedules = ref([]);

        // 假设通过接口获取到的时刻表数据为response
        const response = {
            schedules: [
                {
                    id: 1,
                    schedule_no: "K1234",
                    departure_time: "2023-5-4-11:11:00",
                    stations: [
                        {
                            id: 1,
                            station_no: "S534",
                            name: "beijing"
                        },
                        {
                            id: 2,
                            station_no: "S764",
                            name: "shanghai"
                        },
                        {
                            id: 1,
                            station_no: "S534",
                            name: "beijing"
                        },
                        {
                            id: 1,
                            station_no: "S534",
                            name: "beijing"
                        },
                        {
                            id: 1,
                            station_no: "S534",
                            name: "beijing"
                        },
                        {
                            id: 1,
                            station_no: "S534",
                            name: "beijing"
                        },

                    ],
                    carriage: [
                        {
                            carriage: {
                                id: 1,
                                name: "C1233",
                                seat_num: 120
                            },
                            num: 5
                        },
                        {
                            carriage: {
                                id: 2,
                                name: "C1243",
                                seat_num: 30
                            },
                            num: 2
                        }
                    ]
                },
            ]
        };

        // 在mounted钩子中将response中的数据赋值给schedules
        const mounted = () => {
            schedules.value = response.schedules;
        };

        return {
            schedules,
            mounted
        };
    },
    mounted() {
        this.mounted();
    },
    name: "WorkSpace",
    components: {railway_Navline, TopLine}
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

.carriages span {
    margin-right: 10px;
}
</style>