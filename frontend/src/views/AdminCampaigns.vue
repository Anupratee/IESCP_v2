<template>
  <NavBar />
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
            <h4 class="card-title">
              <b>{{ campaign.name }}</b>
            </h4>
            <p class="card-text flex-fill">
              <b>Category:</b> {{ campaign.category_name }} <br />
              <b>Status:</b> {{ campaign.status }} <br />
              <b>Description:</b> {{ campaign.description }} <br />
              <b>By:</b> {{ campaign.sponsor_name }} <br />
            </p>
            <router-link
              :to="`/admin-home/campaigns/${campaign.id}`"
              class="btn btn-outline-dark"
              >View</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  components: {
    NavBar,
  },
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
