<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToWorkspace="turnToWorkspace" @turnToTrainAdd="turnToTrainAdd" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="add-station">
        <h1>添加站点</h1>
        <form @submit.prevent="submitForm">
            <label for="stationNo">站点编号：</label>
            <input type="text" id="stationNo" v-model="station.stationNo" required>

            <label for="name">站点名：</label>
            <input type="text" id="name" v-model="station.name" required>

            <input type="button" value="添加站点" @click="addStation" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        </form>
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
        }
    },
    data() {
        return {
            station: {
                stationNo: '',
                name: ''
            }
        };
    },
    mounted() {
        // 从本地存储中恢复用户名到 Vuex 的 state 中
        const username = localStorage.getItem('username');
        if (username) {
            this.$store.commit('setUser', username);
        }
        const jwt = localStorage.getItem('jwt');
        if(jwt){
            this.$store.commit('setJwt', jwt);
        }
    },
    methods: {
        addStation() {
            if(this.user==="null"){
                alert("登录已过期，请重新登录");
                this.$store.dispatch('logout');
                localStorage.setItem('username', null);
                this.$router.push('/');
                return;
            }
            if(this.station.stationNo==='') {
                alert("请填写站点编号");
            }
            if(this.station.name==='') {
                alert("请填写站点名");
            }
            axios.post('api/schedules/stations',
                {
                    "station_no":this.station.stationNo,
                    "name": this.station.name
                },{headers:{'jwt': `${this.jwt}`}})
                .then(function(response){
                    if(response.data.result!==0) {
                        alert(response.data.message);
                    }
                    else {
                        alert("添加成功！");
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
.add-station {
  height: calc(100vh - 150px);
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
