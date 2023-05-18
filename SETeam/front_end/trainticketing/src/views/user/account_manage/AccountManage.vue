<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
      <p>账户管理</p>
    </div>
    <div id="secondFloor">
      <div id="money">
        <div><h3>{{this.user}},您好!<br>您的账户情况如下:</h3></div>
        <div><p>账户余额:{{money}}元</p></div>
        <div><p>账户数量:{{amount}}</p></div>
        <div>
          <a href="/accountadd"><button style="background-color: #f1f0f0; color: black; padding: 10px 20px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;" @click="add">添加账户</button></a>
        </div>
      </div>
      <div class="card-grid">
        <div class="card" v-for="account in accounts" :key="account.id" :style="getCardColor()">
          <div class="cardInfo">
            <p3>{{account.name}}</p3>
            <p>{{account.card_id}}</p>
          </div>
          <div>
            <button id="button2" @click="deposit(account)">充值</button>
            &nbsp;&nbsp;
            <button id="button1" @click="deleteCard(account.id)">删除账户</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";
import axios from "axios";
import depositMoney from "@/views/user/deposit_money/DepositMoney.vue";

export default {
  name: "AccountManage",
  components: {TopLine, NavLine},
  computed: {
    depositMoney() {
      return depositMoney
    },
    user() {
      return this.$store.getters.getUser;
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
      accounts:[
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

        ]
    }
  },

  mounted() {
    const username = localStorage.getItem('username');
    if (username) {
      this.$store.commit('setUser', username);
    }
    axios.get('{{base_url}}/accounts',
        {

        })
        .then(function(response)
        {
          this.accounts=response.data.accounts;
        })
        .catch(function(){})
  },

  methods:{
    // eslint-disable-next-line no-unused-vars
    deleteCard(accountid)
    {
      const token = localStorage.getItem('jwtToken');
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios({
        "method": "DELETE",
        "body": {
          "mode": "raw",
          "raw": "",
          "options": {
            "raw": {
              "language": "json"
            }
          }
        },
        "url": {
          "raw": "{{base_url}}/accounts/{{accountid}}",
          "host": [
            "{{base_url}}"
          ],
          "path": [
            "accounts",
            "{{accountid}}"
          ]
        }
      })
        .then(function(response)
        {
          switch(response.data.result){
            case 0:
            {
              break;
            }
            default:
              alert("出现问题，请重试。");
              break;
          }
        })
        .catch(function(){alert("网络异常，请稍后重试。");})
    },
    deposit(account)
    {
      this.$store.dispatch('storeAccount', account);
      localStorage.setItem('storeAccount', account);
      this.$router.push('/depositmoney');
    },
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
  top:0px;
  width:1400px;
  height: 100vh;
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

#money{
  position: absolute;
  top:0px;
  left:50px;
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
  position: absolute;
  top:0px;
  left:750px;
  width:600px;
  display: grid;
  grid-template-rows: repeat(3, 1fr); /* 三列网格 */
  grid-gap: 3px; /* 网格之间的间距 */
  height: 500px;
  padding: 10px;
  border-top: 40px;
  overflow-y: scroll;
}

.card {
  background-color: #fff;
  border: 1px solid #ccc;
  padding: 20px;
  text-align: center;
  font-size: 16px;
  height: 50px;
  display: flex;
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
</style>