<template>
  <router-view />
</template>

<script>
import userMixin from "@/mixins/userMixin";

export default {
  mixins: [userMixin],
  computed: {
    isLoggedIn() {
      return this.logged_in;
    },
    role() {
      return this.role;
    },
    id() {
      return this.id;
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
