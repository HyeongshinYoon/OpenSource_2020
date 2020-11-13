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
      props: true,
      component: () => import("../components/Intro"),
    },
    {
      path: "/login",
      name: "login",
      props: true,
      component: () => import("../components/Login"),
    },
    {
      path: "/main",
      name: "main",
      props: true,
      component: () => import("../components/MainPage"),
      children: [
        {
          path: "/mypage",
          alias: "/",
          name: "mypage",
          props: true,
          component: () => import("../components/MyPage"),
        },
        {
          path: "/upload",
          name: "upload",
          props: true,
          component: () => import("../components/Upload"),
        },
        {
          path: "/body",
          name: "body",
          props: true,
          component: () => import("../components/BodyPage"),
        },
        {
          path: "/face",
          name: "face",
          props: true,
          component: () => import("../components/FacePage"),
        },
        {
          path: "/download",
          name: "download",
          props: true,
          component: () => import("../components/Download"),
        },
      ],
    },
  ],
});
