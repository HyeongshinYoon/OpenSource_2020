import Vue from "vue";
import router from "./routes/OwnmodelRouter";
import App from "./App.vue";
// import axios from "axios";

Vue.config.productionTip = false;
// Vue.prototype.$http = axios;
Vue.use(require("vue-cookie"));

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
