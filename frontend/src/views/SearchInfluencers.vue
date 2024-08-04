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
      searchTerm: "",
      selectedCategory: "",
      categories: [],
      influencers: [],
      loading: false,
      error: null,
      selected_influencer_id: null,
      selected_influencer_name: "",
      ads: [],
    };
  },
  computed: {
    hasInfluencers() {
      return this.influencers.length > 0;
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
    searchInfluencers() {
      this.fetchInfluencers();
    },
  },
};
</script>
