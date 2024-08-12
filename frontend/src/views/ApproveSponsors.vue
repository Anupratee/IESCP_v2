<template>
  <NavBar />
  <h2>Approve Sponsors</h2>
  <div v-if="!hasSponsors"><h2>No Sponsors needing approval</h2></div>
  <div v-if="hasSponsors"><h2>Sponsors needing approval</h2></div>
  <div class="container">
    <div class="row justify-content-center mb-3">
      <div
        class="col-md-4 mb-3"
        v-for="sponsor in sponsors"
        :key="sponsor.user_id"
      >
        <div class="card h-100">
          <img :src="sponsor.image" class="card-img-top" alt="sponsor_image" />
          <div class="card-body d-flex flex-column">
            <h5 class="card-title">{{ sponsor.name }}</h5>
            <p class="card-text flex-fill">
              <b>ID:</b> {{ sponsor.user_id }} <br />
              <b>Email:</b> {{ sponsor.email }} <br />
              <b>Industry:</b> {{ sponsor.industry }} <br />
              <b>Description:</b> {{ sponsor.description }} <br />
              <b>Location:</b> {{ sponsor.location }} <br />
              <b>Flag:</b> {{ sponsor.flag }}
            </p>
            <button
              class="btn btn-outline-dark"
              data-bs-toggle="modal"
              data-bs-target="#confirmApproveSponsor"
              @click="
                selected_sponsor_id = sponsor.user_id;
                selected_sponsor_name = sponsor.name;
              "
            >
              Approve
            </button>
            <button
              class="btn btn-outline-dark"
              data-bs-toggle="modal"
              data-bs-target="#confirmRejectSponsor"
              @click="
                selected_sponsor_id = sponsor.user_id;
                selected_sponsor_name = sponsor.name;
              "
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" id="confirmApproveSponsor" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Sponsor <b>Approval</b> Confirmation</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Confirm you want to approve {{ selected_sponsor_name }}.</p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-outline-dark"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button
            @click="approveSponsor(selected_sponsor_id)"
            class="btn btn-outline-dark"
          >
            Approve
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" id="confirmRejectSponsor" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Sponsor <b>Rejection</b> Confirmation</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="close"
          ></button>
        </div>
        <div class="modal-body">
          <p>Confirm you want to reject {{ selected_sponsor_name }}.</p>
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-outline-dark"
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button
            @click="rejectSponsor(selected_sponsor_id)"
            class="btn btn-outline-dark"
          >
            Reject
          </button>
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
      sponsors: [],
      selected_sponsor_id: null,
      selected_sponsor_name: "",
    };
  },
  created() {
    this.fetchUnapprovedSponsors();
  },
  computed: {
    hasSponsors() {
      return this.sponsors.length > 0;
    },
  },
  methods: {
    fetchUnapprovedSponsors() {
      fetch("http://localhost:5000/unapproved_sponsors", {
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
          this.sponsors = data.unapproved_sponsors;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
    approveSponsor() {
      fetch(
        `http://localhost:5000/approve_sponsor/${this.selected_sponsor_id}`,
        {
          method: "PUT",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
            "Content-Type": "application/json",
          },
        }
      )
        .then((response) => {
          if (!response.ok) {
            if (
              response.status === 400 ||
              response.status === 403 ||
              response.status === 409
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error approving sponsor");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Sponsor approved");
          (this.selected_sponsor_id = null),
            (this.selected_sponsor_name = null),
            this.$router.go();
        })
        .catch((error) => {
          (this.selected_sponsor_id = null),
            (this.selected_sponsor_name = null),
            alert(error.message);
        });
    },
    rejectSponsor() {
      fetch(
        `http://localhost:5000/delete_sponsor/${this.selected_sponsor_id}`,
        {
          method: "PUT",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
            "Content-Type": "application/json",
          },
        }
      )
        .then((response) => {
          if (!response.ok) {
            if (
              response.status === 400 ||
              response.status === 403 ||
              response.status === 409
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error rejecting sponsor");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Sponsor rejected");
          (this.selected_sponsor_id = null),
            (this.selected_sponsor_name = null),
            this.$router.go();
        })
        .catch((error) => {
          (this.selected_sponsor_id = null),
            (this.selected_sponsor_name = null),
            alert(error.message);
        });
    },
  },
};
</script>
