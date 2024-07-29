<template>
  <div><h2>Sponsor Home</h2></div>
  <div v-if="hasCampaigns"><h2>Your Campaigns</h2></div>
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
            <h5 class="card-title">{{ campaign.name }}</h5>
            <p class="card-text flex-fill">
              Status: {{ campaign.status }} <br />
              Description: {{ campaign.description }} <br />
            </p>
            <router-link
              :to="`/sponsor-home/campaigns/${campaign.id}`"
              class="btn btn-primary"
              >View</router-link
            >
            <button
              class="btn btn-danger"
              data-bs-toggle="modal"
              data-bs-target="#confirmDeleteCampaign"
              @click="
                selected_campaign_id = campaign.id;
                selected_campaign_name = campaign.name;
              "
            >
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="modal" id="confirmDeleteCampaign" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Confirm Campaign Deletion</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="close"
          ></button>
        </div>
        <div class="modal-body">
          <p>
            Confirm you want to delete {{ selected_campaign_name }}. This will
            also delete all ads in the campaign.
          </p>
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
            @click="deleteCampaign(selected_campaign_id)"
            class="btn btn-danger"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="container">
    <h2>Create Campaign</h2>
    <br />
    <form
      @submit.prevent="createCampaign"
      enctype="multipart/form-data"
      class="create_campaign_form"
    >
      <label for="campaign_name" class="form-label">Name of Campaign</label>
      <input
        type="text"
        id="campaign_name"
        class="form-control"
        v-model="campaign_name"
        requried
      />
      <br />
      <div>
        <div>
          <label for="categorySelect">Category</label>
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
      <button type="submit" class="btn btn-primary">Add Campaign</button>
      <br />
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      campaigns: [],
      categories: [],
      selected_campaign_id: null,
      selected_campaign_name: "",
      campaign_name: "",
      selected_category_id: null,
      description: "",
      image: null,
    };
  },
  created() {
    this.fetchCampaigns();
    this.fetchCategories();
  },
  computed: {
    hasCampaigns() {
      return this.campaigns.length > 0;
    },
  },
  methods: {
    fetchCampaigns() {
      fetch("http://localhost:5000/campaigns_by_sponsor", {
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
    deleteCampaign() {
      fetch(
        `http://localhost:5000/delete_campaign/${this.selected_campaign_id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
            "Content-Type": "application/json",
          },
        }
      )
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
              throw new Error("Error deleting campaign");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Campaign deleted");
          (this.selected_campaign_id = null),
            (this.selected_campaign_name = null),
            this.$router.go();
        })
        .catch((error) => {
          (this.selected_campaign_id = null),
            (this.selected_campaign_name = null),
            alert(error.message);
        });
    },
    uploadImage() {
      this.image = this.$refs.file.files[0];
    },
    createCampaign() {
      const formData = new FormData();
      formData.append("category_id", this.selected_category_id);
      formData.append("name", this.campaign_name);
      formData.append("description", this.description);
      formData.append("image", this.image);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch("http://localhost:5000/create_campaign", {
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
              throw new Error("Error adding campaign");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("New campaign added!");
          this.fetchCampaigns();
          (this.selected_category_id = null),
            (this.campaign_name = ""),
            (this.description = ""),
            (this.image = null),
            this.$router.push("/sponsor-home");
        })
        .catch((error) => {
          (this.selected_category_id = null),
            (this.campaign_name = ""),
            (this.description = ""),
            (this.image = null),
            alert(error.message);
        });
    },
  },
};
</script>
