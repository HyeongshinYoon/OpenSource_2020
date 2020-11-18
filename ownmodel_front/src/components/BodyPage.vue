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
      <button id="back-button" class="btn" v-on:click="moveBack()">Back</button>
      <button id="reload-button" class="btn" v-on:click="refresh()">Refresh</button>
      <button id="next-button" class="btn" v-on:click="moveOn()">Next</button>
      <!-- <a @click="$router.go(-1)" id="back-button" class="btn">Back</a>
      <router-link to="face" id="next-button" class="btn">Next</router-link> -->
    </div>
  </div>
</template> 

<script>
import axios from 'axios'
import loading_img from '../assets/loading.gif'

export default {
  name: "BodyPage",
  props:['image_file', 'flag'],
  data: function () {
    return {
      bdy: [
        { id: 1, sel: false, src: loading_img },
        { id: 2, sel: false, src: loading_img },
        { id: 3, sel: false, src: loading_img },
        { id: 4, sel: false, src: loading_img },
        { id: 5, sel: false, src: loading_img },
      ],
      curr: -1,
      ready: false,
    };
  },
  methods: {
    flipSelect(i) {
      if (!this.ready) {return;}
      // console.log(this.image_file);
      // this.bdy[0].src = this.image_file;
      if (i<0) {return;}

      if (this.curr>0) { this.bdy[this.curr - 1].sel = false; }
      this.bdy[i - 1].sel = true;
      if (this.curr == i) {
        this.bdy[i - 1].sel = false;
        this.curr = -1;
      } else {
        this.curr = i;
      }      
    },
    getColor(f) {
      if (f) {
        return "#ED7D31";
      } else {
        return "#001236";
      }
    },
    moveOn: function() {
      if (!this.ready) {return;}
      if (this.curr == -1) {
        alert("Please select a body.");
        return;
      }
      this.$router.push({ name: 'face', params: {'flag': 1, 'body_num': this.curr }});
    },
    moveBack: function() {
      if (!this.ready) {return;}
      this.$router.push({ name: 'upload', params: {'flag': 0 }});
    },
    requestBodies(){
      this.ready = false;
      for(let i=0; i<5; i++) {
        this.bdy[i].src = loading_img;
      }
      // let fl;
      // if (this.flag == undefined) {
      //   fl = 1;
      // } else {
      //   fl = this.flag;
      // }
      axios.post('http://localhost:8888/selectBody', {
        cloth: this.image_file,
        // flag: fl,
        flag: this.flag || 0,
        user_id: this.$cookie.get('user_id'),
      }).then(res => {
        console.log(res);
        for(let i=0; i<5; i++) {
          this.bdy[i].src = "data:image/png;base64, " + res.data[i];
        }
        this.ready = true;
      })
    },
    refresh(){
      console.log("curr="+this.curr);
      this.flipSelect(this.curr);
      this.requestBodies();
    }
  },
  created() {
    if (this.$cookie.get('user_id')=='') {
      this.$router.push({ name: 'index'});
      alert("You are not logged in.");
    }
    this.requestBodies();
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
  grid-row: 1;
  grid-column: 1;

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
