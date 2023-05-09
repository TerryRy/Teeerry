<template>
  <div id="content" v-if="loginstatus"><HomePage/></div>
  <div id="content" v-else><WelcomePage :loginstatus="loginstatus" @login="loginstatus = true"/></div>
</template>

<script>
import WelcomePage from "welcome_page/WelcomePage.vue";
import HomePage from "@/views/homepage/HomePage.vue";
import '@/assets/css/backgroundimage.css'

export default {
  name: 'App',
  components: {
    WelcomePage,
    HomePage
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
  border-top: 0px;
  padding-top: 0px;
  top:0px;
  width:100%;
}

</style>
