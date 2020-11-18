<template>
  <div class="login">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <p class="logo">OwnModel</p>
    <div id="login-box">
      <p class="login-text">Log in</p>
      <div class="form-group">
        <input type="text" name="id" id="id" class="form-control" v-model="user.id" placeholder="ID"/>
        <input type="password" name="password" id="password" class="form-control" placeholder="Password" v-model="user.password"/>
      </div>
      <!-- <router-link to="main" class="btn">Go</router-link> -->
      <button class="btn" v-on:click="logIn()">Go</button>
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
      // if (this.user.id=='' || this.user.password=='') {
      //   alert("Fail");
      //   // return; 
      // } else {
      //   alert("Success");
        this.$cookie.set('user_id',this.user.id,'1h');
        this.$router.push({ path: 'main'});
      // }
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
  margin-left: 20vw;
  margin-right: 20vw;
  margin-top: 20px;
  padding: 20px;
  width: 60vw;
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
  font-size: 45px;
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
  margin: 5px 10%;
  height: 40px;
  font-size: 30px;
}
.btn {
  width: 300px;
  height: 50px;
  background-color: whitesmoke;
  color: #001236;
  font-size: 25px;
  margin-top: 10px;
}

</style>

