<template>
    <nav>
        <ul>
            <li id="leftblock"><a href="/workspace" @click="turnToWorkspace">列车时刻表</a></li>
            <li><a href="/stationadd" @click="turnToStationAdd">添加站点</a></li>
            <li><a href="/carriageadd" @click="turnToCarriageAdd">添加车厢</a></li>

<!--            <li><a href="/traindelete" @click="turnToTrainDelete">删减车次</a></li>-->
            <li id="rightblock"><a href="/trainadd" @click="turnToTrainAdd">添加车次</a></li>
<!--            <li ><a href="/trainchange" @click="turnToTrainChange">修改车次</a></li>-->
<!--            <li id="rightblock"><a href="/" @click="logout">退出登录</a></li>-->
        </ul>
    </nav>
</template>

<script>
export default {
    name: "NavLine",
    methods:{
        logout(){
            this.$emit('logout');
        },
        turnToTrainAdd(){
            this.$emit('turnToTrainAdd');
        },
        turnToStationAdd(){
            this.$emit('turnToStationAdd');
        },
        turnToCarriageAdd(){
            this.$emit('turnToCarriageAdd');
        },
        turnToTrainDelete(){
            this.$emit('turnToTrainDelete');
        },
        turnToTrainChange(){
            this.$emit('turnToTrainChange');
        },
        turnToWorkspace(){
            this.$emit('turnToTrainChange');
        },
    }
}
</script>

<style scoped>
nav {
    background-color: #66b9de;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
    top:80px;
    width: 100%;
}

nav ul {
    list-style: none;
    margin: 0;
    padding:0;
    display: flex;
    justify-content: space-between;
}

nav li {
    width:25%;
    margin: 0 10px;
}

nav a {
    color: #fff;
    text-decoration: none;
    padding: 10px;
    display: inline-block;
}

nav a:hover {
    background-color: #0c96cb;
    padding-left: 12%;
    padding-right: 12%;
    display: block;
    font-size:20px;
}

#leftblock {
    padding-left: 10%;
}
#rightblock {
    padding-right: 10%;
}
</style>