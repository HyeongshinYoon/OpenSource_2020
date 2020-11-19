<template>
  <div id="upload">
    <link
      rel="stylesheet"
      href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css"
    />
    <p id="upload-title">Select Face</p>
    <div class="faces-wrapper">
      <div
        v-for="face1 in firstFace"
        v-bind:key="face1.id"
        class="photo-wrapper"
      >
        <img
          v-bind:class="{
            'selected photo': face1.sel,
            'unselected photo': !face1.sel,
          }"
          v-on:click="flipSelect1(face1.id)"
          v-bind:src="face1.src"
        />
      </div>
    </div>
    <div v-if="curr1 > 0" class="faces-wrapper">
      <div
        v-for="face2 in secondFace"
        v-bind:key="face2.id"
        class="photo-wrapper"
      >
        <img
          v-bind:class="{
            'selected photo': face2.sel,
            'unselected photo': !face2.sel,
          }"
          v-on:click="flipSelect2(face2.id)"
          v-bind:src="face2.src"
        />
      </div>
    </div>
    <div id="buttons">
      <button id="back-button" class="btn" v-on:click="moveBack()">Back</button>
      <button id="reload-button" class="btn" v-on:click="refresh()">Refresh</button>
      <button id="next-button" class="btn" v-on:click="moveOn()">Next</button>
      <!-- <a @click="$router.go(-1)" id="back-button" class="btn">Back</a>
      <router-link to="download" id="next-button" class="btn">Next</router-link> -->
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import loading_img from '../assets/loading_square.gif'

export default {
  name: "HelloWorld",
  props:['body_num', 'flag'],
  data: function () {
    return {
      firstFace: [
        { id: 1, sel: false, src: loading_img },
        { id: 2, sel: false, src: loading_img },
        { id: 3, sel: false, src: loading_img },
        { id: 4, sel: false, src: loading_img },
        { id: 5, sel: false, src: loading_img },
      ],
      secondFace: [
        { id: 1, sel: false, src: loading_img },
        { id: 2, sel: false, src: loading_img },
        { id: 3, sel: false, src: loading_img },
        { id: 4, sel: false, src: loading_img },
        { id: 5, sel: false, src: loading_img },
      ],
      curr1: -1,
      curr2: -1,
      ready: true,
    };
  },
  methods: {
    refresh(){
      if (!this.ready) {return;}
      let refresh2 = this.curr2 >= 0;
      this.ready = false;
      if (refresh2) {
        this.flipSelect2(this.curr2);
        this.requestSecondFace();
      } else {
        this.flipSelect1(this.curr1);
        this.requestFirstFace();
      }
    },
    flipSelect1(i) {
      if (!this.ready) {return;}
      if (i<0) {return;}
      if (this.curr1 > 0) {
        this.firstFace[this.curr1 - 1].sel = false;
      }
      if (this.curr2 > 0) {
        this.secondFace[this.curr2 - 1].sel = false;
      }
      if (this.curr1 == i) {
        this.curr1 = -1;
      } else {
        this.curr1 = i;
        this.firstFace[i - 1].sel = true;
        this.requestSecondFace()
      }
      this.curr2 = -1;
    },
    flipSelect2(i) {
      if (!this.ready) {return;}
      if (i<0) {return;}
      if (this.curr1 < 0) {
        return;
      }
      if (this.curr2 > 0) {
        this.secondFace[this.curr2 - 1].sel = false;
      }
      if (this.curr2 == i) {
        this.curr2 = -1;
      } else {
        this.secondFace[i - 1].sel = true;
        this.curr2 = i;
      }
    },
    getColor(f) {
      if (!this.ready) {return;}
      if (f) {
        return "#ED7D31";
      } else {
        return "#001236";
      }
    },
    moveOn: function() {
      if (!this.ready) {return;}
      if (this.curr2 == -1) {
        alert("Please select a face.");
        return;
      }
      this.$router.push({ name: 'download', params: {'flag': 1, 'face_id': this.curr2-1, 'body_id': this.body_num-1}});
    },
    moveBack: function() {
      if (!this.ready) {return;}
      this.$router.push({ name: 'body', params: {'flag': 0 }});
    },
    requestFirstFace() {
      this.ready = false;
      this.curr2 = -1;
      for (let j=0; j<5; j++) {
        this.firstFace[j].src = loading_img;
        this.secondFace[j].src = loading_img;
      }
      if (this.flag == undefined) {
        this.flag = 1;
      }
      axios.post('http://localhost:8888/selectFaceFirst', {
        body_id: this.body_num-1 || 0,
        flag: this.flag || 0,
        user_id: this.$cookie.get('user_id'),
      }).then(res => {
        console.log("RequestFirstFace");
        console.log(res);
        for(let i=0; i<5; i++) {
          this.firstFace[i].src = "data:image/png;base64, " + res.data[i];
        }
        this.ready = true;
      })
    },
    requestSecondFace() {
      this.ready = false;
      for (let j=0; j<5; j++) {
        this.secondFace[j].src = loading_img;
      }
      axios.post('http://localhost:8888/selectFaceSecond', {
        face_id: this.curr1-1 || 0,
        flag: this.flag || 0,
        user_id: this.$cookie.get('user_id'),
      }).then(res => {
        for(let i=0; i<5; i++) {
          this.secondFace[i].src = "data:image/png;base64, " + res.data[i];
        }
        this.ready = true;
      })
    }
  },
  created() {
    if (this.$cookie.get('user_id')=='') {
      this.$router.push({ name: 'index'});
      alert("You are not logged in.");
    }
    this.requestFirstFace()
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
