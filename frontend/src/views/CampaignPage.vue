<template>
  <NavBar />
  <div>
    <h2>
      <b>{{ name }}</b>
    </h2>
    <div class="container">
      <h5><b>Description: </b>{{ description }}</h5>
    </div>
    <h5><b>Category: </b>{{ category_name }}</h5>
    <h5><b>Status: </b>{{ status }}</h5>
  </div>
  <br />
  <br />
  <div class="container">
    <div v-if="hasAds"><h3>All Ads</h3></div>
    <table class="table table-hover" v-if="hasAds">
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
              class="btn btn-outline-dark me-2"
              >View</router-link
            >
            <button
              class="btn btn-outline-dark"
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
  <div class="modal" id="confirmDeleteAd" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Confirm Ad Deletion</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            Confirm you want to delete {{ selected_ad_name }}. This will also
            delete all requests for the Ad.
          </p>
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
            @click="deleteAd(selected_ad_id)"
            class="btn btn-outline-dark"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <br />
  <br />
  <div class="container">
    <h3>Add Advertisement</h3>
    <br />
    <form @submit.prevent="createAd" class="create_ad_form">
      <label for="ad_name" class="form-label">Name of Advertisement</label>
      <input type="text" id="ad_name" class="form-control" v-model="ad_name" />
      <br />
      <label for="ad_budget" class="form-label">Budget in Rupees</label>
      <input
        type="number"
        id="ad_name"
        class="form-control"
        v-model="ad_budget"
      />
      <br />
      <label for="ad_description" class="form-label">Description</label>
      <textarea
        id="ad_description"
        class="form-control"
        rows="6"
        v-model="ad_description"
      ></textarea>
      <br />
      <button type="submit" class="btn btn-outline-dark">
        Add Advertisement
      </button>
    </form>
  </div>
  <br />
  <br />
  <div class="container">
    <h3>Update Campaign</h3>
    <br />
    <form
      @submit.prevent="updateCampaign"
      enctype="multipart/form-data"
      class="update_campaign_form"
      id="update_campaign_form"
      name="update_campaign_form"
    >
      <label for="update_campaign_name" class="form-label"
        >Name of Campaign</label
      >
      <input
        type="text"
        id="update_campaign_name"
        class="form-control"
        v-model="update_campaign_name"
        requried
      />
      <br />
      <div>
        <div>
          <label for="currentCategory">Current Category</label>
          <input
            type="text"
            id="current_category"
            class="form-control"
            v-model="category_name"
            disabled
          />
          <br />
          <label for="categorySelect">Change Category</label>
          <select
            id="categorySelect"
            v-model="selected_category_id"
            required
            class="form-select"
          >
            <option disabled value="">Please select one</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
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
        v-model="status"
        class="form-check-input"
      />
      <br />
      <br />
      <label for="image" class="form-label">Choose an Image</label>
      <br />
      <input
        type="file"
        id="image"
        name="image"
        class="form-control"
        @change="uploadImage"
        ref="file"
      />
      <br />
      <button type="submit" class="btn btn-outline-dark">
        Update Campaign
      </button>
      <br />
    </form>
  </div>
  <br />
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  components: {
    NavBar,
  },
  data() {
    return {
      campaign_id: null,
      category_id: null,
      category_name: "",
      selected_category_id: "",
      name: "",
      description: "",
      status: false,
      image: null,
      update_campaign_name: "",
      update_description: "",
      categories: [],
      ads: [],
      selected_ad_id: null,
      selected_ad_name: "",
      ad_name: "",
      ad_description: "",
      ad_budget: "",
    };
  },
  created() {
    this.campaign_id = this.$route.params.campaign_id;
    this.fetchCampaignData();
    this.fetchCategories();
    this.fetchAds();
  },
  computed: {
    hasAds() {
      return this.ads.length > 0;
    },
  },
  methods: {
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
          this.name = campaignData.name;
          this.update_campaign_name = campaignData.name;
          this.description = campaignData.description;
          this.update_description = campaignData.description;
          this.status = campaignData.status;
          this.image = campaignData.image;
          console.log(data);
          console.log(this.name);
        })
        .catch((error) => {
          alert(error.message);
        });
    },
    fetchCategories() {
      fetch("http://localhost:5000/categories", {
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
          this.categories = data.categories;
          console.log(data);
        })
        .catch((error) => {
          console.error(error.message);
        });
    },
    fetchAds() {
      fetch(`http://localhost:5000/get_ads_by_campaign/${this.campaign_id}`, {
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
    uploadImage() {
      this.image = this.$refs.file.files[0];
    },
    updateCampaign() {
      const formData = new FormData();
      formData.append("category_id", this.selected_category_id);
      formData.append("name", this.update_campaign_name);
      formData.append("description", this.update_description);
      formData.append("status", this.status);
      formData.append("image", this.image);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(`http://localhost:5000/update_campaign/${this.campaign_id}`, {
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
              response.status === 409
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error updating campaign");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Campaign updated successfully!");
          this.fetchCampaignData();
          this.fetchCategories();
          (this.selected_category_id = null),
            (this.update_campaign_name = ""),
            (this.update_description = ""),
            (this.image = null),
            this.$router.push(`/sponsor-home/campaigns/${this.campaign_id}`);
        })
        .catch((error) => {
          (this.selected_category_id = null),
            (this.update_campaign_name = ""),
            (this.update_description = ""),
            (this.image = null),
            alert(error.message);
        });
    },
    createAd() {
      const formData = new FormData();
      formData.append("name", this.ad_name);
      formData.append("description", this.ad_description);
      formData.append("budget", this.ad_budget);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(`http://localhost:5000/create_ad/${this.campaign_id}`, {
        method: "POST",
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
              response.status === 409
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error updating campaign");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Ad created successfully!");
          this.fetchCampaignData();
          this.fetchCategories();
          this.fetchAds();
          (this.ad_name = ""),
            (this.ad_description = ""),
            (this.ad_budget = ""),
            this.$router.push(`/sponsor-home/campaigns/${this.campaign_id}`);
        })
        .catch((error) => {
          (this.ad_name = ""),
            (this.ad_description = ""),
            (this.ad_budget = ""),
            alert(error.message);
        });
    },
    deleteAd() {
      fetch(`http://localhost:5000/delete_ad/${this.selected_ad_id}`, {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (!response.ok) {
            if (
              response.status === 404 ||
              response.status === 403 ||
              response.status === 409
            ) {
              return response.json().then((data) => {
                throw new Error(data.error);
              });
            } else {
              throw new Error("Error deleting Ad");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Ad deleted");
          (this.selected_ad_id = null),
            (this.selected_ad_name = null),
            this.$router.go();
        })
        .catch((error) => {
          (this.selected_ad_id = null),
            (this.selected_ad_name = null),
            alert(error.message);
        });
    },
  },
};
</script>
