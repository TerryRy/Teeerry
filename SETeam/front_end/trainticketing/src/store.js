import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            //全局
            user: null,  //记录当前登录的用户名，在登录时存，在任意页面需要显示时取
            jwt:null,    //令牌，用于查询各种信息，在登录的时候存，在所有登录后的页面接口需要添加到header
            account:null,//记录当前查询或基于的账户，在accountmanage页面点击按钮时存，在depositmoney页面取
            bill:null, //记录当前查询的订单，在orderlist页面点击按钮时存，在orderdetails页面取
            schedule:null, //记录当前查询的车次，在querytrain页面点击按钮时存，在ticketbuy页面取
            departTime:null,
            departure:null,
            destination:null,
            seatType:null,
            ticketID:null,
            schedule_id:null,
            userId: null,
            userName: null,
            userPassword: null,
            userEmail: null,
            userRole: null
        };
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setJwt(state,jwt)
        {
            state.jwt = jwt;
        },
        setAccount(state, account){
            state.account=account;
        },
        setBill(state,bill){
            state.bill=bill;
        },
        setSchedule(state,schedule){
            state.schedule=schedule;
        },
        setDestination(state,destination){
            state.destination=destination;
        },
        setDeparture(state,departure){
            state.departure=departure;
        },
        setDepartTime(state,departTime){
            state.departTime=departTime;
        },
        setSeatType(state,seatType){
          state.seatType=seatType;
        },
        setTicketID(state,ticketID){
            state.ticketID=ticketID;
        },
        setSchedule_id(state,schedule_id){
            state.schedule_id=schedule_id;
        },
        setUserId(state, userId) {
            state.userId=userId;
        },
        setUserName(state, userName) {
            state.userName=userName;
        },
        setUserPassword(state, userPassword) {
            state.userPassword=userPassword;
        },
        setUserEmail(state, userEmail) {
            state.userEmail=userEmail;
        },
        setUserRole(state, userRole) {
            state.userRole=userRole;
        }
    },
    actions: {
        login({ commit }, user, jwt) {
            commit('setJwt',jwt);
            commit('setUser', user);
        },
        logout({ commit }) {
            commit('setUser', null);
            commit('setJwt',null);
        },
        storeAccount({ commit },account) {
            commit('setAccount',account);
        },
        storeBill({ commit },bill) {
            commit('setBill',bill);
        },
        storeSchedule({ commit },schedule){
            commit('setSchedule',schedule);
        },
        storeDestination({ commit },destination){
            commit('setDestination',destination);
        },
        storeDeparture({ commit },departure){
            commit('setDeparture',departure);
        },
        storeDepartTime({ commit },departTime){
            commit('setDepartTime',departTime);
        },
        storeSeatType({ commit },seatType){
            commit('setSeatType',seatType);
        },
        storeTicketID({ commit },ticketID) {
            commit('setTicketID',ticketID);
        },
        storeSchedule_id({ commit },schedule_id){
            commit('setSchedule_id',schedule_id);
        }
    },
    getters: {
        getUser(state) {
            return state.user;
        },
        getJwt(state){
            return state.jwt;
        },
        getAccount(state){
            return state.account;
        },
        getBill(state){
            return state.bill;
        },
        getSchedule(state){
            return state.schedule;
        },
        getDestination(state){
            return state.destination;
        },
        getDeparture(state){
            return state.departure;
        },
        getDepartTime(state){
            return state.departTime;
        },
        getSeatType(state){
            return state.seatType;
        },
        getTicketID(state){
            return state.ticketID;
        },
        getSchedule_id(state){
            return state.schedule_id;
        },
        getUserId(state){
            return state.userId;
        },
        getUserName(state){
            return state.userName;
        },
        getUserPassword(state) {
            return state.userPassword;
        },
        getUserEmail(state) {
            return state.userEmail;
        },
        getUserRole(state) {
            return state.userRole;
        }
    }
});

export default store;
