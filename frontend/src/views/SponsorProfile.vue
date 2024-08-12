<template>
  <NavBar />
  <div class="profile-container">
    <div class="profile-header">
      <img v-if="image" :src="image" alt="Profile Image" />
      <div v-else class="placeholder-image">No Image</div>
      <br />
      <br />
      <h1>
        <b>{{ name }}</b>
      </h1>
      <p>{{ role }}</p>
    </div>
    <div class="profile-details">
      <p><strong>Email:</strong> {{ email }}</p>
      <p><strong>Description:</strong> {{ description }}</p>
      <p><strong>Location:</strong> {{ location }}</p>
      <p><strong>Approved:</strong> {{ approved }}</p>
      <p><strong>Industry:</strong> {{ industry }}</p>
    </div>
  </div>
  <br />
  <div class="container">
    <h3>Update Profile</h3>
    <br />
    <form @submit.prevent="updateProfile" enctype="multipart/form-data">
      <label for="update_name" class="form-label">Name</label>
      <input
        type="text"
        class="form-control"
        id="update_name"
        v-model="update_name"
        required
      />
      <br />
      <label for="update_description" class="form-label">Description</label>
      <textarea
        class="form-control"
        id="update_description"
        rows="6"
        v-model="update_description"
      ></textarea>
      <br />
      <label for="location" class="form-label">Location</label>
      <select
        id="location"
        class="form-control"
        v-model="update_location"
        required
      >
        <option value="" disabled selected>Select a state</option>
        <option value="Andhra Pradesh">Andhra Pradesh</option>
        <option value="Arunachal Pradesh">Arunachal Pradesh</option>
        <option value="Assam">Assam</option>
        <option value="Bihar">Bihar</option>
        <option value="Chhattisgarh">Chhattisgarh</option>
        <option value="Goa">Goa</option>
        <option value="Gujarat">Gujarat</option>
        <option value="Haryana">Haryana</option>
        <option value="Himachal Pradesh">Himachal Pradesh</option>
        <option value="Jharkhand">Jharkhand</option>
        <option value="Karnataka">Karnataka</option>
        <option value="Kerala">Kerala</option>
        <option value="Madhya Pradesh">Madhya Pradesh</option>
        <option value="Maharashtra">Maharashtra</option>
        <option value="Manipur">Manipur</option>
        <option value="Meghalaya">Meghalaya</option>
        <option value="Mizoram">Mizoram</option>
        <option value="Nagaland">Nagaland</option>
        <option value="Odisha">Odisha</option>
        <option value="Punjab">Punjab</option>
        <option value="Rajasthan">Rajasthan</option>
        <option value="Sikkim">Sikkim</option>
        <option value="Tamil Nadu">Tamil Nadu</option>
        <option value="Telangana">Telangana</option>
        <option value="Tripura">Tripura</option>
        <option value="Uttar Pradesh">Uttar Pradesh</option>
        <option value="Uttarakhand">Uttarakhand</option>
        <option value="West Bengal">West Bengal</option>
        <option value="Andaman and Nicobar Islands">
          Andaman and Nicobar Islands
        </option>
        <option value="Chandigarh">Chandigarh</option>
        <option value="Dadra and Nagar Haveli and Daman and Diu">
          Dadra and Nagar Haveli and Daman and Diu
        </option>
        <option value="Delhi">Delhi</option>
        <option value="Lakshadweep">Lakshadweep</option>
        <option value="Puducherry">Puducherry</option>
      </select>
      <br />
      <label for="update_industry" class="form-label">Industry</label>
      <input
        type="text"
        class="form-control"
        id="update_industry"
        v-model="update_industry"
      />
      <br />
      <label for="update_image" class="form-label">Profile Image</label>
      <input
        type="file"
        class="form-control"
        id="update_image"
        @change="uploadImage"
        ref="file"
      />
      <br />
      <br />
      <button type="submit" class="btn btn-outline-dark">Update Profile</button>
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
      user_id: null,
      email: "",
      name: "",
      role: "",
      image: null,
      description: "",
      location: "",
      approved: null,
      industry: "",
      update_email: "",
      update_name: "",
      update_image: null,
      update_description: "",
      update_location: "",
      update_industry: "",
    };
  },
  created() {
    this.user_id = this.$route.params.user_id;
    this.fetchSponsor();
  },
  methods: {
    fetchSponsor() {
      fetch(`http://localhost:5000/sponsor/${this.user_id}`, {
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
          const userData = data.user;
          const sponsorData = data.sponsor;
          this.email = userData.email;
          this.update_email = userData.email;
          this.name = userData.name;
          this.update_name = userData.name;
          this.role = userData.role;
          this.image = userData.image;
          this.description = userData.description;
          this.update_description = userData.description;
          this.location = userData.location;
          this.update_location = userData.location;
          this.approved = sponsorData.is_approved;
          this.industry = sponsorData.industry;
          this.update_industry = sponsorData.industry;
          console.log(data);
        })
        .catch((error) => {
          alert(error.message);
        });
    },
    uploadImage() {
      this.update_image = this.$refs.file.files[0];
    },
    updateProfile() {
      const formData = new FormData();
      formData.append("update_name", this.update_name);
      formData.append("update_description", this.update_description);
      formData.append("update_location", this.update_location);
      formData.append("update_industry", this.update_industry);
      formData.append("update_image", this.update_image);
      for (let pair of Array.from(formData.entries())) {
        console.log(pair[0] + ", " + pair[1]);
      }
      fetch(`http://localhost:5000/update_sponsor/${this.user_id}`, {
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
              throw new Error("Error updating profile");
            }
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Profile updated successfully!");
          this.fetchSponsor();
          (this.update_name = ""),
            (this.update_description = ""),
            (this.update_location = ""),
            (this.update_industry = ""),
            (this.update_image = null),
            this.$router.push(`/sponsors/profile/${this.user_id}`);
        })
        .catch((error) => {
          (this.update_name = ""),
            (this.update_description = ""),
            (this.update_location = ""),
            (this.update_industry = ""),
            (this.update_image = null),
            alert(error.message);
        });
    },
  },
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

.profile-container {
  max-width: 800px;
  margin: 50px auto;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
}

.profile-header img {
  border-radius: 50%;
  width: 150px;
  height: 150px;
}

.placeholder-image {
  width: 150px;
  height: 150px;
  background-color: #ccc;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.profile-details {
  margin-top: 20px;
}

.profile-details p {
  margin: 10px 0;
}
</style>
