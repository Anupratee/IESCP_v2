<template>
  <div>
    <h2>Influencer Home</h2>
  </div>
  <br />
  <div v-if="hasCampaigns">
    <h2>All Campaigns</h2>
  </div>
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
              :to="`/influencer-home/campaigns/${campaign.id}`"
              class="btn btn-primary"
              >View</router-link
            >
          </div>
        </div>
      </div>
    </div>
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
  <br />
  <div class="container">
    <div v-if="hasRequests">
      <h3>Your Requests</h3>
    </div>
    <table class="table table-hover" v-if="hasRequests">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Description</th>
          <th scope="col">Payment Amount</th>
          <th scope="col">Status</th>
          <th scope="col">Campaign</th>
          <th scope="col">Sponsor</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.ad_name }}</td>
          <td>{{ request.ad_description }}</td>
          <td>{{ request.payment_amount }}</td>
          <td>{{ request.ad_status }}</td>
          <td>{{ request.campaign_name }}</td>
          <td>{{ request.sponsor_name }}</td>
          <td>
            <button
              class="btn btn-success me-2"
              data-bs-toggle="modal"
              data-bs-target="#acceptAdModal"
              @click="
                selected_request_id = request.id;
                selected_ad_name = request.ad_name;
                payment_amount = request.payment_amount;
              "
            >
              Accept
            </button>
            <button
              class="btn btn-primary me-2"
              data-bs-toggle="modal"
              data-bs-target="#negotiateAdModal"
              @click="
                selected_request_id = request.id;
                selected_ad_name = request.ad_name;
                payment_amount = request.payment_amount;
              "
            >
              Negotiate
            </button>
            <button
              class="btn btn-danger"
              data-bs-toggle="modal"
              data-bs-target="#declineAdModal"
              @click="
                selected_request_id = request.id;
                selected_ad_name = request.ad_name;
                payment_amount = request.payment_amount;
              "
            >
              Decline
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div
    class="modal fade"
    id="acceptAdModal"
    tabindex="-1"
    aria-labelledby="acceptAdModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="acceptAdModalLabel">
            Accept ad: {{ selected_ad_name }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to accept ad {{ selected_ad_name }} with payment
          amount {{ payment_amount }}
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-success" @click="acceptRequest">
            Accept
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="negotiateAdModal"
    tabindex="-1"
    aria-labelledby="negotiateAdModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="negotiateAdModalLabel">
            Negotiate ad: {{ selected_ad_name }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="negotiateAmount" class="form-label"
              >New Payment Amount</label
            >
            <input
              type="number"
              class="form-control"
              id="negotiateAmount"
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
            Close
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click="negotiateRequest"
          >
            Negotiate
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="declineAdModal"
    tabindex="-1"
    aria-labelledby="declineAdModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="declineAdModalLabel">
            Decline ad: {{ selected_ad_name }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to decline ad {{ selected_ad_name }}?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-danger" @click="declineRequest">
            Decline
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
      campaigns: [],
      ads: [],
      requests: [],
      selected_ad_id: null,
      selected_ad_name: "",
      payment_amount: null,
      selected_request_id: null,
    };
  },
  created() {
    this.fetchCampaigns();
    this.fetchAds();
    this.fetchRequests();
  },
  computed: {
    hasCampaigns() {
      return this.campaigns.length > 0;
    },
    hasAds() {
      return this.ads.length > 0;
    },
    hasRequests() {
      return this.requests.length > 0;
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
    fetchRequests() {
      fetch("http://localhost:5000/influencer_ad_requests", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then((data) => {
          this.requests = data.requests;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
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
    acceptRequest() {
      fetch(
        `http://localhost:5000/accept_request/${this.selected_request_id}`,
        {
          method: "POST",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        }
      )
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.error);
            });
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Request accepted successfully!");
          (this.selected_request_id = null),
            (this.selected_ad_name = ""),
            (this.payment_amount = null),
            this.$router.go();
        })
        .catch((error) => {
          alert(error.message);
          (this.selected_request_id = null),
            (this.selected_ad_name = ""),
            (this.payment_amount = null),
            this.$router.go();
        });
    },
  },
};
</script>
