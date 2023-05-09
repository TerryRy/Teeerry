<template>
<div id="topline"><Topline/></div>
<div><NavLine/></div>
</template>

<script>
import Topline from 'common/TopLine.vue'
import NavLine from "@/components/common/NavLine.vue";
export default {
  name: "HomePage",
  components: {
    NavLine,
    Topline
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