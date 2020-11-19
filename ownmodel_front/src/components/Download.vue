<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">Download Image</p>
    <div id="photo-wrapper">
      <img id="new-photo" v-bind:src="image_src" />
    </div>
    <div id="buttons">
      <button id="back-button" class="btn" v-on:click="moveBack()">Back</button>
      <button id="next-button" class="btn" v-on:click="moveOn()">Next</button>
      <a id="download-manager" v-bind:href="image_src" download="results.jpg" style="display: none"/>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import loading_image from '../assets/loading.gif'

export default {
  name: "HelloWorld",
  props:['face_id', 'flag', 'body_id'],
  data: function () {
    return {
      image_src: loading_image,
      ready: false,
    };
  },
  methods: {
    moveOn: function() {
      if (!this.ready) {return;}
      this.ready = false;
      axios.post('http://localhost:8888/addLookBook', {
        user_id: this.$cookie.get('user_id'),
      }).then(res => {
        res;
        this.ready = true;
        this.$router.push({ name: 'mypage', params: {'flag': 1}});
      })
      
    },
    moveBack: function() {
      if (!this.ready) {return;}
      this.$router.push({ name: 'face'});
    },
    requestImage() {
      this.ready = false;
      axios.post('http://localhost:8888/selectModel', {
        face_id: this.face_id || 0,
        user_id: this.$cookie.get('user_id'),
        body_id: this.body_id || 0,
      }).then(res => {
        console.log("Download response");
        console.log(res);
        this.image_src = "data:image/png;base64, " + res.data;
        this.ready = true;
      })
    },
    download_img() {
      document.getElementById("download-manager").click();
    }
  },
  created() {
    if (this.$cookie.get('user_id')=='') {
      this.$router.push({ name: 'index'});
      alert("You are not logged in.");
    }
    this.requestImage();
    this.ready=true;
    // this.image_src = fs.readFileSync("./assets/myaccount.png", "base64");
    // console.log(this.image_src);
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@font-face {
  font-family: "AbrilFatface";
  src: url("../assets/AbrilFatface-Regular.ttf") format("truetype");
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
#upload-title {
  font-size: 60px;
  color: #001236;
  margin-top: 20px;
  margin-left: 10%;
  width: fit-content;
}
#photo-wrapper {
  width: 100%;
}
#new-photo {
  height: 400px;
  width: 300px;
  border-style: solid;
  border-width: 5px;
  border-color: #001236;
  border-radius: 20px;
}
#new-photo:hover {
  cursor: pointer;
}
#buttons {
  margin-top: 20px;
}
.btn {
  width: 150px;
  height: 50px;
  margin-left: 10px;
  margin-right: 10px;
  background-color: #001236;
  color: whitesmoke;
  font-size: 30px;
}
.btn:hover {
  color: whitesmoke;
}
</style>
