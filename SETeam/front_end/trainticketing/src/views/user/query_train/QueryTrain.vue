<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine @turnToBillsManage="turnToBillsManage" @turnToAccountManage="turnToAccountManage" @logout="logout"/></div>
  <div id="mainBlock">

  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";

export default {
  name: "QueryTrain",
  components: {NavLine, TopLine}
}
</script>

<style scoped>
#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);;
  width:1400px;
  height: 100vh;
  text-align: center;
}
</style>