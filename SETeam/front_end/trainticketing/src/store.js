import { createStore } from 'vuex';

const store = createStore({
    state() {
        return {
            user: null,
            account:null,
            bill:null
        };
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setAccount(state, account){
            state.account=account;
        },
        setBill(state,bill){
            state.bill=bill;
        }
    },
    actions: {
        login({ commit }, user) {
            // 在这里进行登录逻辑
            // ...
            // 登录成功后将用户信息保存到 state 中
            commit('setUser', user);
        },
        logout({ commit }) {
            // 在这里进行注销逻辑
            // ...
            // 将用户信息置为 null
            commit('setUser', null);
        },
        storeAccount({ commit },account) {
            commit('setAccount',account);
        },
        storeBill({ commit },bill) {
            commit('setBill',bill);
        }
    },
    getters: {
        getUser(state) {
            return state.user;
        },
        getAccount(state){
            return state.account;
        },
        getBill(state){
            return state.bill;
        }
    }
});

export default store;
