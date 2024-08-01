<template>
  <div><h2>Admin Home</h2></div>
  <br />
  <div class="container my-4">
    <div class="row">
      <div class="col-md-4">
        <div class="card text-white bg-primary mb-3">
          <div class="card-body">
            <h5 class="card-title">Total Users</h5>
            <p class="card-text" id="total-users">{{ total_users }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success mb-3">
          <div class="card-body">
            <h5 class="card-title">Total Campaigns</h5>
            <p class="card-text" id="total-campaigns">
              {{ total_campaigns }}
            </p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-danger mb-3">
          <div class="card-body">
            <h5 class="card-title">Total Ads</h5>
            <p class="card-text" id="total-ads">{{ total_ads }}</p>
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
      ads: [],
      total_users: null,
      total_campaigns: null,
      total_ads: null,
    };
  },
  created() {
    this.fetchCampaigns();
    this.fetchAds();
    this.fetchTotalStats();
  },
  computed: {
    hasCampaigns() {
      return this.campaigns.length > 0;
    },
    hasAds() {
      return this.ads.length > 0;
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
    fetchTotalStats() {
      fetch("http://localhost:5000/total_stats", {
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
          this.total_users = data.total_users;
          this.total_campaigns = data.total_campaigns;
          this.total_ads = data.total_ads;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
  },
};
</script>
