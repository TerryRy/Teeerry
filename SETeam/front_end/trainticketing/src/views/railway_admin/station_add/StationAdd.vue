<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="add-station">
        <h1>添加站点</h1>
        <form @submit.prevent="submitForm">
            <label for="stationNo">站点编号：</label>
            <input type="text" id="stationNo" v-model="station.stationNo" required>

            <label for="name">站点名：</label>
            <input type="text" id="name" v-model="station.name" required>

            <button type="submit">添加站点</button>
        </form>
    </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";

export default {
    components: {railway_Navline, TopLine},
    data() {
        return {
            station: {
                stationNo: '',
                name: ''
            }
        };
    },
    methods: {
        submitForm() {
            /*const requestBody = {
                station_no: this.station.stationNo,
                name: this.station.name
            };*/

            // Perform API request to add the station using the requestBody object
            // You can use axios or any other library for making HTTP requests

            // Reset form fields after successful submission
            this.station.stationNo = '';
            this.station.name = '';
        }
    }
}
</script>

<style scoped>
.add-station {
    max-width: 400px;
    margin: 150px auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

label {
    display: block;
    margin-bottom: 10px;
}

input[type="text"] {
    width: 100%;
    padding: 5px;
    font-size: 16px;
    border-radius: 4px;
    border: 1px solid #ccc;
    box-sizing: border-box;
    margin-bottom: 10px;
}

button {
    padding: 10px 20px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>
