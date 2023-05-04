<template>
  <div><TopLine/></div>
  <div id="content" v-if="loginstatus"><HomePage/></div>
  <div id="content" v-else><WelcomePage :loginstatus="loginstatus" @1000="loginstatus = true"/></div>
</template>

<script>
import TopLine from "@/components/common/TopLine.vue";
import WelcomePage from "welcome_page/WelcomePage.vue";

export default {
  name: 'App',
  components: {
    WelcomePage,
    TopLine
  },
  data(){
    return{
      loginstatus:false
    }
  },
  methods:{
    login(){
      this.loginstatus = true
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
#content{
  position: absolute;
  border-top: 80px;
  width:100%;
}
</style>
