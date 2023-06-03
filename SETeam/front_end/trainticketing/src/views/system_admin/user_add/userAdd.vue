<template>
	<div id="topline"><TopLine/></div>
	<div id="nav"><userNavline @turnToUserList="turnToUserList" @turnToUserAdd="turnToUserAdd" @turnToUserChange="turnToUserChange"/></div>
	<div class="add-schedule">
		<h1>添加用户</h1>
		<div class="form-container">
      <el-form  label-width="120px">
        <el-form-item label="用户名">
        <el-input v-model="userName" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input type="password" v-model="password" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input type="email" v-model="email" />
        </el-form-item>
        <el-form-item label="权限">
          <el-select v-model="role" placeholder="请选择赋予的身份和权限">
            <el-option label="普通用户" value="Common User" />
            <el-option label="系统管理员" value="System Admin" />
            <el-option label="铁路系统员" value="Train Admin" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="addUser()">添加用户</el-button>
        </el-form-item>
      </el-form>
<!--			<form @submit.prevent="submitForm">-->
<!--				<label for="userName">用户名：</label>-->
<!--				<input type="text" id="userName" v-model="userName" required>-->

<!--				<label for="password">密码：</label>-->
<!--				<input type="text" id="password" v-model="password" required>-->

<!--				<label for="email">邮箱：</label>-->
<!--				<input type="text" id="email" v-model="email" required>-->

<!--				<label for="role">权限：</label>-->
<!--				<input type="text" id="role" v-model="role" v-if="allowInput" required>-->
<!--				<select v-model="role" v-else>-->
<!--					<option value="Common User">普通用户</option>-->
<!--					<option value="System Admin">系统管理员</option>-->
<!--					<option value="Train Admin">铁路管理员</option>-->
<!--				</select>-->
<!--							-->
<!--				<button type="submit" @click="addUser()">添加用户</button>-->
<!--			</form>-->
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

export default {
  name:"UserAdd",
	components: {userNavline, TopLine},
	data() {
    return {
      userName:'',
      password:'',
      email:'',
      allowInput: false,
      role: '',
      selectedOption: ''
    };
  },

  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    jwt() {
      return this.$store.getters.getJwt;
    }
  },

	methods: {
			submitForm() {
					// Perform API request to add the schedule using newSchedule object

					// Reset form fields after successful submission
					this.userName = '';
					this.password = '';
					this.email = '';
					this.role = '';
      },
    addUser() {
        if (this.user==="null") {
            alert("登陆已过期，请重新登陆");
            this.$store.dispatch('logout');
            this.$router.push('/');
        }
      if (this.userName==='') {
        ElMessage.error("用户名不能为空");
        return;
      }
      if (this.password==='') {
        ElMessage.error("密码不能为空");
        return;
      }
      if (this.email==='') {
        ElMessage.error("邮箱不能为空");
        return;
      }
      if (this.role==='') {
        ElMessage.error("权限不能为空");
        return;
      }
      let roles=[];
      roles.push(this.role)
      axios.post('api/users/',
          {
            "name":this.userName,
            "password":this.password,
            "email":this.email,
            "role":roles
          }, {headers: {'jwt': `${this.jwt}`}})
          .then(function(response){
            if (response.data.result!==0) {
              ElMessage.error(response.data.message);
            }
            else {
              ElMessage.success("添加成功");
            }
          })
          .catch(function(){
            alert("网络错误，请稍后重试");
          })
    }
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
  },
}
</script>

<style scoped>
.add-schedule {
	/*max-width: 350px;*/
	/*margin: 150px auto;*/
  height: calc(100vh - 200px);
	padding: 40px;
	border: 1px solid #ccc;
	border-radius: 4px;
	background-color: #f4f4f4a4;
}

h1 {
	margin-bottom: 20px;
}

.form-container {
	/*max-height: 350px; !* 设置适当的高度 *!*/
	/*overflow-y: auto;*/
  width: 400px;
  position: relative;
  margin: 0 auto;
}

label {
	display: block;
	margin-bottom: 20px;
}

select {
	width: 100%;
	padding: 20px;
	font-size: 16px;
	border-radius: 4px;
	border: 1px solid #ccc;
	box-sizing: border-box;
	margin-bottom: 10px;
}

/*input[type="text"] {*/
/*	width: 100%;*/
/*	padding: 20px;*/
/*	font-size: 16px;*/
/*	border-radius: 4px;*/
/*	border: 1px solid #ccc;*/
/*	box-sizing: border-box;*/
/*	margin-bottom: 10px;*/
/*}*/

button {
	padding: 10px 20px;
	background-color: #4CAF50;
	color: white;
	border: none;
	border-radius: 4px;
	cursor: pointer;
	margin-top: 5px;
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