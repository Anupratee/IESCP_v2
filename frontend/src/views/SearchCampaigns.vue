<template>
  <div class="container">
    <input
      class="form-control"
      type="text"
      v-model="searchTerm"
      placeholder="Enter campaign name"
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
    <button @click="searchCampaigns" class="btn btn-primary">Search</button>
    <br />
    <br />

    <div v-if="loading">Loading...</div>
    <div v-if="!loading && error">
      <p>{{ error }}</p>
    </div>
    <div v-if="!loading && !error">
      <h2>Search Results:</h2>
      <div v-if="hasCampaigns">
        <h3>All Campaigns</h3>
      </div>
      <div v-else>
        <p>No campaigns found matching your search criteria.</p>
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
      campaigns: [],
      loading: false,
      error: null,
    };
  },
  computed: {
    hasCampaigns() {
      return this.campaigns.length > 0;
    },
  },
  async created() {
    await this.fetchCategories();
    await this.fetchCampaigns();
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
    async fetchCampaigns() {
      this.loading = true;
      this.error = null;

      try {
        let url = "http://localhost:5000/search_campaigns";
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
          throw new Error("Failed to fetch campaigns.");
        }

        const data = await response.json();
        this.campaigns = data.campaigns;
      } catch (error) {
        this.error = "An error occurred while fetching campaigns.";
      }

      this.loading = false;
    },
    searchCampaigns() {
      this.fetchCampaigns();
    },
  },
};
</script>
