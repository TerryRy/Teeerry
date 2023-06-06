2<template>
	<div id="topline"><TopLine/></div>
	<div id="nav"><userNavline @turnToUserList="turnToUserList" @turnToUserAdd="turnToUserAdd" @turnToUserChange="turnToUserChange"/></div>
	<div class="contain">
		<h1>修改用户信息</h1>
		<div class="container">
			<form @submit.prevent="updateUser">
				<label for="userName">用户名：</label>
				<input type="text" id="userName" v-model="userName" required>

<!--				<label for="password">密码：</label>-->
<!--				<input type="text" id="password" v-model="password" required>-->

				<label for="email">邮箱：</label>
				<input type="text" id="email" v-model="email" required>

<!--				<label for="role">权限：</label>-->
<!--				<input type="text" id="role" v-model="role" v-if="allowInput" required>-->
<!--				<select v-model="selectedOption" v-else>-->
<!--					<option value="option1">普通用户</option>-->
<!--					<option value="option2">系统管理员</option>-->
<!--					<option value="option3">铁路管理员</option>-->
<!--				</select>-->
        <br>
				<button type="Update" @click="submitUser()">提交更改</button>
			</form>
			<form @submit.prevent="deleteUser">
				<button type="delete" @click="DeleteUser()">注销用户</button>
			</form>
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

