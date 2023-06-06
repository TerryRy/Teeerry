<template>
    <div v-if="updateTableVisible" id="dia">
        <el-dialog custom-class="transparent-dialog" class="custom-dialog" style="height:350px;width: 400px;border-radius: 30px;background-color: rgba(255, 255, 255, 1);" v-model="updateTableVisible" modal:false>
            <el-row style="width: 100%; background-color: rgba(255,255,255,0);">
                <el-col :span="24">
                    <update-user @updated="updateTableVisible=false"></update-user>
                </el-col>
            </el-row>
        </el-dialog>
    </div>
  <el-backtop :right="100" :bottom="100" />
  <div id="topline"><TopLine/></div>
	<div id="nav"><userNavline/></div>
  <div class="container">
    <h1>用户列表</h1>
		<div class="user-list">
      <div style="margin: 0 auto;width:1100px">
      <el-table  :data="users" width="100%" :stripe="true" :border="true" fit>
<!--        <el-table-column type="index"></el-table-column>-->
        <el-table-column prop="id" label="UID" width="100px"></el-table-column>
        <el-table-column prop="username" label="用户名" width="150px"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="300px"></el-table-column>
        <el-table-column label="用户权限" width="150px">
          <template v-slot="{ row }">
            <p v-for="group in row.groups" :key="group.name">{{ group.name }}</p>
          </template>
        </el-table-column>
        <el-table-column label="名下账户" type="expand" width="150px">
          <template v-slot="{ row }">
            <el-table  :data="row.accounts"  :stripe="true" :border="true" >
              <el-table-column type="index"></el-table-column>
              <el-table-column prop="name" label="账户名" width="200px"></el-table-column>
              <el-table-column prop="id" label="银行卡号" width="400px"></el-table-column>
              <el-table-column prop="amount" label="余额" width="400px"></el-table-column>、
            </el-table>
<!--            <p v-for="account in row.accounts" :key="account.id">{{ account.id }}<br>{{ account.name }}<br>{{ account.card_id }}<br>{{ account.amount }}</p>-->
          </template>
        </el-table-column>

          <el-table-column label="操作" width="250px">
              <template v-slot="{ row }">
                  <el-button  type="default" @click="updateUser(row)">更改信息</el-button>
                  <el-button  type="danger" @click="deleteUser(row.id)">注销用户</el-button>
              </template>
          </el-table-column>

      </el-table>
<!--			<div v-for="tUser in users" :key="tUser.id" class="user-item">-->
<!--				<h3>用户id:</h3>-->
<!--				<p>{{ tUser.id }}</p>-->
<!--				<h3>用户名:</h3>-->
<!--				<p>{{ tUser.name }}</p>-->
<!--				<h3>邮箱:</h3>-->
<!--				<p>{{ tUser.email }}</p>-->
<!--				<h3>用户权限:</h3>-->
<!--                <p v-for="group in tUser.groups" :key="group.name">{{ group.name }}</p>-->
<!--                <h3>名下账户:</h3>-->
<!--                <p v-for="account in tUser.accounts" :key="account.id">{{ account.id }}<br>{{ account.name }}<br>{{ account.card_id }}<br>{{ account.amount }}</p>-->
<!--                &lt;!&ndash;                <button type="checkAccount" @click="checkAccount()">查看账户</button>&ndash;&gt;-->
<!--                <button  @click="deleteUser(tUser.id)">注销用户</button>-->
<!--			</div>-->
      </div>
		</div>
  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import userNavline from "@/components/common/userNavline.vue";
import axios from 'axios';
import {ElMessage} from "element-plus";
import updateUser from "@/views/system_admin/user_list/updateUser.vue";

export default {
  name:"UserList",
  computed: {
      user() {
          return this.$store.getters.getUser;
      },
      jwt() {
          return this.$store.getters.getJwt;
      },
  },
        // 在mounted钩子中将response中的数据赋值给users
      data() {
          return {
              updateTableVisible: false,
              users: []
          }
      },

      methods: {
          updateUser(teUser) {
              if (teUser.id === 8) {
                  ElMessage.error("无法修改根用户信息");
              }
          else {
              this.$store.commit('setUserId', teUser.id);
              this.$store.commit('setUserName', teUser.username);
              this.$store.commit('setUserEmail', teUser.email);
     //         alert(this.$store.getters.getUserName);
              this.updateTableVisible = true;
          }
      },

          deleteUser(id) {
              if (id === 8) {
                  ElMessage.error("无法删除根用户");
                  return;
          }
              axios.delete('api/users/' + id,
                  {headers: {'jwt': `${this.jwt}`}})
                  .then(function(response) {
                      if (response.data.result !== 0) {
                          ElMessage.error(response.data.message);
                      } else {
                          // window.location.reload();
                          ElMessage({message:"注销成功",type:'success'});
                          this.$router.go(0);
                     }
                  })
                  .catch(function () {
                      alert("网络错误，请稍后重试");
                  })
          },

      },


    mounted() {
        const jwt = localStorage.getItem('jwt');
        if (jwt) {
            this.$store.commit('setJwt', jwt);
        }
        const user = localStorage.getItem('user');
        if (user) {
            this.$store.commit('setUser', user);
        }

        axios.get('api/users/',
            {headers: {'jwt': `${this.jwt}`}})
            .then(response => {
                 this.users = response.data.users;// 响应数据
            })
            .catch(error => {
                console.error(error); // 错误信息
            });

    },
	components: {updateUser, userNavline, TopLine},
};
</script>

<style scoped>

.el-table-colum th {
    text-align: center;
}

.container {
	min-height: calc(100vh - 124px);
  min-width: 100vw;
  top:0;
	/*margin: 150px auto;*/
  margin: 0 0;
	/*padding: 40px;*/
	border: 1px solid #ccc;
	border-radius: 4px;
	background-color: #f4f4f4a4;
}

button[type="deleteUser"] {
    padding: 10px 20px;
    background-color: #962626;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 5px;
}

button[type="checkAccount"] {
    padding: 10px 20px;
    background-color: #0056b3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 5px;
}

h1 {
	margin-bottom: 20px;
}

.user-list {
	/*min-height: calc(100vh - 124px);*/
	/*overflow-y: auto;*/
  margin: 0 auto;
}

.user-item {
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