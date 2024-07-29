<template>
  <div><h2>Influencer Home</h2></div>
  <div v-if="hasCampaigns"><h2>All Campaigns</h2></div>
  <br />
  <div class="container">
    <div class="row justify-content-center mb-3">
      <div
        class="col-md-4 mb-3"
        v-for="campaign in campaigns"
        :key="campaign.id"
      >
        <div class="card h-100">
          <img
            :src="campaign.image"
            class="card-img-top"
            alt="campaign cover"
          />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ campaign.name }}</h5>
            <p class="card-text flex-fill">
              Status: {{ campaign.status }} <br />
              Description: {{ campaign.description }} <br />
            </p>
            <router-link
              :to="`/sponsor-home/campaigns/${campaign.id}`"
              class="btn btn-primary"
              >View</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
    };
  },
  created() {
    this.fetchCampaigns();
  },
  computed: {
    hasCampaigns() {
      return this.campaigns.length > 0;
    },
  },
  methods: {
    fetchCampaigns() {
      fetch("http://localhost:5000/campaigns", {
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
          this.campaigns = data.campaigns;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
  },
};
</script>
