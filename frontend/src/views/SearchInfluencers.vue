<template>
  <div class="container">
    <input
      class="form-control"
      type="text"
      v-model="searchTerm"
      placeholder="Enter influencer name"
    />
    <br />
    <div class="form-group">
      <label for="category">Category</label>
      <select v-model="selectedCategory" class="form-control" id="category">
        <option value="">All Categories</option>
        <option
          v-for="category in categories"
          :key="category.id"
          :value="category.id"
        >
          {{ category.name }}
        </option>
      </select>
    </div>
    <br />
    <button @click="searchInfluencers" class="btn btn-primary">Search</button>
    <br />
    <br />
    <div v-if="loading">Loading...</div>
    <div v-if="!loading && error">
      <p>{{ error }}</p>
    </div>
    <div v-if="!loading && !error">
      <h2>Search Results:</h2>
      <div v-if="hasInfluencers">
        <h3>All Influencers</h3>
      </div>
      <div v-else>
        <p>No influencers found matching your search criteria.</p>
      </div>
      <br />
      <div class="container">
        <div class="row justify-content-center mb-3">
          <div
            class="col-md-4 mb-3"
            v-for="influencer in influencers"
            :key="influencer.id"
          >
            <div class="card h-100">
              <img
                :src="influencer.image"
                class="card-img-top"
                alt="influencer image"
              />
              <div class="card-body d-flex flex-column">
                <h4 class="card-title">
                  <b>{{ influencer.name }}</b>
                </h4>
                <p class="card-text flex-fill">
                  <b>Category:</b> {{ influencer.category_name }} <br />
                  <b>Followers:</b> {{ influencer.followers }} <br />
                  <b>Platforms:</b> {{ influencer.platforms }} <br />
                  <b>Description:</b> {{ influencer.description }} <br />
                  <b>Location:</b> {{ influencer.location }} <br />
                </p>
                <button
                  class="btn btn-primary"
                  data-bs-toggle="modal"
                  data-bs-target="#requestAdModal"
                  @click="
                    selected_influencer_id = influencer.id;
                    selected_influencer_name = influencer.name;
                  "
                >
                  Request
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
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
              Request for ad: {{ selected_influencer_name }}
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
              <label for="adSelect" class="form-label">Select Ad</label>
              <select
                v-model="selected_ad_id"
                class="form-control"
                id="adSelect"
              >
                <option value="">Select an ad</option>
                <option v-for="ad in ads" :key="ad.id" :value="ad.id">
                  {{ ad.name }}
                </option>
              </select>
            </div>
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
            <button @click="requestAd" class="btn btn-success">Send</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      searchTerm: "",
      selectedCategory: "",
      categories: [],
      influencers: [],
      ads: [],
      loading: false,
      error: null,
      selected_influencer_id: null,
      selected_influencer_name: "",
      selected_ad_id: null,
      payment_amount: null,
    };
  },
  computed: {
    hasInfluencers() {
      return this.influencers.length > 0;
    },
  },
  watch: {
    selected_ad_id(newAdId) {
      const selectedAd = this.ads.find((ad) => ad.id === newAdId);
      if (selectedAd) {
        this.payment_amount = selectedAd.budget;
      } else {
        this.payment_amount = null;
      }
    },
  },
  async created() {
    await this.fetchCategories();
    await this.fetchInfluencers();
    await this.fetchAds();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await fetch("http://localhost:5000/categories", {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch categories.");
        }

        const data = await response.json();
        this.categories = data.categories;
      } catch (error) {
        this.error = "An error occurred while fetching categories.";
      }
    },
    async fetchInfluencers() {
      this.loading = true;
      this.error = null;

      try {
        let url = "http://localhost:5000/search_influencers";
        const params = new URLSearchParams();

        if (this.searchTerm) {
          params.append("search_term", this.searchTerm);
        }
        if (this.selectedCategory) {
          params.append("category_id", this.selectedCategory);
        }

        if (params.toString()) {
          url += `?${params.toString()}`;
        }

        const response = await fetch(url, {
          method: "GET",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch influencers.");
        }

        const data = await response.json();
        this.influencers = data.influencers;
      } catch (error) {
        this.error = "An error occurred while fetching influencers.";
      }

      this.loading = false;
    },
    async fetchAds() {
      try {
        const response = await fetch(
          "http://localhost:5000/get_ad_by_sponsor",
          {
            method: "GET",
            headers: {
              Authorization: "Bearer " + localStorage.getItem("access_token"),
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch ads.");
        }

        const data = await response.json();
        this.ads = data.ads;
      } catch (error) {
        this.error = "An error occurred while fetching ads.";
      }
    },
    searchInfluencers() {
      this.fetchInfluencers();
    },
    requestAd() {
      const formData = new FormData();
      formData.append("payment_amount", this.payment_amount);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(
        `http://localhost:5000/sponsor_create_request/${this.selected_ad_id}/${this.selected_influencer_id}`,
        {
          method: "POST",
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: formData,
        }
      )
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
          this.selected_ad_id = null;
          this.selected_ad_name = "";
          this.payment_amount = null;
          this.$router.go();
        })
        .catch((error) => {
          alert(error.message);
          this.selected_ad_id = null;
          this.selected_ad_name = "";
          this.payment_amount = null;
          this.$router.go();
        });
    },
  },
};
</script>
