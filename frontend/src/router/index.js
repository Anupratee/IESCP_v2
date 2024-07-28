import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RegisterInfluencer from "../views/RegisterInfluencer.vue";
import RegisterSponsor from "../views/RegisterSponsor.vue";
import SponsorHome from "../views/SponsorHome.vue";
import SponsorProfile from "../views/SponsorProfile.vue";
import CampaignPage from "../views/CampaignPage.vue";
import AdPage from "../views/AdPage.vue";

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
  },
  {
    path: "/sponsors/profile/:user_id",
    name: "sponsor_profile",
    component: SponsorProfile,
  },
  {
    path: "/sponsor-home/campaigns/:campaign_id",
    name: "campaign_home",
    component: CampaignPage,
  },
  {
    path: "/sponsor-home/ads/:ad_id",
    name: "ad_page",
    component: AdPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
