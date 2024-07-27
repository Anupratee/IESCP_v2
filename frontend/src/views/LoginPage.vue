<template>
  <div class="container">
    <h2>Login</h2>
    <br />
    <form @submit.prevent="login" class="login-form">
      <label for="email" class="form-label">Email</label>
      <input
        type="text"
        id="email"
        class="form-control"
        v-model="email"
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
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
    <br />
    <p>
      Don't have an account?
      <router-link to="/register-influencer">Sign Up</router-link>
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const formdata = {
        email: this.email,
        password: this.password,
      };
      try {
        const response = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          localStorage.setItem("access_token", data.access_token);
          const userRole = data.role;

          if (userRole === "admin") {
            this.$router.push("/admin-home");
          } else if (userRole === "influencer") {
            this.$router.push("/influencer-home");
          } else if (userRole === "sponsor") {
            this.$router.push("/sponsor-home");
          } else {
            alert("Unknown user role");
          }
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred while attempting to login");
      }
    },
  },
};
</script>
