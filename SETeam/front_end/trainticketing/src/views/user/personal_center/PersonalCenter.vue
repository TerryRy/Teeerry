<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>我的个人信息</p>
    </div>
    <div id="secondFloor">
      <div>
        <table>
          <!--<tr>
            <th>字段</th>
            <th>值</th>
            <th>操作</th>
          </tr>-->
          <tr v-for="(field, index) in fields" :key="index">
            <td>{{ field.label }}</td>
            <td v-if="!field.editing">
              <span v-if="field.type === 'password'">{{ hidePassword(field.value) }}</span>
              <span v-else>{{ field.value }}</span>
            </td>
            <td v-else>
              <input
                  v-model="field.value"
                  :type="field.type"
              />
            </td>
            <td>
              <button @click="toggleEditing(field)">
                {{ field.editing ? '保存' : '修改' }}
              </button>
            </td>
          </tr>
        </table>
      </div>
      <!--
      <table>
        <tbody>
        <tr>
          <th class="vertical-header">乘车人姓名</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">乘坐车次</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">车厢号</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">座位号</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">出发时间</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">出发地</th>
          <td>{{}}</td>
        </tr>
        <tr>
          <th class="vertical-header">目的地</th>
          <td>{{}}</td>
        </tr>
        </tbody>
      </table>
--->
    </div>
  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
import axios from "axios";

export default {
  name: "PersonalCenter",
  components: {NavLine, TopLine},
  data() {
    return {
      fields: [
        { label: '用户名', value: 'John Doe', editing: false },
        { label: '邮箱', value: 'johndoe@example.com', editing: false },
        { label: '密码', value: '********', editing: false, type: 'password' },
        // 其他字段
      ]
    };
  },
  methods:{
    storePersonInfo()
    {
      axios();
    },
    toggleEditing(field) {
      if(field.editing)
      {
        alert(field.value);
        this.storePersonInfo();
      }
      field.editing = !field.editing;
    },
    hidePassword(password) {
      return password.replace(/./g, '*');
    }
  }
}
</script>

<style scoped>
#topline{
  position: fixed;
  z-index: 9999;
}
#nav{
  position: fixed;
  z-index: 9999;
}

#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);
  top:150px;
  width:1400px;
  height: 500vh;
  text-align: center;
  z-index: 10;
}

#introduceWord{
  position: fixed;
  width:1400px;
  align-items:center;
  display: block;
  top:200px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#secondFloor{
  position: fixed;
  top:300px;
  padding: 0;
  margin: 0;
  display: flex;
}

table {
  border-collapse: collapse;
  width: 800px;
  margin-left: 300px;
  margin-right: 300px;
  padding-top: 50px;
  position: absolute;
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #66b9de;
  font-weight: bold;
  width: 300px;
}

td{
  width: 500px;
  background-color: lightcyan;
}

#buttons{
  position: relative;
  width: 1400px;
  top:350px;
}
</style>