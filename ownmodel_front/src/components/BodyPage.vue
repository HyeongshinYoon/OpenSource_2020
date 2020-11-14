<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">Select Body</p>
    <div id="bodies-wrapper">
      <div v-for="body in bdy" v-bind:key="body.id" class="photo-wrapper">
        <img
          v-bind:class="{
            'selected photo': body.sel,
            'unselected photo': !body.sel,
          }"
          v-on:click="flipSelect(body.id)"
          v-bind:src="body.src"
        />
      </div>
    </div>
    <div id="buttons">
      <a @click="$router.go(-1)" id="back-button" class="btn">Back</a>
      <router-link to="face" id="next-button" class="btn">Next</router-link>
    </div>
  </div>
</template> 

<script>
import axios from 'axios'

export default {
  name: "BodyPage",
  props:['image_file', 'flag'],
  data: function () {
    return {
      bdy: [
        { id: 1, sel: false, src: require("../assets/new_photo.png") },
        { id: 2, sel: false, src: require("../assets/new_photo.png") },
        { id: 3, sel: false, src: require("../assets/new_photo.png") },
        { id: 4, sel: false, src: require("../assets/new_photo.png") },
        { id: 5, sel: false, src: require("../assets/new_photo.png") },
      ],
      curr: -1,
    };
  },
  methods: {
    flipSelect(i) {
      // console.log(this.image_file);
      this.bdy[0].src = this.image_file;
      
      if (this.curr>0) {this.bdy[this.curr - 1].sel = false;}
      this.bdy[i - 1].sel = true;
      this.curr = i;
    },
    getColor(f) {
      if (f) {
        return "#ED7D31";
      } else {
        return "#001236";
      }
    },
  },
  created() {
    fetch(this.image_file)
      .then(res => res.blob()) // Gets the response and returns it as a blob
      .then(blob => {
        // Here's where you get access to the blob
        // And you can use it for whatever you want
        // Like calling ref().put(blob)

        // Here, I use it to make an image appear on the page
        // let objectURL = URL.createObjectURL(blob);
        // let myImage = new Image();
        // myImage.src = objectURL;
        // document.getElementById('myImg').appendChild(myImage)

        axios.post('http://192.168.243.17:8888/selectBody', { 
          cloth: blob,
          flag: this.flag,
          user_id: this.$cookie.get('user_id')
        }).then(res => {
          console.log(res);
          for(let i=0; i<5; i++) {
            var blob = new Blob([encodeURI(res.data[i])], { type: 'image/jpg' });
            var file = new File([blob], 'tmp_file.jpg', {type: 'image/jpg', lastModified: Date.now()});
            console.log(file);
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = e =>{
                // this.image_src = e.target.result;
                // this.new_src = e.target.result;
                // console.log(e.target.result);
                this.bdy[i].src = e.target.result;
            };
          }
        })
    });
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
.photo-wrapper {
  width: 100%;
  padding: 5px;
}
.photo {
  height: 280px;
  width: 210px;
  padding: 10px;
  border-style: solid;
  border-width: 5px;
  border-radius: 20px;
}
.selected {
  border-color: #ED7D31;
}
.unselected {
  border-color: #001236;
}
#buttons {
  margin-top: 20px;
}
#bodies-wrapper {
  display: grid;
  grid-template: 1fr / 1fr 1fr 1fr 1fr 1fr;
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
