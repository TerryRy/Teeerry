<template>
<Topline/>
</template>

<script>
import Topline from 'common/TopLine.vue'
export default {
  name: "HomePage",
  components: {
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
</style>