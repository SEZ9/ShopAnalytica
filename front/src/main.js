import Vue from 'vue';
import App from './App.vue';
import iView from 'iview';
import 'iview/dist/styles/iview.css';
import locale from 'iview/dist/locale/en-US';

Vue.use(iView,{ locale });

new Vue({
    el: '#app',
    render: h => h(App)
});