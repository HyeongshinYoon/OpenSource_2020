<template>
  <div id="upload">
    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
    <p id="upload-title">3. Select Face</p>
    <div class="faces-wrapper">
      <div v-for="face1 in firstFace" v-bind:key="face1.id" class="photo-wrapper">
        <img v-bind:class="{'selected photo':face1.sel, 'unselected photo':!face1.sel}" v-on:click="flipSelect1(face1.id)" src="../assets/myaccount.png">
      </div>
    </div>
    <div v-if="curr1>0" class="faces-wrapper">
      <div v-for="face2 in secondFace" v-bind:key="face2.id" class="photo-wrapper">
        <img v-bind:class="{'selected photo': face2.sel, 'unselected photo': !face2.sel}" v-on:click="flipSelect2(face2.id)" src="../assets/myaccount.png">
      </div>
    </div>
    <div id="buttons">
      <router-link to="body" id="back-button" class="btn">Back</router-link>
      <router-link to="download" id="next-button" class="btn">Next</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data: function () {
  return {
    firstFace: [
      {id: 1, sel: false, src: "../assets/myaccount.png"},
      {id: 2, sel: false, src: "../assets/myaccount.png"},
      {id: 3, sel: false, src: "../assets/myaccount.png"},
      {id: 4, sel: false, src: "../assets/myaccount.png"},
      {id: 5, sel: false, src: "../assets/myaccount.png"},
    ],
    secondFace: [
      {id: 1, sel: false, src: "../assets/myaccount.png"},
      {id: 2, sel: false, src: "../assets/myaccount.png"},
      {id: 3, sel: false, src: "../assets/myaccount.png"},
      {id: 4, sel: false, src: "../assets/myaccount.png"},
      {id: 5, sel: false, src: "../assets/myaccount.png"},
    ],
    curr1: -1,
    curr2: -1
  }
  },
  methods: {
    flipSelect1(i) {
      if (this.curr1 > 0) {this.firstFace[this.curr1-1].sel = false;}
      if (this.curr2 > 0) {this.secondFace[this.curr2-1].sel = false;}
      this.firstFace[i-1].sel = true;
      this.curr1 = i;
      this.curr2 = -1;      
    },
    flipSelect2(i) {
      if (this.curr1 < 0) {return;}
      if (this.curr2 > 0) {this.secondFace[this.curr2-1].sel = false;}
      this.secondFace[i-1].sel = true;
      this.curr2 = i;
    },
    getColor(f) {
      if (f) {
        return '#ED7D31';
      } else {
        return '#001236';
      }
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
  height: 210px;
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
.faces-wrapper {
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
