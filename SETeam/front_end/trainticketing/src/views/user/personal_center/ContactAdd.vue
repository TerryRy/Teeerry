<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>添加联系人</p>
    </div>
    <div id="accountinput">
      <form id="register-form">
        <span>姓名：&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><input class="scn" type="text" placeholder="联系人姓名" v-model="name"/><br><br>
        <div class="radio-group" style="display: flex;margin: 0 auto;text-align: center;width:290px">
        <span>性别：&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
        <label style="display: flex">
        <input type="radio" v-model="gender" value="M" style="width:20px;">
        <span>男</span>
        </label>
          &nbsp;&nbsp;&nbsp;&nbsp;
        <label style="display: flex">
          <input type="radio" v-model="gender" value="F" style="width:20px;">
          <span>女</span>
        </label>
        </div>
        <span>出生日期：</span><input class="scn" type="date" placeholder="出生日期" v-model="birthdate"/><br><br>
        <span>身份证号：</span><input class="scn" type="text" placeholder="身份证号" v-model="id_card"/><br><br>
        <input type="button" value="添加" @click="addContact" style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; width:100px"/>&nbsp;&nbsp;
        <a href="/personalcenter"><input type="button" value="返回" @click="turnToAccountManage" style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; width:100px"/></a>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
    <div class="footer">
      <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
    </div>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";

export default {
  name: "ContactAdd",
  components: {
    NavLine,
    TopLine
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
    jwt(){
      return this.$store.getters.getJwt;
    }
  },
  data(){
    return{
      name:null,
      gender:null,
      birthdate:null,
      id_card:null
    }
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
  },
  methods:{
    addContact()
    {
      if(this.user==="null")
      {
        alert("登录已过期，请重新登录");
        this.$store.dispatch('logout');
        localStorage.setItem('username', null);
        this.$router.push('/');
        return;
      }
      if(this.Name===null)
      {
        alert("请填写联系人姓名");
      }
      if(this.gender===null)
      {
        alert("请填写性别");
      }
      if(this.birthdate===null)
      {
        alert("请填写出生日期");
      }
      if(this.id_card===null)
      {
        alert("请填写身份整好");
      }
      axios.post('api/contacts/',
          {
            "name": this.name,
            "gender": this.gender,
            "birthdate": this.birthdate,
            "id_card": this.id_card
          },{headers:{'jwt': `${this.jwt}`}})
          .then(function(response){
            if(response.data.result!==0)
            {
              alert(response.data.message);
            }
            else
            {
              alert("添加成功！");
            }
          })
          .catch(function(){
            alert("网络错误，请稍后重试。");
          })
      /*
      axios.post('{{base_url}}/accounts/',
          {
            "account_name": this.accountName,
            "card_holder_name":this.user,
            "card_id":this.accountID
          })
          .then(function(response)
          {
            switch(response.data.result){
              case 0:
              {
                alert("账户添加成功！")
                break;
              }
              default:
                alert("出现问题，请重试。");
                break;
            }
          })
          .catch(function(){alert("网络异常，请稍后重试。");})

       */
    }
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

#accountinput{
  position: relative;
  width: 600px;
  margin: 0 auto;
  align-items:center;
  display: block;
  top:50px;
}
#accountinput input{
  width:200px;
  margin: 0 auto;
  padding: 5px;
  border-radius: 5px;
}
#accountinput span{

  text-align: left;
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
  position: absolute;
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