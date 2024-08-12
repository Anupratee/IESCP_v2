<template>
  <NavBar />
  <h2>Register Sponsor</h2>
  <div class="container">
    <form @submit.prevent="signup">
      <label for="email" class="form-label">Email</label>
      <input
        type="email"
        id="email"
        class="form-control"
        v-model="email"
        required
      />
      <br />
      <label for="name" class="form-label">Name</label>
      <input
        type="text"
        id="name"
        class="form-control"
        v-model="name"
        required
      />
      <br />
      <label for="location" class="form-label">Location</label>
      <select id="location" class="form-control" v-model="location" required>
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
      <label for="industry" class="form-label">Industry</label>
      <input
        type="text"
        id="industry"
        class="form-control"
        v-model="industry"
        required
      />
      <br />
      <label for="password" class="form-label">Password</label>
      <input
        type="password"
        id="password"
        class="form-control"
        v-model="password"
        required
      />
      <br />
      <button type="submit" class="btn btn-outline-dark">Register</button>
    </form>
  </div>
  <br />
  <div>
    <p>Already have an account? <router-link to="/">Login</router-link></p>
    <p>
      Want to be an influencer?
      <router-link to="/register-influencer">Register</router-link>
    </p>
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
      name: "",
      email: "",
      location: "",
      industry: "",
      password: "",
    };
  },
  methods: {
    async signup() {
      const formdata = {
        name: this.name,
        email: this.email,
        location: this.location,
        industry: this.industry,
        password: this.password,
      };
      try {
        const response = await fetch("http://localhost:5000/register_sponsor", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        });
        console.log(formdata);
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push("/");
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Registration error:", error);
        alert("An error occurred while attemping to register");
      }
    },
  },
};
</script>
