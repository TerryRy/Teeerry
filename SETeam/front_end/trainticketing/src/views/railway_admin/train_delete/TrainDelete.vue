<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToWorkspace="turnToWorkspace" @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="main">
    <div class="container">
        <h1>删减车次</h1>
        <div class="schedule-details">
            <p>你确定要删除吗？</p>

            <div class="schedule-info">
                <div>
                    <strong>车次编号：</strong> {{ scheduleId }}
                </div>
                <div>
                    <strong>车次名：</strong> {{ schedule.schedule_no }}
                </div>
                <div>
                    <strong>站点名：</strong>
                    <ul>
                        <li v-for="stationId in schedule.station_ids" :key="stationId">{{ stationId }}</li>
                    </ul>
                </div>
                <div>
                    <strong>车厢编号：</strong>
                    <ul>
                        <li v-for="carriageId in schedule.carriage_ids" :key="carriageId">{{ carriageId }}</li>
                    </ul>
                </div>
                <div>
                    <strong>出发时间：</strong> {{ schedule.departure_time }}
                </div>
                <div>
                    <strong>到达时间：</strong>
                    <ul>
                        <li v-for="arrivalTime in schedule.arrival_times" :key="arrivalTime">{{ arrivalTime }}</li>
                    </ul>
                </div>
            </div>
        </div>

        <button class="delete-button" @click="deleteSchedule">删除车次</button>
    </div>
    </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";

export default {
    components: {railway_Navline, TopLine},
    data() {
        return {
            scheduleId: 1, // 替换为实际的 schedule ID
            schedule: {
                schedule_no: 'S123Test',
                station_ids: [1, 4, 3, 2],
                carriage_ids: [1],
                departure_time: '2023-05-04 00:00:00',
                arrival_times: ['2023-05-04 00:00:00', '2023-05-04 00:00:00', '2023-05-04 00:00:00', '2023-05-04 00:00:00']
            }
        };
    },
    methods: {
        deleteSchedule() {
            // Make API request to delete the schedule using this.scheduleId
            // You can use axios or any other library for making HTTP requests
            console.log(`Deleting schedule with ID: ${this.scheduleId}`);
            console.log('Schedule:', this.schedule);
        }
    }
};
</script>

<style>
.main{
    width: 100%;
    height: 100vh;
    background-color:rgba(255,255,255,0.15);
}
.container {
    max-width: 400px;
    margin: 0 auto;
    padding: 50px;
}

h1 {
    margin-bottom: 20px;
}

.schedule-details {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 20px;
}

.schedule-info {
    margin-bottom: 10px;
}

strong {
    display: inline-block;
    margin-top: 10px;
}

ul {
    margin: 0;
    padding: 0;
    list-style-type: none;
    margin-top: 10px;
}

li {
    margin-bottom: 5px;
}

.delete-button {
    padding: 10px 20px;
    background-color: #ff4d4d;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.delete-button:hover {
    background-color: #ff3333;
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
