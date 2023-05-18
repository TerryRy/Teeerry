<template>
  <div id="topline"><TopLine/></div>
  <div id="nav"><NavLine/></div>
  <div id="mainBlock">

  </div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import NavLine from "@/components/common/NavLine.vue";
export default {
  name: "HomePage",
  components: {
    NavLine,
    TopLine
  }
}
</script>

<style scoped>
#topline{
  position: relative;
  top:0px;
}

#mainBlock{
  margin:0 auto;
  background-color: rgba(255, 255, 255, 0.8);;
  width:1400px;
  height: 100vh;
  text-align: center;
}
</style>