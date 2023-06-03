<template>
  <el-backtop :right="100" :bottom="100" />
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>通知公告</p>
    </div>
    <div id="secondFloor">
              <p v-if="messages.length===0">暂无消息</p>
      <div v-else class="schedule-list" style="margin: 0 auto; text-align: center;">
        <el-table :resize-sensor="false" :data="messages" style="width: 100%" :stripe="true" :border="true" :fit="false">
          <el-table-column type="index" label="序号" width="100px"></el-table-column>
<!--          <el-table-column type="index" prop="id" label="序号" width="100px">-->
<!--          </el-table-column>-->
          <el-table-column label="内容" width="700px">
            <template v-slot="{ row }">
              <p>{{row.message}}</p>
            </template>
          </el-table-column>
          <el-table-column label="发信人" width="200px">
            <template v-slot="{ row }">
              {{row.from_user}}
            </template>
          </el-table-column>
          <el-table-column prop="send_time" label="发信时间" width="200px">
          </el-table-column>
        </el-table>

      </div>

    </div>

  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import axios from "axios";

export default {
  name: "MessageList",
  components: {NavLine, TopLine},
  data(){
    return{
      messages:[]
    }
  },
  computed:{
    jwt(){
      return this.$store.getters.getJwt;
    },
    isnotlogin(){
      return this.jwt==="null"||this.jwt===null;
    }
  },
  mounted() {
    axios.get('/api/messages/',
        {
          params: {
            "send":false
          },
          headers:{'jwt':`${this.jwt}`}
        }
    )
        .then((response)=>{
          this.messages=response.data.system_messages;
          // alert(this.messages);
        })

  },
  methods:{

  }
}
</script>

<style scoped>
#topline{
  position: relative;
}
#nav{
  position: relative;
}

#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);;
  width:100%;
  text-align: center;
  height: calc(100vh - 150px);
}

#introduceWord{
  position: relative;
  width:100%;
  align-items:center;
  display: block;
  top:50px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#introduceWord button{
  position: absolute;
  right:200px;
  background-color: #ec1616;
  color: #ffffff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#secondFloor{
  position: relative;
  top:50px;
  padding: 0;
  margin: 0 auto;
  display: flex;
}


.schedule_grid {
  position: relative;
  top:50px;
  width:1200px;
  margin: 0 auto;
  display: grid;
  grid-template-rows: repeat(7, 3fr);
  grid-gap: 3px; /* 网格之间的间距 */
  max-height: 500px;
  padding: 10px;
  border-top: 40px;
  overflow-y: scroll;
  line-height: 35px;
}

.schedule {
  background-color: rgba(214, 232, 239, 0.45);
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
  font-size: 16px;
  height: 70px;
  display: flex;
  border-radius: 10px;

}

.id{
  margin: 0;
  padding: 0;
  top:0;
  left:0;
  font-size: 10px;
}

.trainInfo{
  text-align: left;
  display: inline-block;
  font-size: 20px;
}

.stationsInfo{
  display: inline-block;
  margin-right: 10px;
}

#button1{
  display: inline-block;
  position: absolute;
  right:80px;
  background-color: #628ede;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  top: 50px;
  width:300px;
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