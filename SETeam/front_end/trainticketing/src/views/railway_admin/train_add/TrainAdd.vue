<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="add-schedule">
        <h1>添加车次</h1>
        <div class="form-container">
            <form @submit.prevent="submitForm">
                <label for="scheduleNo">车次编号：</label>
                <input type="text" id="scheduleNo" v-model="scheduleNo" required>

                <label for="stationIds">车站编号：</label>
                <input type="text" id="stationIds" v-model="stationIds" required>

                <label for="carriageIds">车厢编号：</label>
                <input type="text" id="carriageIds" v-model="carriageIds" required>

                <label for="departureTime">出发时间：</label>
                <input type="datetime-local" id="departureTime" v-model="departureTime" required>

                <label for="arrivalTimes">到达时间：</label>
                <div v-for="(arrivalTime, index) in arrivalTimes" :key="index">
                    <input type="datetime-local" v-model="arrivalTimes[index]" required>
                </div>

                <div class="button-container">
                    <button type="button" @click="addArrivalTimeField()">增加到达时间</button>
                </div>

                <button type="submit">添加车次</button>
            </form>
        </div>
    </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";

export default {
    components: {railway_Navline, TopLine},
    data() {
        return {
            scheduleNo: '',
            stationIds: '',
            carriageIds: '',
            departureTime: '',
            arrivalTimes: [''],
        };
    },
    methods: {
        submitForm() {
            /*const newSchedule = {
                schedule_no: this.scheduleNo,
                station_ids: this.stationIds.split(',').map(id => parseInt(id.trim())),
                carriage_ids: this.carriageIds.split(',').map(id => parseInt(id.trim())),
                departure_time: this.departureTime,
                arrival_times: this.arrivalTimes,
            };*/

            // Perform API request to add the schedule using newSchedule object

            // Reset form fields after successful submission
            this.scheduleNo = '';
            this.stationIds = '';
            this.carriageIds = '';
            this.departureTime = '';
            this.arrivalTimes = [''];
        },
        addArrivalTimeField(index) {
            this.arrivalTimes.splice(index + 1, 0, '');
        }
    }
}
</script>

<style scoped>
.add-schedule {
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

label {
    display: block;
    margin-bottom: 20px;
}

input[type="text"],
input[type="datetime-local"] {
    width: 100%;
    padding: 20px;
    font-size: 16px;
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
</style>














