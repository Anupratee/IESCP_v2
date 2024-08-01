import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RegisterInfluencer from "../views/RegisterInfluencer.vue";
import RegisterSponsor from "../views/RegisterSponsor.vue";
import SponsorHome from "../views/SponsorHome.vue";
import SponsorProfile from "../views/SponsorProfile.vue";
import CampaignPage from "../views/CampaignPage.vue";
import AdPage from "../views/AdPage.vue";
import InfluencerHome from "../views/InfluencerHome.vue";
import InfluencerCampaign from "../views/InfluencerCampaign.vue";
import InfluencerProfile from "@/views/InfluencerProfile.vue";
import AdminHome from "../views/AdminHome.vue";
import ApproveSponsors from "../views/ApproveSponsors.vue";
import AdminCampaigns from "@/views/AdminCampaigns.vue";
import AdminAds from "../views/AdminAds.vue";

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
  {
    path: "/influencer-home",
    name: "influencer_home",
    component: InfluencerHome,
  },
  {
    path: "/influencers/profile/:user_id",
    name: "influencers_profile",
    component: InfluencerProfile,
  },
  {
    path: "/influencer-home/campaigns/:campaign_id",
    name: "influencer-home_home",
    component: InfluencerCampaign,
  },
  {
    path: "/admin-home",
    name: "admin_home",
    component: AdminHome,
  },
  {
    path: "/admin-home/approve-sponsors",
    name: "approve-sponsors",
    component: ApproveSponsors,
  },
  {
    path: "/admin-home/campaigns",
    name: "admin_campaigns",
    component: AdminCampaigns,
  },
  {
    path: "/admin-home/ads",
    name: "admin_ads",
    component: AdminAds,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
