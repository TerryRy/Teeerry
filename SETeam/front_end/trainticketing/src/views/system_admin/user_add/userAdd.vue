<template>
	<div id="topline"><TopLine/></div>
	<div id="nav"><userNavline @turnToUserList="turnToUserList" @turnToUserAdd="turnToUserAdd" @turnToUserChange="turnToUserChange"/></div>
	<div class="add-schedule">
		<h1>添加用户</h1>
		<div class="form-container">
			<form @submit.prevent="submitForm">
				<label for="userName">用户名：</label>
				<input type="text" id="userName" v-model="userName" required>

				<label for="password">密码：</label>
				<input type="text" id="password" v-model="password" required>

				<label for="email">邮箱：</label>
				<input type="text" id="email" v-model="email" required>

				<label for="role">权限：</label>
				<input type="text" id="role" v-model="role" v-if="allowInput" required>
				<select v-model="selectedOption" v-else>
					<option value="option1">普通用户</option>
					<option value="option2">系统管理员</option>
					<option value="option3">铁路管理员</option>
				</select>
							
				<button type="submit" @click="addUser()">添加用户</button>
			</form>
		</div>
	</div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import userNavline from "@/components/common/userNavline.vue";
// import axios from 'axios';

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
    showTextInput() {
      return this.allowInput && this.selectedOption === '';
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
	background-color: #f4f4f4a4;
}

h1 {
	margin-bottom: 20px;
}

.form-container {
	max-height: 350px; /* 设置适当的高度 */
	overflow-y: auto;
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
</style>