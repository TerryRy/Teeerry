<template>
  <div id="topline"><TopLine/></div>
	<div id="nav"><userNavline @turnToUserList="turnToUserList" @turnToUserAdd="turnToUserAdd" @turnToUserChange="turnToUserChange"/></div>
  <div class="container">
    <h1>用户列表</h1>
		<div class="user-list">
			<div v-for="user in users" :key="user.id" class="user-item">
				<h3>用户id:</h3>
				<p>{{ user.id }}</p>
				<h3>用户名:</h3>
				<p>{{ user.name }}</p>
				<h3>邮箱:</h3>
				<p>{{ user.email }}</p>
				<h3>用户权限:</h3>
				<p>{{ user.role }}</p>
			</div>
		</div>
  </div>
</template>

<script>
import { ref } from 'vue';
import TopLine from "@/components/common/TopLine.vue";
import userNavline from "@/components/common/userNavline.vue";
export default {
  name:"UserList",
    setup() {
        const users = ref([]);

        // 假设通过接口获取到的时刻表数据为response
        const response = {
            users: [
                {
                    id: 1,
                    name: "K1234",
                    email: "2023-5-4-11:11:00",
                    role: "普通用户",
                },
								{
                    id: 2,
                    name: "G1234",
                    email: "2023-5-24-11:11:00",
                    role: "管理员",
                },
            ]
        };

        // 在mounted钩子中将response中的数据赋值给users
        const mounted = () => {
            users.value = response.users;
        };

        return {
            users,
            mounted
        };
    },
    mounted() {
        this.mounted();
    },
	components: {userNavline, TopLine},
};
</script>

<style scoped>
.container {
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

.user-list {
	/* max-height: 350px; */
	overflow-y: auto;
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
</style>