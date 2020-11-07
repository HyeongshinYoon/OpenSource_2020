<template>
  <div id="mypage">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <div id="acc-info">
      <div id="acc-img"></div>
      <div class="acc-menu"><p>Musinsha Store</p></div>
      <div class="acc-menu"><p>Edit</p></div>
    </div>
    <div id="lookbook">
      <div id="lookbook-top">
        <p id="lookbook-title">Lookbook</p>
        <router-link to="upload" id="lookbook-next" class="btn">New</router-link>
      </div>      
      <div id="lookbook-list">
        <ul class="grid">
        <li v-for="photo in lookbook_photos" v-bind:key = "photo">
          <img class="lookbook-img" src="../assets/sample.jpg">
        </li>
      </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: function () {
  return {
    lookbook_photos: ["a","b","c","d","e","f"],
  }
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
  margin: 0;
  padding: 0;
}
p {
  margin: 0;
}
#mypage {
  display: grid;
  grid-template: 1fr / 350px 1fr;
  padding-top: 30px;
}
#lookbook-top {
  display: grid;
  grid-template: 1fr / 350px 1fr 150px;
}
#acc-img {
  width: 250px;
  height: 250px;
  background-color: #001236;
  border-radius: 30px;
  margin-left: 70px;
}
#lookbook {
  width: 100%-70px;
  margin-right: 30px;
}
#lookbook-next {
  grid-row: 1;
  grid-column: 3;
  background-color: #001236;
  color: whitesmoke;
  width: 150px;
  align-self: flex-end;
}
#lookbook-title {
  font-size: 65px;
  color: #001236;
  width: fit-content;
}
#lookbook-list {
  width: 100%;
  height: 100%;
  margin-top: 10px;
  border-width: 5px;
  border-style: solid;
  border-color:  #001236;
  border-radius: 20px;
}
.lookbook-img {
  width: 100%;
}
.acc-menu {
  width: 250px;
  height: 50px;
  border-color: #001236;
  border-style: solid;
  background-color:whitesmoke;
  border-width: 5px;
  border-radius: 10px;
  margin-left: 70px;
  margin-top: 15px;
  font-size: 25px;
  align-items: baseline;
}
.btn {
  width: 300px;
  height: 50px;
  background-color: whitesmoke;
  color: #001236;
  font-size: 30px;
}


/* Grid layout */
.grid {
	/* background-color: #ddedfb; */
	list-style: none;
	margin: 0 auto;
	padding: 10px;
	text-align: left;
	width: 100%;
}

.grid li {
	display: inline-block;
	position: relative;
  object-fit: contain;
	width: 25%;
  padding: 10px;
  /* padding-top: 33.3%; */
  /* background-color: cyan; */
}

.grid li a {
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	border: 2px solid #fff;
	height: 99%;
	position: absolute;
	width: 98%;
}
</style>
