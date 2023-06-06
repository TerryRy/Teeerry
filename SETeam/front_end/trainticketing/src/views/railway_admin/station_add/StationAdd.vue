<template>
    <div id="topline">
        <TopLine />
    </div>
    <div id="nav">
        <railway_Navline
            @turnToWorkspace="turnToWorkspace"
            @turnToTrainAdd="turnToTrainAdd"
            @turnTrainDelete="turnTrainDelete"
            @turnTrainChange="turnTrainChange"
            @logout="logout"
        />
    </div>
    <div class="main">
      <el-row style="width: 100%">
        <el-col :span="12">
          <div class="schedule-list" style="width: 100%;">
            <h1 style="top:50px">站点列表</h1>
            <el-table :data="stations" style="margin: 0 auto;top:50px;width: 600px" max-height="60vh">
              <el-table-column prop="station_no" label="SID" width="200px"></el-table-column>
              <el-table-column prop="name" label="站点名称" width="400px"></el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="add-station">
            <h1>添加站点</h1>
            <form @submit.prevent="submitForm">
                <label for="stationNo"><b>站点编号：</b></label>
              <input type="text" id="stationNo" v-model="station.stationNo" required />

              <label for="name"><b>站点名</b></label>
              <input type="text" id="name" v-model="station.name" required />

              <input type="button" value="添加站点" @click="addStation" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
              <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
            </form>
          </div>
        </el-col>
      </el-row>

    </div>
    <div class="footer">
        <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
    </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import railway_Navline from "@/components/common/railway_Navline.vue";
import axios from "axios";
import {ElMessage} from "element-plus";
export default {
    components: { railway_Navline, TopLine },
    computed: {
        user() {
            return this.$store.getters.getUser;
        },
        jwt() {
            return this.$store.getters.getJwt;
        },
    },
    data() {
        return {
            station: {
                stationNo: "",
                name: "",
            },
          stations:[]
        };
    },
    mounted() {
        // 从本地存储中恢复用户名到 Vuex 的 state 中
        const username = localStorage.getItem("username");
        if (username) {
            this.$store.commit("setUser", username);
        }
        const jwt = localStorage.getItem("jwt");
        if (jwt) {
            this.$store.commit("setJwt", jwt);
        }
      axios.get('api/schedules/stations',
          {
            headers:{'jwt': `${this.jwt}`}
          })
          .then((response)=>
          {
            this.stations=response.data.stations;
          })
    },
    methods: {
        addStation() {
            if (this.user === "null") {
                ElMessage({message:"登录已过期，请重新登录",type:'warning'});
                this.$store.dispatch("logout");
                localStorage.setItem("username", null);
                this.$router.push("/");
                return;
            }

            axios
                .post(
                    "api/schedules/stations",
                    {
                        station_no: this.station.stationNo,
                        name: this.station.name,
                    },
                    { headers: { jwt: `${this.jwt}` } }
                )
                .then((response) => {
                    if (response.data.result !== 0) {
                        ElMessage.error(response.data.message);
                    } else {
                        ElMessage({message:response.data.message,type:'success'});
                    }
                })
                .catch(() => {
                    ElMessage.error("网络错误，请稍后重试。");
                });
        },
    },
};
</script>

<style scoped>
.main {
    width: 100%;
    min-height: calc(100vh - 200px);
    background-color: rgba(255, 255, 255, 0.65);
}

.add-station {
    max-width: 400px;
    top: 20px;
    margin: 0px auto;
    padding: 20px;
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

.button {
    padding: 10px 20px;
    background-color: #4caf50;
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

