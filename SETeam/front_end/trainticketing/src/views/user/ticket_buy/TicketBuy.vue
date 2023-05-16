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
  name: "TicketBuy",
  components: {NavLine, TopLine}
}
</script>

<style scoped>

</style>