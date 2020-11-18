<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">Upload Clothes</p>
    <!-- <form id="upload-form" action="/" -->
      <div id="photo-wrapper">
        <input id="upload_logic" type="file" v-on:change="uploadImage" style="display: none"/>
        <img id="new-photo" v-bind:src="image_src" v-on:click="clickUpload()"/>
      </div>
      <div id="buttons">
        <button id="back-button" class="btn" v-on:click="moveBack()">Back</button>
        <!-- <a @click="$router.go(-1)" id="back-button" class="btn">Back</a> -->
        <button id="next-button" class="btn" v-on:click="moveOn()">Next</button>
      </div> 
  </div>
</template>

<script>
import axios from 'axios'
import loading_img from '../assets/loading.gif'
import new_img from '../assets/new_photo.png'

export default {
  name: "HelloWorld",
  props:['flag'],
  data: function() {
    return {
      image_src: loading_img,
      ready: false,
    };
  },
  methods: {
    uploadImage: function(event) {
      if (!this.ready) {return;}
      this.ready = false;
      const reader = new FileReader();
      reader.readAsDataURL(event.target.files[0]);
      reader.onload = e =>{
          this.image_src = e.target.result;
          this.ready = true;
          console.log(e.target.result);
      };
    },
    clickUpload: function() {
      if (!this.ready) {return;}
      document.getElementById("upload_logic").click();
    },
    moveOn: function() {
      if (!this.ready) {return;}
      if (this.curr < 0) {
        alert("Please choose a body.");
        return;
      }
      this.$router.push({ name: 'body', params: {'image_file': this.image_src, 'flag': 1 }});
    },
    moveBack: function() {
      if (!this.ready) {return;}
      this.$router.push({ name: 'mypage'});
    }
  },
  created() {
    this.ready = false;
    if (this.$cookie.get('user_id')=='') {
      this.$router.push({ name: 'index'});
      alert("You are not logged in.");
    }
    axios.post('http://localhost:8888/startUpload', {
      flag: this.flag || 0,
      user_id: this.$cookie.get('user_id'),
    }).then(res => {
      if (Object.keys(res.data).length != 0) {
        this.image_src = "data:image/png;base64, " + res.data[0];
      } else {
        this.image_src = new_img;
      }
      this.ready = true;      
    }) 
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
  width: 300px;
  height: 400px;
  border-style: solid;
  border-width: 5px;
  border-color: #001236;
  border-radius: 20px;
  margin-left: auto;
  margin-right: auto;
}
#new-photo {
  margin: auto;
  width: 100%;
  height:100%;
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
