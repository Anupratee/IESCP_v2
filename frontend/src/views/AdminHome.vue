<template>
  <div>
    <h2>Admin Home</h2>
    <br />
    <div class="container my-4">
      <div class="row">
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Users</h5>
              <p class="card-text" id="total-users">{{ total_users }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Sponsors</h5>
              <p class="card-text" id="total-campaigns">
                {{ total_sponsors }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Influencers</h5>
              <p class="card-text" id="total-ads">{{ total_influencers }}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Campaigns</h5>
              <p class="card-text" id="total-users">{{ total_campaigns }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Ads</h5>
              <p class="card-text" id="total-campaigns">
                {{ total_ads }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card mb-3">
            <div class="card-body">
              <h5 class="card-title">Total Requests</h5>
              <p class="card-text" id="total-ads">{{ total_requests }}</p>
            </div>
          </div>
        </div>
      </div>
      <br />
      <div class="row">
        <div class="col-md-12">
          <div class="card mb-3">
            <div class="card-body">
              <h4 class="card-title">Sponsors and Influencers Distribution</h4>
              <img
                :src="chartUrl"
                alt="Sponsors and Influencers Chart"
                class="img-fluid"
              />
            </div>
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
      total_sponsors: null,
      total_influencers: null,
      total_campaigns: null,
      total_ads: null,
      total_requests: null,
      chartUrl: "",
    };
  },
  created() {
    this.fetchCampaigns();
    this.fetchAds();
    this.fetchTotalStats();
    this.fetchChart();
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
          throw new Error("Network response was not ok.");
        })
        .then((data) => {
          this.campaigns = data.campaigns;
        })
        .catch((error) => {
          console.error("Error fetching campaigns:", error);
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
          throw new Error("Network response was not ok.");
        })
        .then((data) => {
          this.ads = data.ads;
        })
        .catch((error) => {
          console.error("Error fetching ads:", error);
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
          throw new Error("Network response was not ok.");
        })
        .then((data) => {
          this.total_users = data.total_users;
          this.total_sponsors = data.total_sponsors;
          this.total_influencers = data.total_influencers;
          this.total_campaigns = data.total_campaigns;
          this.total_ads = data.total_ads;
          this.total_requests = data.total_requests;
        })
        .catch((error) => {
          console.error("Error fetching total stats:", error);
        });
    },
    fetchChart() {
      fetch("http://localhost:5000/pie_chart/sponsors_influencers", {
        responseType: "blob",
      })
        .then((response) => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error("Network response was not ok.");
        })
        .then((blob) => {
          const url = URL.createObjectURL(blob);
          this.chartUrl = url;
        })
        .catch((error) => {
          console.error("Error fetching chart:", error);
        });
    },
  },
};
</script>
