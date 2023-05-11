<template>
  <div id="topline"><TopLine/></div>
  <div><NavLine/></div>
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

</style>