<template>
  <div><h2>Profile Page</h2></div>
  {{ name }}
</template>

<script>
export default {
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
          this.update_name = userData.update_name;
          this.role = userData.role;
          this.image = userData.image;
          this.description = userData.description;
          this.update_description = userData.description;
          this.location = userData.location;
          this.approved = sponsorData.is_approved;
          this.industry = sponsorData.industry;
          this.update_industry = sponsorData.industry;
          console.log(data);
        })
        .catch((error) => {
          alert(error.message);
        });
    },
  },
};
</script>
