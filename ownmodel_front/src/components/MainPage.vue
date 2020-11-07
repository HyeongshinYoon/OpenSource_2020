<template>
  <div class="login">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <div id="top-banner" class="grid">
      <router-link to="/index" class="logo-grid"><img class="logo" src="../assets/logo.png"></router-link>
      <router-link to="/main" class="myacc-grid"><img class="myacc" src="../assets/myaccount.png"></router-link>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: function () {
  return {
    user: {
      id: '',
      password: ''
    }}
  },
  methods: {
    logIn: function () {
      alert("login pressed");
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h3 {
  margin: 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0;
}
a {
  color: #42b983;
  margin: 0;
  padding: 0;
}
p {
  margin: 0;
}
#top-banner {
  width: 100%;
  height: 60px;
  border-bottom-style: solid;
  border-bottom-width: 2px;
  border-bottom-color: #001236;
}
.grid {
  display: grid;
  grid-template: 1fr / 100px 1fr 160px;
}
.logo {
  height: 60px;
  padding-top: 15px;
  padding-bottom: 15px;
  padding-left: 100px;
}
.myacc {
  width: 60px;
  height: 60px;
  padding: 10px;
}
.logo-grid {
  grid-row: 1;
  grid-column: 1;
}
.myacc-grid {
  grid-row: 1;
  grid-column: 3;
}
</style>
