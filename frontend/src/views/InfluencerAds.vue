<template>
  <div>
    <h3>My Ads</h3>
    <br />
    <div class="container">
      <table class="table table-hover" v-if="hasAds">
        <thead>
          <tr>
            <th scope="col">Name</th>
            <th scope="col">Description</th>
            <th scope="col">Budget</th>
            <th scope="col">Status</th>
            <th scope="col">Campaign</th>
            <th scope="col">Sponsor</th>
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
          </tr>
        </tbody>
      </table>
      <p v-else>No ads available.</p>
    </div>
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
      fetch("http://localhost:5000/influencer_ads", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.error || "Error fetching ads");
            });
          }
          return response.json();
        })
        .then((data) => {
          this.ads = data.ads;
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
  },
};
</script>
