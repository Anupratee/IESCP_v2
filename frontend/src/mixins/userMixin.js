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
        const user = await this.getUser(access_token);
        if (!user) {
          this.logged_in = false;
          return;
        }
        this.user = user;
        this.id = user.id;
        this.logged_in = true;
        this.role = user.role;
        console.log("logged_in");
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
      this.role = null;
      this.id = null;
      console.log("logged_out");
    },
  },
};
