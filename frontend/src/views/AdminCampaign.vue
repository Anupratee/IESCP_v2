<template>
  <NavBar />
  <div>
    <h2>
      <b>{{ campaign_name }}</b>
    </h2>
    <h5><b>Description: </b>{{ campaign_description }}</h5>
    <h5><b>Category: </b>{{ category_name }}</h5>
    <h5><b>Status: </b>{{ campaign_status }}</h5>
  </div>
  <br />
  <br />
  <div class="container">
    <div v-if="hasAds">
      <h3>All Ads</h3>
    </div>
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
      ads: [],
      campaign_id: null,
      campaign_name: "",
      campaign_status: "",
      category_name: "",
      campaign_description: "",
      selected_ad_id: null,
      selected_ad_name: "",
      payment_amount: null,
    };
  },
  created() {
    this.campaign_id = this.$route.params.campaign_id;
    this.fetchAds();
    this.fetchCampaignData();
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
    fetchCampaignData() {
      fetch(`http://localhost:5000/campaign_by_id/${this.campaign_id}`, {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          const campaignData = data.campaign;
          this.category_name = campaignData.category_name;
          this.campaign_name = campaignData.name;
          this.campaign_description = campaignData.description;
          this.campaign_status = campaignData.status;
          console.log(data);
        })
        .catch((error) => {
          alert(error.message);
        });
    },
  },
};
</script>
