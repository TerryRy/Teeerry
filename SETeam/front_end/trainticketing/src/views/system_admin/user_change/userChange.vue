<template>
	<div id="topline"><TopLine/></div>
	<div id="nav"><userNavline @turnToUserList="turnToUserList" @turnToUserAdd="turnToUserAdd" @turnToUserChange="turnToUserChange"/></div>
	<div class="contain">
		<h1>修改用户信息</h1>
		<div class="container">
			<form @submit.prevent="updateUser">
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

				<button type="submit">提交更改</button>
			</form>
			<form @submit.prevent="deleteUser">
				<button type="delete">注销用户</button>
			</form>
		</div>
	</div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import userNavline from "@/components/common/userNavline.vue";

export default {
  name:"UserChange",
	components: {userNavline, TopLine},
	data() {
    return {
      allowInput: false,
      role: '',
      selectedOption: ''
    };
	},
	methods: {
		updateUser() {
			// Make API request to update the schedule using this.schedule object and schedule.id
			// You can use axios or any other library for making HTTP requests
			const userId = 1; // Replace with actual schedule ID
			console.log(`Updating user with ID: ${userId}`);

			// Reset form fields after successful submission
			this.userName = '';
			this.password = '';
			this.email = '';
			this.role = '';
		},

		deleteUser() {
      // Make API request to delete the schedule using this.schedule object and schedule.id
      // You can use axios or any other library for making HTTP requests
      const userId = 1; // Replace with actual schedule ID
      console.log(`Deleting user with ID: ${userId}`);
		},
	}
}
</script>

<style>

.contain {
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

.container {
	max-height: 350px;
	overflow-y: auto;
}

label {
	display: block;
	margin-bottom: 20px;
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

select {
	width: 100%;
	padding: 20px;
	font-size: 16px;
	border-radius: 4px;
	border: 1px solid #ccc;
	box-sizing: border-box;
	margin-bottom: 10px;
}

/*button[type="delete"] {*/
/*	padding: 10px 20px;*/
/*	background-color: #0056b3;*/
/*	color: white;*/
/*	border: none;*/
/*	border-radius: 4px;*/
/*	cursor: pointer;*/
/*	margin-top: 5px;*/
/*}*/

/*button[type="submit"] {*/
/*	padding: 10px 20px;*/
/*	background-color: #4CAF50;*/
/*	color: white;*/
/*	border: none;*/
/*	border-radius: 4px;*/
/*	cursor: pointer;*/
/*	margin-top: 5px;*/
/*}*/
</style>
