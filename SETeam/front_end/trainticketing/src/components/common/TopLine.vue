<template>
  <div id="TopLine">
  <div id="icon"><img src="@/assets/images/icon.png"></div>
  <div id="name"><p>畅游中国铁路售票官方网站</p></div>
  </div>
</template>

<script>

export default {
  name: "TopLine"
}
</script>

<style scoped>
  #TopLine{
    background-color: whitesmoke;
    overflow:hidden;
    display: flex;
    align-items: center;
    flex-wrap:wrap;
    position:fixed;
    top:0px;
    width: 100%;
    height: 80px;
  }
  #icon{
    position: absolute;
    left:5%;
  }
  #icon img{
    width: 65px;
  }
  #name{
    position: absolute;
    left: 10%;
  }
  #name p{
    font-size: 26px;
    font-family: Microsoft YaHei,serif;
    font-weight: bold;
    color: black;
  }
</style>