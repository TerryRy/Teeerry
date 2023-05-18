<template>
    <div class="container">
        <h1>Modify Schedule</h1>
        <div class="scrollable">
            <form @submit.prevent="updateSchedule">
                <label for="scheduleNo">Schedule No:</label>
                <input type="text" id="scheduleNo" v-model="schedule.schedule_no" required>

                <label for="stationIds">Station IDs:</label>
                <multiselect v-model="schedule.station_ids" :options="stations" id="stationIds" multiple required></multiselect>

                <label for="carriageIds">Carriage IDs:</label>
                <multiselect v-model="schedule.carriage_ids" :options="carriages" id="carriageIds" multiple required></multiselect>

                <label for="departureTime">Departure Time:</label>
                <input type="datetime-local" id="departureTime" v-model="schedule.departure_time" required>

                <label for="arrivalTimes">Arrival Times:</label>
                <div v-for="(arrivalTime, index) in schedule.arrival_times" :key="index">
                    <input type="datetime-local" v-model="schedule.arrival_times[index]" required>
                    <button type="button" @click="removeArrivalTime(index)">Remove Arrival Time</button>
                </div>
                <button type="button" @click="addArrivalTime">Add Arrival Time</button>

                <button type="submit">Update Schedule</button>
            </form>
        </div>
    </div>
</template>

<script>
import Multiselect from '@vueform/multiselect';

export default {
    components: {
        Multiselect
    },
    data() {
        return {
            schedule: {
                schedule_no: '',
                station_ids: [],
                carriage_ids: [],
                departure_time: '',
                arrival_times: []
            },
            stations: [
                { id: 1, name: 'Station 1' },
                { id: 2, name: 'Station 2' },
                { id: 3, name: 'Station 3' },
                { id: 4, name: 'Station 4' },
                { id: 7, name: 'Station 7' }
            ],
            carriages: [
                { id: 1, name: 'Carriage 1' },
                { id: 3, name: 'Carriage 3' },
                { id: 4, name: 'Carriage 4' }
            ]
        };
    },
    methods: {
        updateSchedule() {
            // Make API request to update the schedule using this.schedule object and schedule.id
            // You can use axios or any other library for making HTTP requests
            const scheduleId = 1; // Replace with actual schedule ID
            console.log(`Updating schedule with ID: ${scheduleId}`);
            console.log('Schedule:', this.schedule);

            // Reset form fields after successful submission
            this.schedule.schedule_no = '';
            this.schedule.station_ids = [];
            this.schedule.carriage_ids = [];
            this.schedule.departure_time = '';
            this.schedule.arrival_times = [];
        },
        addArrivalTime() {
            this.schedule.arrival_times.push('');
        },
        removeArrivalTime(index) {
            this.schedule.arrival_times.splice(index, 1);
        }
    }
};
</script>

<style>
.container {
    max-width: 500px;
    margin: 0 auto;
    padding: 50px;
}

h1 {
    margin-bottom: 20px;
}

.scrollable {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #ccc;
    padding: 50px;
    margin-bottom: 20px;
}

label {
    display: block;
    margin-top: 10px;
}

input[type="text"],
input[type="datetime-local"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
    margin-top: 5px;
}

multiselect {
    margin-top: 5px;
}

button {
    padding: 8px 16px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
}

button:hover {
    background-color: #0056b3;
}

button[type="submit"] {
    background-color: #28a745;
}

button[type="submit"]:hover {
    background-color: #1e7e34;
}

button[type="button"] {
    background-color: #dc3545;
}

button[type="button"]:hover {
    background-color: #a71d2a;
}
</style>









