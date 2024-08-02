<template>
  <div>
    <h2><b>My Requests</b></h2>
  </div>
  <br />
  <div class="container">
    <div class="row justify-content-center mb-3">
      <div class="col-md-4 mb-3" v-for="request in requests" :key="request.id">
        <div class="card h-100">
          <img
            :src="request.influencer_image"
            class="card-img-top"
            alt="influencer_img"
          />
          <div class="card-body d-flex flex-column">
            <h4 class="card-title">
              <b>{{ request.influencer_name }}</b>
            </h4>
            <p class="card-text flex-fill">
              <b>Ad Name:</b> {{ request.ad_name }} <br />
              <b>Payment Amount:</b> {{ request.payment_amount }} <br />
              <b>Status:</b> {{ request.ad_status }} <br />
              <b>Campaign:</b> {{ request.campaign_name }} <br />
              <b>Sponsor:</b> {{ request.sponsor_name }} <br />
            </p>
            <div
              v-if="request.from_who === 'sponsor'"
              class="d-flex justify-content-between"
            >
              <button
                class="btn btn-success me-2"
                data-bs-toggle="modal"
                data-bs-target="#acceptModal"
                @click="setSelectedRequest(request)"
              >
                Accept
              </button>
              <button
                class="btn btn-primary me-2"
                data-bs-toggle="modal"
                data-bs-target="#negotiateModal"
                @click="setSelectedRequest(request)"
              >
                Negotiate
              </button>
              <button
                class="btn btn-danger"
                data-bs-toggle="modal"
                data-bs-target="#declineModal"
                @click="setSelectedRequest(request)"
              >
                Decline
              </button>
            </div>
            <div
              v-else-if="request.from_who === 'influencer'"
              class="d-flex justify-content-between"
            >
              <button
                class="btn btn-warning me-2"
                data-bs-toggle="modal"
                data-bs-target="#editModal"
                @click="setSelectedRequest(request)"
              >
                Edit
              </button>
              <button
                class="btn btn-danger"
                data-bs-toggle="modal"
                data-bs-target="#retractModal"
                @click="setSelectedRequest(request)"
              >
                Retract
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Accept Modal -->
  <div
    class="modal fade"
    id="acceptModal"
    tabindex="-1"
    aria-labelledby="acceptModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="acceptModalLabel">Accept Request</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to accept this request for
          <b>{{ selectedRequest.ad_name }}</b
          >?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-success" @click="handleAccept">
            Accept
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Negotiate Modal -->
  <div
    class="modal fade"
    id="negotiateModal"
    tabindex="-1"
    aria-labelledby="negotiateModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="negotiateModalLabel">
            Negotiate Request
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <label for="newAmount" class="form-label">New Payment Amount:</label>
          <input
            type="number"
            class="form-control"
            id="newAmount"
            v-model="selectedRequest.payment_amount"
          />
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
            @click="handleNegotiate"
          >
            Negotiate
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Decline Modal -->
  <div
    class="modal fade"
    id="declineModal"
    tabindex="-1"
    aria-labelledby="declineModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="declineModalLabel">Decline Request</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to decline this request for
          <b>{{ selectedRequest.ad_name }}</b
          >?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-danger" @click="handleDecline">
            Decline
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Modal -->
  <div
    class="modal fade"
    id="editModal"
    tabindex="-1"
    aria-labelledby="editModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editModalLabel">Edit Request</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <label for="editAmount" class="form-label"
            >Edit Payment Amount:</label
          >
          <input
            type="number"
            class="form-control"
            id="editAmount"
            v-model="selectedRequest.payment_amount"
          />
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-warning" @click="handleEdit">
            Edit
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Retract Modal -->
  <div
    class="modal fade"
    id="retractModal"
    tabindex="-1"
    aria-labelledby="retractModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="retractModalLabel">Retract Request</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to retract this request for
          <b>{{ selectedRequest.ad_name }}</b
          >?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-danger" @click="handleRetract">
            Retract
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
    this.fetchRequests();
  },
  computed: {
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
      fetch("http://localhost:5000/sponsor_ad_requests", {
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
      fetch(`http://localhost:5000/create_request/${this.selected_ad_id}`, {
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
    rejectRequest() {
      fetch(
        `http://localhost:5000/reject_request/${this.selected_request_id}`,
        {
          method: "DELETE",
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
          alert("Request rejected successfully!");
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
    updateRequest() {
      const formData = new FormData();
      formData.append("payment_amount", this.payment_amount);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
        fetch(
          `http://localhost:5000/update_request/${this.selected_request_id}`,
          {
            method: "PUT",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access_token"),
            },
            body: formData,
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
            alert("Request updated successfully!");
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
      }
    },
  },
};
</script>
