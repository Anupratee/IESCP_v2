import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RegisterInfluencer from "../views/RegisterInfluencer.vue";
import RegisterSponsor from "../views/RegisterSponsor.vue";
import SponsorHome from "../views/SponsorHome.vue";
import SponsorProfile from "../views/SponsorProfile.vue";
import SponsorRequests from "../views/SponsorRequests.vue";
import SearchInfluencers from "@/views/SearchInfluencers.vue";
import CampaignPage from "../views/CampaignPage.vue";
import AdPage from "../views/AdPage.vue";
import InfluencerHome from "../views/InfluencerHome.vue";
import InfluencerCampaign from "../views/InfluencerCampaign.vue";
import InfluencerProfile from "@/views/InfluencerProfile.vue";
import InfluencerAds from "../views/InfluencerAds.vue";
import SearchCampaigns from "../views/SearchCampaigns.vue";
import AdminHome from "../views/AdminHome.vue";
import ApproveSponsors from "../views/ApproveSponsors.vue";
import AdminCampaigns from "@/views/AdminCampaigns.vue";
import AdminCampaign from "@/views/AdminCampaign.vue";
import AdminAds from "../views/AdminAds.vue";

function checkLoggedin(to, from, next) {
  const access_token = localStorage.getItem("access_token");
  if (!access_token) {
    console.log("Access token not found. Redirecting to /login");
    next("/");
  } else {
    console.log("Access token found. Proceeding to route");
    next();
  }
}

function checkAdmin(to, from, next) {
  const access_token = localStorage.getItem("access_token");
  if (!access_token) {
    next("/");
  } else {
    fetch("http://localhost:5000/get_user", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch user data");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);
        if (data.role === "admin") {
          next();
        } else {
          next("/");
        }
      })
      .catch((error) => {
        console.error("Error occurred while fetching user data", error);
        next("/");
      });
  }
}

const routes = [
  {
    path: "/",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/register-influencer",
    name: "register_influencer",
    component: RegisterInfluencer,
  },
  {
    path: "/register-sponsor",
    name: "register_sponsor",
    component: RegisterSponsor,
  },
  {
    path: "/sponsor-home",
    name: "sponsor_home",
    component: SponsorHome,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/sponsors/profile/:user_id",
    name: "sponsor_profile",
    component: SponsorProfile,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/sponsor-home/requests",
    name: "sponsor_requests",
    component: SponsorRequests,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/sponsor-home/search",
    name: "influencer_search",
    component: SearchInfluencers,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/sponsor-home/campaigns/:campaign_id",
    name: "campaign_home",
    component: CampaignPage,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/sponsor-home/ads/:ad_id",
    name: "ad_page",
    component: AdPage,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/influencer-home",
    name: "influencer_home",
    component: InfluencerHome,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/influencer-home/my-ads",
    name: "influencer_ads",
    component: InfluencerAds,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/influencer-home/search",
    name: "campaign_search",
    component: SearchCampaigns,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/influencers/profile/:user_id",
    name: "influencers_profile",
    component: InfluencerProfile,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/influencer-home/campaigns/:campaign_id",
    name: "influencer-home_home",
    component: InfluencerCampaign,
    meta: { requiresAuth: true },
    beforeEnter: checkLoggedin,
  },
  {
    path: "/admin-home",
    name: "admin_home",
    component: AdminHome,
    meta: { requiresAuth: true },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin-home/approve-sponsors",
    name: "approve-sponsors",
    component: ApproveSponsors,
    meta: { requiresAuth: true },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin-home/campaigns",
    name: "admin_campaigns",
    component: AdminCampaigns,
    meta: { requiresAuth: true },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin-home/campaigns/:campaign_id",
    name: "admin_campaign",
    component: AdminCampaign,
    meta: { requiresAuth: true },
    beforeEnter: checkAdmin,
  },
  {
    path: "/admin-home/ads",
    name: "admin_ads",
    component: AdminAds,
    meta: { requiresAuth: true },
    beforeEnter: checkAdmin,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
