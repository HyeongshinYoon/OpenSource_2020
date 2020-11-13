<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">2. Select Body</p>
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
      <!-- <router-link to="upload" id="back-button" class="btn">Back</router-link> -->
      <router-link to="face" id="next-button" class="btn">Next</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data: function () {
    return {
      bdy: [
        { id: 1, sel: false, src: require("../assets/new_photo.png") },
        { id: 2, sel: false, src: require("../assets/new_photo.png") },
        { id: 3, sel: false, src: require("../assets/new_photo.png") },
        { id: 4, sel: false, src: require("../assets/new_photo.png") },
        { id: 5, sel: false, src: require("../assets/new_photo.png") },
      ],
      curr: 1,
    };
  },
  methods: {
    flipSelect(i) {
      this.bdy[this.curr - 1].sel = false;
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
