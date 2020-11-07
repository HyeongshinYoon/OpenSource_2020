<template>
  <div class="intro">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <div id="intro-logo">
      <p class="logo">OwnModel</p>
      <p class="catch-phrase">빠르고 저렴하게</p>
      <p class="catch-phrase">당신이 원하는 모델을 만나다</p>
    </div>
    <router-link to="login" class="btn">로그인</router-link>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
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
@font-face {
  font-family: "AbrilFatface";
  src: url("../assets/AbrilFatface-Regular.ttf") format('truetype');
}

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
}
p {
  margin: 0;
}
#intro-img {
  width: 450px;
}
#intro-logo {
  padding-top: 10vh;
  padding-bottom: 10vh;
}
.intro {
  background-color: #001236;
  height: 100vh;
  width: 100vw;
}
.catch-phrase {
  font-size:30px;
  color: whitesmoke;
}
.logo {
  font-family: "AbrilFatface";
  font-size: 100px;
  color: whitesmoke;
}
.btn {
  width: 300px;
  height: 50px;
  background-color: whitesmoke;
  color: #001236;
  font-size: 25px;
}

</style>
