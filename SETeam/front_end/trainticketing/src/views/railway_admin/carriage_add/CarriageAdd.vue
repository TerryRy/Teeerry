<template>
    <div id="topline"><TopLine/></div>
    <div id="nav"><railway_Navline @turnToTrainAdd="turnToTrainAdd" @turnToWorkspace="turnToWorkspace" @turnTrainDelete="turnTrainDelete" @turnTrainChange="turnTrainChange" @logout="logout"/></div>
    <div class="main">
      <el-row style="width: 100%">
        <el-col :span="12">
          <div class="schedule-list" style="width: 100%;">
            <h1 style="top:50px">车厢列表</h1>
            <el-table :data="carriages" style="margin: 0 auto;top:50px;width: 600px" max-height="80vh">
              <el-table-column prop="id" label="CID" width="100px"></el-table-column>
              <el-table-column prop="name" label="类型名称" width="200px"></el-table-column>
              <el-table-column prop="seat_num" label="座位数量" width="150px"></el-table-column>
              <el-table-column prop="increase_rate" label="席位加价率" width="150px"></el-table-column>
            </el-table>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="add-carriage">
            <h1>添加车厢</h1>
            <form @submit.prevent="submitForm">
              <label for="name"><b>车厢名：</b></label>
              <input type="text" id="name" v-model="carriage.name" required>

              <label for="seatNum"><b>座位数量：</b></label>
              <input type="number" id="seatNum" v-model="carriage.seatNum" required>

              <label for="increase_rate"><b>席位加价率：</b></label>
              <input type="number" id="increase_rate" v-model="carriage.increase_rate" required>
              <input type="button" value="添加车厢" @click="addCarriage" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;"/>&nbsp;&nbsp;
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
            carriage: {
                name: '',
                seatNum: null,
                increase_rate : null
            },
          carriages:[]
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
      axios.get('api/schedules/carriages',
          {
            headers:{'jwt': `${this.jwt}`}
          })
          .then((response)=>
          {
            this.carriages=response.data.carriages;
          })
    },
    methods: {
        addCarriage() {
            if(this.user==="null"){
                ElMessage({message:"登录已过期，请重新登录",type:'warning'});
                this.$store.dispatch('logout');
                localStorage.setItem('username', null);
                this.$router.push('/');
                return;
            }
            /*if(this.carriage.name==='') {
                alert("请填写车厢名");
            }
            if(this.carriage.seatNum===null) {
                alert("请填写座位数量");
            }*/
            if(this.carriage.increase_rate<0) {
                ElMessage({message:"席位加价率不能小于0",type:'warning'});
                return;
            }
            axios.post('api/schedules/carriages',
                {
                    "name": this.carriage.name,
                    "seat_num": this.carriage.seatNum,
                    "increase_rate": this.carriage.increase_rate
                },{headers:{'jwt': `${this.jwt}`}})
                .then(function(response){
                    if(response.data.result!==0) {
                        ElMessage.error(response.data.message);
                    }
                    else {
                        ElMessage({message:response.data.message,type:'success'});
                    }
                })
                .catch(function(){
                    ElMessage.error("网络错误，请稍后重试。");
                })
        }
    }
}
</script>

<style scoped>
.main{
    width: 100%;
  min-height: calc(100vh - 200px);
    background-color:rgba(255,255,255,0.65);
}
.add-carriage {
    max-width: 400px;
    top: 20px;
    margin: 0px auto;
    padding: 20px;
    /*//border: 1px solid #ccc;*/
    /*//border-radius: 4px;*/
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
