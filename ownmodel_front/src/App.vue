<template>
  <div id="app">
    <router-view></router-view>
    <!--Intro msg="Welcome to Your Vue.js App"/-->
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
@font-face {
  font-family: "AbrilFatface";
  src: url("./assets/AbrilFatface-Regular.ttf") format('truetype');
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 0px;
  padding: 0px;
}
* {
  /* background-color: #001236; */
  font-family: "AbrilFatface";
}
</style>
