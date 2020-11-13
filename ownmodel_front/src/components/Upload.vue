<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">1. Upload Clothes</p>
    <div id="photo-wrapper">
      <input type="file" />
      <img id="new-photo" v-bind:src="image_src" />
    </div>
    <div id="buttons">
      <a @click="$router.go(-1)" id="back-button" class="btn">Back</a>
      <router-link to="body" id="next-button" class="btn">Next</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data: function() {
    return {
      lookbook_photos: ["a", "b", "c", "d", "e", "f"],
      image_src: require("../assets/new_photo.png"),
    };
  },
  methods: {
    loadImage: function(event) {
      alert("File uploaded");
      alert(event);
    },
  },
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
