export default {
  data() {
    return {
      user: null,
      role: null,
      id: null,
      logged_in: false,
    };
  },
  async created() {
    await this.checklogin();
  },
  methods: {
    async checklogin() {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) {
        this.role = null;
        this.logged_in = false;
        console.log("not logged in");
        return;
      }
      try {
        this.user = await this.getUser(access_token);
        this.id = this.user.id;
        this.logged_in = true;
        console.log("logged_in");
        if (this.user.role == "admin") {
          this.role = "admin";
        }
        if (this.user.role == "influencer") {
          this.role = "influencer";
        }
        if (this.user.role == "sponsor") {
          this.role = "sponsor";
        }
      } catch (error) {
        console.error("error fetching user info", error);
        this.logged_in = false;
      }
    },
    async getUser(access_token) {
      console.log(access_token);
      const response = await fetch("http://localhost:5000/get_user", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log(response.headers);
      if (response.status === 401) {
        this.logged_in = false;
        return null;
      }
      return await response.json();
    },
    logout() {
      localStorage.removeItem("access_token");
      this.$router.push("/");
      this.logged_in = false;
      console.log("logged_out");
    },
  },
};
