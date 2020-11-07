import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
  mode: "history",
  routes: [
    {
      path: "/",
      alias: "/index",
      name: "index",
      component: () => import("../components/Intro")
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../components/Login")
    },
    {
      path: "/main",
      name: "main",
      component: () => import("../components/MainPage"),
      children: [
        {
          path: "/mypage",
          alias: "/",
          name: "mypage",
          component: () => import("../components/MyPage")
        },
        {
          path: "/upload",
          name: "upload",
          component: () => import("../components/Upload")
        },
        {
          path: "/body",
          name: "body",
          component: () => import("../components/BodyPage")
        },
        {
          path: "/face",
          name: "face",
          component: () => import("../components/FacePage")
        },
        {
          path: "/download",
          name: "download",
          component: () => import("../components/Download")
        }
      ]
    }
  ]
});