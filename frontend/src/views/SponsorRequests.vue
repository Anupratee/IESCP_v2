<template>
  <div>
    <h2 class="text-center mb-4">
      <b>Your Requests</b>
    </h2>
    <div class="container">
      <div class="row justify-content-center mb-3">
        <div
          class="col-md-4 mb-3"
          v-for="request in requests"
          :key="request.id"
        >
          <div class="card h-100">
            <img
              :src="request.influencer_image"
              class="card-img-top"
              alt="Influencer Image"
            />
            <div class="card-body d-flex flex-column">
              <h4 class="card-title">
                <b>{{ request.ad_name }}</b>
              </h4>
              <div class="card-text flex-fill">
                <b>Ad Description:</b> {{ request.ad_description }} <br />
                <b>Ad Status:</b> {{ request.ad_status }} <br />
                <b>Campaign:</b> {{ request.campaign_name }} <br />
                <b>Payment Amount:</b> {{ request.payment_amount }} <br />
                <hr />
                <b>Influencer Details:</b> <br />
                <b>Name:</b> {{ request.influencer_name }} <br />
                <b>Email:</b> {{ request.influencer_email }} <br />
                <b>Description:</b> {{ request.influencer_description }} <br />
                <b>Location:</b> {{ request.influencer_location }} <br />
                <b>Followers:</b> {{ request.influencer_followers }} <br />
                <b>Platforms:</b> {{ request.influencer_platforms }} <br />
                <b>Flag:</b> {{ request.influencer_flag ? "Yes" : "No" }}
              </div>
              <br />
              <div v-if="request.from_who === 'influencer'">
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
              </div>
              <div v-else-if="request.from_who === 'sponsor'">
                <button
                  class="btn btn-warning me-2"
                  data-bs-toggle="modal"
                  data-bs-target="#editAdModal"
                  @click="
                    selected_request_id = request.id;
                    selected_ad_name = request.ad_name;
                    payment_amount = request.payment_amount;
                  "
                >
                  Edit
                </button>
                <button
                  class="btn btn-danger"
                  data-bs-toggle="modal"
                  data-bs-target="#retractAdModal"
                  @click="
                    selected_request_id = request.id;
                    selected_ad_name = request.ad_name;
                    payment_amount = request.payment_amount;
                  "
                >
                  Retract
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
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
    <div class="modal-dialog modal-dialog-centered">
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
          <button type="button" class="btn btn-primary" @click="updateRequest">
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
          <button type="button" class="btn btn-danger" @click="rejectRequest">
            Decline
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="editAdModal"
    tabindex="-1"
    aria-labelledby="editAdModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="editAdModalLabel">
            Edit ad: {{ selected_ad_name }}
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
            <label for="editAmount" class="form-label"
              >New Payment Amount</label
            >
            <input
              type="number"
              class="form-control"
              id="editAmount"
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
          <button type="button" class="btn btn-warning" @click="updateRequest">
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
  <div
    class="modal fade"
    id="retractAdModal"
    tabindex="-1"
    aria-labelledby="retractAdModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="retractAdModalLabel">
            Retract ad: {{ selected_ad_name }}
          </h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure you want to retract your request for ad
          {{ selected_ad_name }}?
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
          >
            Close
          </button>
          <button type="button" class="btn btn-danger" @click="rejectRequest">
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
      requests: [],
      payment_amount: null,
      selected_request_id: null,
      selected_ad_name: "",
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