export default {
  name:"UserChange",
	components: {userNavline, TopLine},
	data() {
        return {
            // users: [],
            // firstUser: null,
            // id: null,
            userName: "",
            email: "",
            allowInput: false,
            // role: '',
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
        updateUser() {
            // Make API request to update the schedule using this.schedule object and schedule.id
            // You can use axios or any other library for making HTTP requests
            const userId = 1; // Replace with actual schedule ID
            console.log(`Updating user with ID: ${userId}`);

            // Reset form fields after successful submission
            this.userName = '';
            this.email = '';
            // this.role = '';
        },

        // getUser() {
        //   if (this.email === "null" && this.userName === "null") {
        //     alert("请输入有效信息");
        //   } else if (this.userName !== "null") {
        //     axios.get('api/users/',
        //         {
        //           params: {
        //             "name": this.userName,
        //           },
        //           headers: {'jwt': `${this.jwt}`}
        //         })
        //         .then(response => {
        //           this.users = response.data.users;
        //         })
        //         .catch(error => {
        //           console.log(error);
        //         });
        //   } else if (this.email !== "null") {
        //     axios.get('api/users/',
        //         {
        //           params: {
        //             "email": this.email,
        //           },
        //           headers: {'jwt': `${this.jwt}`}
        //         })
        //         .then(response => {
        //           this.users = response.data.users;
        //         })
        //         .catch(error => {
        //           console.log(error);
        //         });
        //   }
        //   this.firstUser = this.users.at(0);
        //   alert("rwgeugdovhwj;e");
        //   alert(this.firstUser);
        //   // this.id = this.firstUser.id;
        //   this.id = 1;
        // },

        // DeleteUser() {
        //   let users = [];
        //   let firstUser = null;
        //   let id = null;
        //     // this.getUser();
        //   if (this.email === "null" && this.userName === "null") {
        //     alert("请输入有效信息");
        //   } else if (this.userName !== "null") {
        //     axios.get('api/users/',
        //         {
        //           params: {
        //             "name": this.userName,
        //           },
        //           headers: {'jwt': `${this.jwt}`}
        //         })
        //         .then(response => {
        //           users = response.data.users;
        //         })
        //         .catch(error => {
        //           console.log(error);
        //         });
        //   } else if (this.email !== "null") {
        //     axios.get('api/users/',
        //         {
        //           params: {
        //             "email": this.email,
        //           },
        //           headers: {'jwt': `${this.jwt}`}
        //         })
        //         .then(response => {
        //           users = response.data.users;
        //         })
        //         .catch(error => {
        //           console.log(error);
        //         });
        //   }
        //   this.firstUser = users.at(0);
        //   alert("rwgeugdovhwj;e");
        //   alert(this.firstUser);
        //   this.id = this.firstUser.id;
        //   // this.id = 1;
        //
        //     axios.delete('api/users/' + this.id,
        //         {headers: {'jwt': `${this.jwt}`}})
        //         .then(function (response) {
        //             if (response.data.result!==0) {
        //                 alert(response.data.message);
        //             }
        //             else {
        //                 alert("删除成功");
        //             }
        //         })
        //         .catch(function () {
        //             alert("网络错误，请稍后重试");
        //         })
        // },

        submitUser() {
            // this.getUser();
          let users = [];
          let firstUser = null;
          let id = null;
          if (this.email === "null" && this.userName === "null") {
            alert("请输入有效信息");
          } else if (this.userName !== "null") {
            axios.get('api/users/',
                {
                  params: {
                    "name": this.userName,
                  },
                  headers: {'jwt': `${this.jwt}`}
                })
                .then(response => {
                  alert("error1");

                  users = response.data.users;
                  alert("error2");

                  firstUser = users.at(0);
                  alert(users);
                  id = firstUser.id;
                  alert("error3");

                  // this.id = 1;
                  if (this.userName === '' || this.userName === null || this.userName === "null") {
                    this.userName = firstUser.name;
                  }
                  alert("error4");

                  if (this.email === '' || this.email === null || this.email ==="null") {
                    this.email = firstUser.email;
                  }
                  alert("error5");

                  if (this.role === '' || this.role === null || this.role === "null") {
                    this.role = firstUser.role;
                  }
                  alert(id);
                  // let roles = [];
                  // roles.push(this.role);
                  axios.put('api/users/' + id,
                      {
                        name: this.userName,
                        email: this.email,
                        role: this.role
                      }, {headers: {'jwt': `${this.jwt}`}})
                      .then(function (response) {
                        if (response.data.result !== 0) {
                          alert(response.data.message);
                        } else {
                          alert("修改成功");
                          window.location.reload();
                        }
                      })
                      .catch(function () {
                        alert("网络错误，请稍后重试");
                      })
                })
                .catch(error => {
                  console.log(error);
                });
          } else if (this.email !== "null") {
            axios.get('api/users/',
                {
                  params: {
                    "email": this.email,
                  },
                  headers: {'jwt': `${this.jwt}`}
                })
                .then(response => {
                  alert("error1");

                  users = response.data.users;
                  alert("error2");

                  firstUser = users.at(0);
                  alert(users);
                  id = firstUser.id;
                  alert("error3");

                  // this.id = 1;
                  if (this.userName === '' || this.userName === null || this.userName === "null") {
                    this.userName = firstUser.name;
                  }
                  alert("error4");

                  if (this.email === '' || this.email === null || this.email ==="null") {
                    this.email = firstUser.email;
                  }
                  alert("error5");

                  if (this.role === '' || this.role === null || this.role === "null") {
                    this.role = firstUser.role;
                  }
                  alert(id);
                  axios.put('api/users/' + id,
                      {
                        name: this.userName,
                        email: this.email,
                        role: this.role
                      }, {headers: {'jwt': `${this.jwt}`}})
                      .then(function (response) {
                        if (response.data.result !== 0) {
                          alert(response.data.message);
                        } else {
                          alert("修改成功");
                          window.location.reload();
                        }
                      })
                      .catch(function () {
                        alert("网络错误，请稍后重试");
                      })
                })
                .catch(error => {
                  alert("error");
                  console.log(error);
                });
          }
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

      if (this.user === "null") {
        alert("登陆已过期，请重新登陆");
        this.$store.dispatch('logout');
        this.$router.push('/');
      }
    },

}
</script>

<style>

.contain {
	/*max-width: 350px;*/
  height: calc(100vh - 150px);
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
	/*max-height: 350px;*/
	/*overflow-y: auto;*/
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
