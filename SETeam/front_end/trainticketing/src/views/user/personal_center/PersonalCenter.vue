<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>联系人管理</p>
    </div>
    <div id="secondFloor">
      <div id="money">
        <div><h3>{{this.user}},您好!<br>您共有{{accounts.length}}个联系人</h3></div>
        <div>
          <a href="/contactadd"><button style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="add">添加联系人</button></a>
        </div>
      </div>
      <div class="card-grid">
        <p v-if="accounts.length===0">您还没有联系人</p>
        <div class="card" v-for="account in accounts" :key="account.id" :style="getCardColor()">
          <div class="cardInfo">
            <h3>{{account.name}}</h3>
            <span>身份证号：{{account.id_card}}</span>
          </div>
          <div>
            <button id="button1" @click="deleteCard(account)">删除联系人</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer">
    <p>&copy; 2023 畅游中国. All rights reserved. | 联系电话: 15566293351</p>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";
import depositMoney from "@/views/user/deposit_money/DepositMoney.vue";

export default {
  name: "PersonalCenter",
  components: {TopLine, NavLine},
  computed: {
    depositMoney() {
      return depositMoney
    },
    user() {
      return this.$store.getters.getUser;
    },
    jwt(){
      return this.$store.getters.getJwt;
    }
  },
  data(){
    return{
      money:0,
      amount:0,
      colors: [
        'rgba(92, 167, 225, 0.45)',
        'rgba(0, 128, 64, 0.45)',
        'rgba(255, 92, 0, 0.45)',
        'rgba(83, 51, 255, 0.45)',
        'rgba(127, 195, 236, 0.45)',
        'rgba(101, 185, 96, 0.45)',
        'rgba(152, 216, 122, 0.45)',
        'rgba(255, 141, 68, 0.45)',
        'rgba(255, 174, 113, 0.45)',
        'rgba(189, 147, 249, 0.45)',
        'rgba(213, 176, 252, 0.45)'

      ],
      accounts:[]/*
        {
          "id": 1,
          "name": "account1",
          "card_id": "122435543434",
          "amount": 300.00
        },
        {
          "id": 2,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 3,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 4,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 5,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 6,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 7,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 8,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },{
          "id": 9,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },
        {
          "id": 10,
          "name": "account2",
          "card_id": "876543676876",
          "amount": 50.00
        },

        ]*/
    }
  },

  mounted() {
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
    }
    const jwt = localStorage.getItem('jwt');
    if(jwt){
      this.$store.commit('setJwt', jwt);
    }
    axios.get('api/contacts/',
        {
          headers:{'jwt': `${this.jwt}`}
        })
        .then((response)=>
        {
          this.accounts=response.data.contacts;
        })
        .catch(function(){alert("网络异常，请稍后重试！")})
  },

  methods:{
    // eslint-disable-next-line no-unused-vars
    deleteCard(account)
    {
      axios.delete(`/api/contacts/${account.id}`,{headers:{'jwt': `${this.jwt}`}})
          .then((response)=>
          {
            switch (response.data.result)
            {
              case 0:
                alert("删除成功!");
                break;
              default:
                alert("出现一些问题……");
            }
            this.$router.go(0);
          })
          .catch(function () {
            alert("网络错误");
          })
    }
    ,
    getCardColor()
    {
      const randomColor = this.colors[Math.floor(Math.random() * this.colors.length)];
      return { backgroundColor: randomColor };
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
  padding: 0;
  margin: 0;
}

#mainBlock{
  position: relative;
  margin:0 auto;
  padding: 0;
  background-color: rgba(255, 255, 255, 0.8);
  top:0;
  width:100%;
  text-align: center;
  z-index: 0;
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

#secondFloor{
  position: relative;
  top:50px;
  margin: 0 auto;
  padding: 0;
  display: flex;
}

#money{
  position: relative;
  top:0px;
  margin: 0 auto;
  width:600px;
  padding-top: 100px;
}

#money p{
  font-size: 20px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#money h3{
  font-family: 华光行书_CNKI, serif;
  font-size: 30px;
}

.card-grid {
  position: relative;
  top:20px;
  margin: 0 auto;
  width:600px;
  display: grid;
  grid-template-rows: repeat(7, 1fr); /* 三列网格 */
  grid-gap: 3px; /* 网格之间的间距 */
  height: 500px;
  padding: 10px;
  border-top: 40px;
  overflow-y: scroll;
}

.card {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 15px;
  text-align: left;
  font-size: 16px;
  height: 100px;
  display: flex;
  border-radius: 10px;
}

.cardInfo{
  width: 450px;
}


#button1{
  position: absolute;
  right:50px;
  background-color: #ec1616;
  color: #ffffff;
  padding: 10px 10px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

#button2
{
  position: absolute;
  right:150px;
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
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