<template>
  <nav>
    <div v-if="isLoggedIn">
      <div v-if="role === 'admin'">
        <router-link to="/admin-home">Home</router-link> |
        <router-link to="/login" @click="logout">Logout</router-link> |
        <router-link to="/admin-home/approve-sponsors">Approve</router-link> |
        <router-link to="/admin-home/campaigns">Campaigns</router-link> |
        <router-link to="/admin-home/ads">Ads</router-link>
      </div>
      <div v-if="role === 'sponsor'">
        <router-link to="/sponsor-home">Home</router-link> |
        <router-link :to="`/sponsors/profile/${this.id}`">Profile</router-link>
        | <router-link to="/login" @click="logout">Logout</router-link> |
      </div>
      <div v-if="role === 'influencer'">
        <router-link to="/influencer-home">Home</router-link> |
        <router-link :to="`/influencers/profile/${this.id}`"
          >Profile</router-link
        >
        | <router-link to="/login" @click="logout">Logout</router-link> |
      </div>
    </div>
  </nav>
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
