<template>
  <nav>
    <div v-if="isLoggedIn">
      <div v-if="role === 'admin'">
        <router-link to="/admin-home">Home</router-link> |
        <router-link to="/admin-home/approve-sponsors">Approve</router-link> |
        <router-link to="/admin-home/campaigns">Campaigns</router-link> |
        <router-link to="/admin-home/ads">Ads</router-link> |
        <router-link to="/login" @click="logout">Logout</router-link>
      </div>
      <div v-if="role === 'sponsor'">
        <router-link to="/sponsor-home">Home</router-link> |
        <router-link :to="`/sponsors/profile/${this.id}`">Profile</router-link>
        |
        <router-link to="/sponsor-home/requests">Requests</router-link> |
        <router-link to="/sponsor-home/search">Search</router-link> |
        <router-link to="/login" @click="logout">Logout</router-link>
      </div>
      <div v-if="role === 'influencer'">
        <router-link to="/influencer-home">Home</router-link> |
        <router-link :to="`/influencers/profile/${this.id}`"
          >Profile</router-link
        >
        |
        <router-link to="/influencer-home/my-ads">My ads</router-link> |
        <router-link to="/influencer-home/search">Search</router-link> |
        <router-link to="/login" @click="logout">Logout</router-link>
      </div>
    </div>
    <div v-if="!isLoggedIn">
      <router-link to="/">Login</router-link> |
      <router-link to="/register-influencer">Register Influencer</router-link> |
      <router-link to="/register-sponsor">Register Sponsor</router-link>
    </div>
  </nav>
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
