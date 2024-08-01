<template>
  <div>
    <h2>{{ campaign_name }}</h2>
    <p><b>Description: </b>{{ campaign_description }}</p>
    <p><b>Category: </b>{{ category_name }}</p>
    <p><b>Status: </b>{{ campaign_status }}</p>
  </div>
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
            <button
              class="btn btn-primary"
              data-bs-toggle="modal"
              data-bs-target="#requestAdModal"
              @click="
                selected_ad_id = ad.id;
                selected_ad_name = ad.name;
                payment_amount = ad.budget;
              "
            >
              Request
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div
    class="modal fade"
    id="requestAdModal"
    tabindex="-1"
    aria-labelledby="requestAdLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="requestAdLabel">
            Request for ad: {{ selected_ad_name }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="payment_amount" class="form-label"
              >Payment Amount</label
            >
            <input
              type="number"
              class="form-control"
              id="payment_amount"
              v-model="payment_amount"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button
            @click="requestAd(selected_ad_id, payment_amount)"
            class="btn btn-success"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
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
    requestAd() {
      const formData = new FormData();
      formData.append("payment_amount", this.payment_amount);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(`http://localhost:5000/influencer_request/${this.selected_ad_id}`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            if (response.status === 400 || response.status === 409) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error sending request");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Request sent successfully!");
          (this.selected_ad_id = null),
            (this.selected_ad_name = ""),
            (this.payment_amount = null),
            this.$router.go();
        })
        .catch((error) => {
          alert(error.message);
          (this.selected_ad_id = null),
            (this.selected_ad_name = ""),
            (this.payment_amount = null),
            this.$router.go();
        });
    },
  },
};
</script>
