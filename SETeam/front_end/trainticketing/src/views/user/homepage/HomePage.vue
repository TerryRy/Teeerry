<template>
<div id="topline"><TopLine/></div>
<div><NavLine/></div>
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
#HomePage {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#topline{
  position: relative;
  top:0px;
}
</style>