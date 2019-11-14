import axios from 'axios';
import Vue from 'vue';
import Vuex from 'vuex';
import VueRouter from 'vue-router';

import App from './App.vue';
import ContactsList from './components/ContactsList.vue';
import ContactDetail from './components/ContactDetail.vue';

import '../node_modules/spectre.css/dist/spectre.css';
import '../node_modules/spectre.css/dist/spectre-icons.css';

/*
 * Set up Vue
 */
Vue.config.productionTip = false;
Vue.use(VueRouter);
Vue.use(Vuex);

/* 
 * Set up axios
 */
window.axios = axios;
window.axios.defaults.baseURL = 'http://ec2-54-218-214-243.us-west-2.compute.amazonaws.com:5000/api';
if (process.env.NODE_ENV == 'development') {
    window.axios.defaults.baseURL = 'http://localhost:5000/api';
}

/*
 * Vue route set up
 */
const routes = [
    { path: '/', component: App,
      children: [
          { path: '', component: ContactsList, meta: { title: 'Contacts List' } },
          { path: '/contact/:id', component: ContactDetail, props: true, meta: { title: 'Contacts Detail' } }
      ]
    }
];
const router = new VueRouter({
    mode: 'history',
    routes
});

/*
 * Use the store to save contact list query parameters
 */
const store = new Vuex.Store({
    state: {
        listPage: 1,
        listPageSize: 10,
        listSortField: 'id',
        listSortDir: 'asc'
    },
    mutations: {
        setListPage(state, value) {
            state.listPage = value;
        },
        setListPageSize(state, value) {
            state.listPageSize = value;
        },
        setListSortField(state, value) {
            state.listSortField = value;
        },
        setListSortDir(state, value) {
            state.listSortDir = value;
        }
    }
});

/* 
 * Instantiate Vue
 */
new Vue({
    render: h => h(App),
    router,
    store
}).$mount('#app');
