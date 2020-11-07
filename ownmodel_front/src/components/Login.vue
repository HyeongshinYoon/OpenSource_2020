<template>
  <div class="login">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <p class="logo">OwnModel</p>
    <div id="login-box">
      <p class="login-text">로그인</p>
      <div class="form-group">
        <input type="text" name="id" id="id" class="form-control" placeholder="아이디"/>
        <input type="password" name="password" id="password" class="form-control" placeholder="비밀번호" v-model="user.password"/>
      </div>
      <router-link to="main" class="btn">Go</router-link>
    </div>
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
}
p {
  margin: 0;
}
#login-box {
  margin-bottom: 10vh;  
  margin-left: 10vw;
  margin-right: 10vw;
  padding: 20px;
  width: 80vw;
  border-color: whitesmoke;
  border-style: solid;
  border-width: 10px;
}
.login {
   background-color: #001236;
   width: 100vw;
   height: 100vh;
}
.login-text {
  font-size: 40px;
  color: whitesmoke;
  margin-bottom: 20px;
}
.logo {
  font-size: 100px;
  color: whitesmoke;
  padding-top: 20px;
}
.form-group {
  margin-top: 10px;
}
.form-control {
  width: 80%;
  margin: 10px 10%;
}
.btn {
  width: 300px;
  height: 50px;
  background-color: whitesmoke;
  color: #001236;
  font-size: 25px;
}

</style>
