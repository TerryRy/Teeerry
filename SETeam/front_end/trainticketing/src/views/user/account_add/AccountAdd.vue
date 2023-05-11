<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">
    <div id="introduceWord">
    <p>添加您的银行卡账户</p>
    </div>
    <div id="accountinput">
      <form id="register-form">
        <p>请设置账户名称</p><input class="scn" type="text" placeholder="账户名称" v-model="accountName"/><br><br>
        <p>请输入银行卡号</p><input class="scn" type="text" placeholder="银行卡号" v-model="accountID"/><br><br>
        <input type="submit" value="添加" @click="addAccount" />&nbsp;&nbsp;
        <input type="button" value="返回" @click="returnToAccountManage" />
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      </form>
    </div>
  </div>
</template>

<script>
import NavLine from "@/components/common/NavLine.vue";
import TopLine from "@/components/common/TopLine.vue";

export default {
  name: "AccountAdd",
  components: {
    NavLine,
    TopLine
  }
}
</script>

<style scoped>
#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);;
  width:1400px;
  min-height: 1000px;
  text-align: center;
}

#introduceWord{
  position: fixed;

  width:1400px;
  align-items:center;
  display: block;
  top:250px;
}

#introduceWord p{
  font-size: 26px;
  font-weight: bold;
  font-family: 华光行书_CNKI, serif;
}

#accountinput{
  position: fixed;
  width: 1400px;
  align-items:center;
  display: block;
  top:300px;
}
</style>