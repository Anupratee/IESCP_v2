<template>
  <br />
  <div class="container">
    <div v-if="hasAds"><h3>All Ads</h3></div>
    <table class="table table-hover" v-if="hasAds">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Description</th>
          <th scope="col">Budget</th>
          <th scope="col">Status</th>
          <th scope="col">Campaign</th>
          <th scope="col">Sponsor</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ad in ads" :key="ad.id">
          <td>{{ ad.name }}</td>
          <td>{{ ad.description }}</td>
          <td>{{ ad.budget }}</td>
          <td>{{ ad.status }}</td>
          <td>{{ ad.campaign_name }}</td>
          <td>{{ ad.sponsor_name }}</td>
          <td>
            <router-link
              :to="`/influencer-home/ads/${ad.id}`"
              class="btn btn-primary"
              >View</router-link
            >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ads: [],
    };
  },
  created() {
    this.fetchAds();
  },
  computed: {
    hasAds() {
      return this.ads.length > 0;
    },
  },
  methods: {
    fetchAds() {
      fetch("http://localhost:5000/ads", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          this.ads = data.ads;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
  },
};
</script>
