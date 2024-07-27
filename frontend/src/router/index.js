import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RegisterInfluencer from "../views/RegisterInfluencer.vue";
import RegisterSponsor from "../views/RegisterSponsor.vue";
import SponsorHome from "../views/SponsorHome.vue";
import CampaignPage from "../views/CampaignPage.vue";

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
    path: "/sponsor-home/campaigns/:campaign_id",
    name: "campaign_home",
    component: CampaignPage,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
