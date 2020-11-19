<template>
  <div id="mypage">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <div id="acc-info">
      <div id="acc-img">
        <img class="prof-img" src="../assets/musinsha.png"/>
      </div>
      <div class="acc-menu"><p>Musinsha Store</p></div>
      <div class="acc-menu"><p>Edit</p></div>
    </div>
    <div id="lookbook">
      <div id="lookbook-top">
        <a id="download-manager" v-bind:href="download_src" download="results.jpg" style="display: none"/>
        <p id="lookbook-title">Lookbook</p>
        <button id="lookbook-next" class="btn" v-on:click="toNew()">New</button>
        <!-- <router-link to="upload" id="lookbook-next" class="btn">New</router-link> -->
      </div>
      <div id="lookbook-list">
        <ul class="grid">
        <li v-for="photo in lookbook_photos" v-bind:key = "photo.id">
          <img class="lookbook-img" v-bind:src="photo.src" v-on:click="download_img(photo.src)">
        </li>
      </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import loading_image from '../assets/loading_square.gif'

export default {
  name: 'HelloWorld',
  data: function () {
    return {
      lookbook_photos: [{id: 0, src: loading_image}],
      download_src: '',
    }
  },
  methods: {
    toNew() {
      this.$router.push({ name: 'upload', params: {'flag': 1 }});
    },
    download_img(s) {
      this.download_src = s;
      document.getElementById("download-manager").click();
    }
  },
  created() {
    if (this.$cookie.get('user_id')=='') {
      this.$router.push({ name: 'index'});
      alert("You are not logged in.");
    }
    axios.post('http://localhost:8888/getLookbook', {
        user_id: this.$cookie.get('user_id'),
      }).then(res => {
      let lookbook_photos= [];
      console.log(res.data);
      console.log(Object.keys(res.data).length);
      for(let i=0; i<Object.keys(res.data).length; i++) {
        lookbook_photos.push({id: i, src: "data:image/png;base64, "+res.data[i]});
        this.tmp_src = "data:image/png;base64, "+res.data[i];
      }
      if (lookbook_photos.length == 0) {
        lookbook_photos.push({id: 0, src: require("../assets/new_photo.png")});
      }
      this.lookbook_photos = lookbook_photos;
    })
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
  background-color: whitesmoke;
  border-color: #001236;
  border-style: solid;
  border-radius: 30px;
  border-width: 5px;
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
.prof-img {
  width: 100%;
  height: 100%;
  border-radius: 20px;
  overflow: hidden;
  z-index: -1;
}
.lookbook-img {
  width: 100%;
}
.lookbook-img:hover {
  cursor: pointer;
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
