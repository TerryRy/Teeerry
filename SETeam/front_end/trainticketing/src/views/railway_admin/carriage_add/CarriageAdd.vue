<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="add-carriage">
        <h1>添加车厢</h1>
        <form @submit.prevent="submitForm">
            <label for="name">车厢名：</label>
            <input type="text" id="name" v-model="carriage.name" required>

            <label for="seatNum">座位数量：</label>
            <input type="number" id="seatNum" v-model="carriage.seatNum" required>

            <label for="increase_rate">席位加价率：</label>
            <input type="number" id="increase_rate" v-model="carriage.increase_rate" required>

            <button type="submit">添加车厢</button>
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
            carriage: {
                name: '',
                seatNum: null,
                increase_rate : null
            }
        };
    },
    methods: {
        /*submitForm() {
            const requestBody = {
                name: this.carriage.name,
                seat_num: this.carriage.seatNum,
                increase_rate:this.carriage.increase_rate
            };*/

            // Perform API request to add the carriage using the requestBody object
            // You can use axios or any other library for making HTTP requests

            // Reset form fields after successful submission
            //this.carriage.name = '';
            //this.carriage.seatNum = null;
            //this.carriage.increase_rate = null;
        //}
    }
}
</script>

<style scoped>
.add-carriage {
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

input[type="text"],
input[type="number"] {
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
