<template>
  <div>
    <h2>{{ name }}</h2>
  </div>
  <div>
    <div v-if="hasrequests"><h3>All Requests</h3></div>
    <table class="table table-hover" v-if="hasrequests">
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Name</th>
          <th scope="col">Description</th>
          <th scope="col">Budget</th>
          <th scope="col">Status</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ad in ads" :key="ad.id">
          <td>{{ ad.id }}</td>
          <td>{{ ad.name }}</td>
          <td>{{ ad.description }}</td>
          <td>{{ ad.budget }}</td>
          <td>{{ ad.status }}</td>
          <td>
            <router-link
              :to="`/sponsor-home/ads/${ad.id}`"
              class="btn btn-primary"
              >View</router-link
            >
            <button
              class="btn btn-danger"
              data-bs-toggle="modal"
              data-bs-target="#confirmDeleteAd"
              @click="
                selected_ad_id = ad.id;
                selected_ad_name = ad.name;
              "
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="container">
    <h2>Update Advertisement</h2>
    <br />
    <form
      @submit.prevent="updateAd"
      class="update_ad_form"
      id="update_ad_form"
      name="update_ad_form"
    >
      <label for="update_ad_name" class="form-label"
        >Name of Advertisement</label
      >
      <input
        type="text"
        id="update_ad_name"
        class="form-control"
        v-model="update_ad_name"
        requried
      />
      <br />
      <label for="update_ad_budget" class="form-label">Budget in Rupees</label>
      <input
        type="number"
        id="update_ad_budget"
        name="update_ad_budget"
        class="form-control"
        v-model="update_ad_budget"
        required
      />
      <br />
      <label for="description" class="form-label">Description</label>
      <textarea
        id="description"
        class="form-control"
        rows="6"
        v-model="update_description"
        requried
      ></textarea>
      <br />
      <label for="completed" class="form-label">Mark as Completed</label>
      <br />
      <input
        type="checkbox"
        id="completed"
        v-model="update_status"
        class="form-check-input"
      />
      <br />
      <br />
      <button type="submit" class="btn btn-primary">
        Update Advertisement
      </button>
      <br />
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      ad_id: null,
      name: "",
      budget: null,
      description: "",
      status: "",
      update_ad_name: "",
      update_ad_budget: null,
      update_description: "",
    };
  },
  created() {
    this.ad_id = this.$route.params.ad_id;
    this.fetchAdData();
  },
  methods: {
    fetchAdData() {
      fetch(`http://localhost:5000/get_ad_by_id/${this.ad_id}`, {
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
          const adData = data.ad;
          this.name = adData.name;
          this.update_ad_name = adData.name;
          this.description = adData.description;
          this.update_description = adData.description;
          this.budget = adData.budget;
          this.update_ad_budget = adData.budget;
          this.status = adData.status;
          console.log(data);
        });
    },
    updateAd() {
      const formData = new FormData();
      formData.append("update_name", this.update_ad_name);
      formData.append("update_description", this.update_description);
      formData.append("update_budget", this.update_ad_budget);
      formData.append("update_status", this.update_status);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(`http://localhost:5000/update_ad/${this.ad_id}`, {
        method: "PUT",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            if (
              response.status === 400 ||
              response.status === 403 ||
              response.status === 409 ||
              response.status === 404
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error updating ad");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Ad updated successfully!");
          this.fetchAdData();
          (this.update_ad_name = ""),
            (this.update_ad_budget = null),
            (this.update_description = ""),
            (this.status = null),
            this.$router.push(`/sponsor-home/ads/${this.ad_id}`);
        })
        .catch((error) => {
          (this.update_ad_name = ""),
            (this.update_ad_budget = null),
            (this.update_description = ""),
            (this.status = null),
            alert(error.message);
        });
    },
  },
};
</script>
