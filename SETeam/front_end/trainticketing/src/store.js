import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            user: null,  //记录当前登录的用户名，在登录时存，在任意页面需要显示时取
            jwt:null,    //令牌，用于查询各种信息，在登录的时候存，在所有登录后的页面接口需要添加到header
            account:null,//记录当前查询或基于的账户，在accountmanage页面点击按钮时存，在depositmoney页面取
            bill:null, //记录当前查询的订单，在orderlist页面点击按钮时存，在orderdetails页面取
            schedule:null, //记录当前查询的车次，在querytrain页面点击按钮时存，在ticketbuy页面取

            cur_user:null,//系统管理员专用，用于记录当前管理的用户。
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
        setCurUser(state,cur_user){
            state.cur_user=cur_user;
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
        storeCurUser({ commit },cur_user){
            commit('setCurUser',cur_user);
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
        getCurUser(state){
            return state.cur_user;
        }
    }
});

export default store;
