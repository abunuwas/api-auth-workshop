<template>
  <div id="nav" style="height: 150px;">
    <nav class="navbar navbar-expand-lg navbar-light" style="background: #8b76b0; padding-left: 20px;">
      <div class="navbar-brand" style="color: #fab246;"><h4>PyJobs.works</h4></div>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <a class="navbar-brand menu" v-if="!$auth.isAuthenticated.value" @click="login">Register</a>
        <a class="navbar-brand menu" v-if="!$auth.isAuthenticated.value" @click="login">Login</a>
        <a class="navbar-brand menu" @click="logout" v-if="$auth.isAuthenticated.value">Logout</a>
      </div>
    </nav>
  </div>

  <div class="container-fluid" style="padding: 0 40px 40px;">

    <div>Authentication details</div>
    <div>Your token <span><img :src="copyIcon" alt="copy-auth-token" style="width: 1%; min-width: 15px;" class="copy-icon" @click="copyToken"></span></div>
    <div class="token-area" @click="copyToken">{{ this.authToken }}</div>

    <div class="row" style="margin-top: 30px;">
      <div class="col-11" v-for="job in jobs" :key="job.id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ job.title }}</h5>
            <div class="card-text">
              <div><p>{{ job.hirer }}</p></div>
              <div>
                <p><span><i class="fa-solid fa-location-dot"></i></span> {{ job.location.city }}, {{ job.location.country }}
                  <span><i class="fa-regular fa-calendar-days"></i></span> {{ Math.ceil(today.diff(job.dateListed, 'days').days) }} days ago</p>
              </div>
              <div>
                <p><span><i class="fa-solid fa-money-bills"></i></span> US${{ job.rate.amount }} per {{ job.rate.amountPerTime }}</p>
              </div>
              <div>
                <p>{{ job.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>

  <div id="bottom" class="container-fluid" style="padding-top: 0; min-height: 80px;">
    <div style="padding-top: 10px;">
      <a href="https://microapis.io" target="_blank"><img :src="microapis" style="width: 1.8rem; margin: 10px" alt="microapis.io"></a>
      <a href="https://github.com/abunuwas/microservice-apis" target="_blank"><img :src="github" style="width: 2rem; margin: 10px" alt="github"></a>
      <a href="https://twitter.com/microapis" target="_blank"><img :src="twitter" style="width: 2rem; margin: 10px" alt="twitter"></a>
      <a href="https://www.reddit.com/r/microapis/" target="_blank"><img :src="reddit" style="width: 2rem; margin: 10px" alt="reddit"></a>
      <a href="https://www.youtube.com/channel/UCtrp0AWmJJXb50zb12XxTlQ" target="_blank"><img :src="youtube" style="width: 2.5rem; margin: 10px" alt="reddit"></a>
    </div>
  </div>
</template>

<script lang="ts">
import axios from "axios";
import { defineComponent } from "vue";
import { DateTime } from "luxon";

interface appData {
  // products: any,
  // basket: Array<any>,
  jobs: Array<any>,
  // selectedSize: any,
  authToken: null | string
}

export default defineComponent({
  data() {
    return {
      // basket: [],
      jobs: [],
      // selectedSize: null,
      microapis: require('../public/microapis.png'),
      github: require('../public/github.png'),
      twitter: require('../public/twitter.png'),
      reddit: require('../public/reddit.png'),
      youtube: require('../public/youtube.png'),
      shoppingCartIcon: require('../public/shopping-cart.png'),
      copyIcon: require('../public/copy.png'),
      authToken: null,
      today: DateTime.now()
    } as appData
  },
  async mounted() {
    // @ts-ignore
    console.log(this.$auth.isAuthenticated.value)
    // @ts-ignore
    this.authToken = await this.$auth.getTokenSilently()
    // @ts-ignore
    console.log(await this.$auth.getIdTokenClaims())
    // @ts-ignore
    console.log(this.$auth.user.value)
    // @ts-ignore
    this.jobs = await this.getJobs();
  },
  methods: {
    login() {
      // @ts-ignore
      this.$auth.loginWithRedirect();
    },
    logout() {
      // @ts-ignore
      this.$auth.logout({
        returnTo: window.location.origin
      });
    },
    // addItemToBasket(itemToAdd: any) {
    //   // @ts-ignore
    //   const itemToAddId = `${itemToAdd.id}-${itemToAdd.selectedSize.size}`
    //   if (!this.basket.map(addedItem => addedItem.id).includes(itemToAddId)) {
    //     this.basket.push({
    //       id: itemToAddId,
    //       product: itemToAdd.name,
    //       size: itemToAdd.selectedSize.size,
    //       quantity: 1
    //     })
    //   } else {
    //     const item = this.basket.filter(item => item.id === itemToAddId)[0]
    //     item.quantity++
    //   }
    // },
    // deleteItem(itemToDelete: any) {
    //   this.basket.splice(this.basket.indexOf(itemToDelete), 1)
    // },
    // async checkout() {
    //   const payload = this.basket.map(item => {
    //     return {
    //       product: item.product,
    //       size: item.size,
    //       quantity: item.quantity
    //     }
    //   })
    //   try {
    //     const response = await axios.post(
    //       `${process.env.VUE_APP_BASE_URL}/jobs`,
    //       {orjobsder: payload},
    //       {headers: {Authorization: `Bearer ${this.authToken}`}}
    //     )
    //     this.jobs.push(response.data)
    //   } catch (error) {
    //     console.log(error.response)
    //   }
    // },
    async getJobs() {
      try {
        const response = await axios.get(
          `${process.env.VUE_APP_BASE_URL}/jobs`,
          {headers: {Authorization: `Bearer ${this.authToken}`}}
        )
        console.log(response)
        // @ts-ignore
        return response.data.jobs.map(job => {
          console.log(job.dateListed)
          console.log(DateTime.fromISO(job.dateListed))
          return {
            ...job,
            dateListed: DateTime.fromISO(job.dateListed),
            liveUntil: DateTime.fromISO(job.liveUntil),
          }
        })
      } catch (error) {
        console.log(error.response)
      }
    } ,
    copyToken() {
      // @ts-ignore
      navigator.clipboard.writeText(this.authToken);
    }
  }
})
</script>
<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}

#bottom {
  width: 100%;
  background-color: #2c3e50;
  color: azure;
  text-align: center;
  margin-top: 100px;
  bottom: 0;
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
}

#logo,
.menu:hover {
  cursor: pointer
}

.navbar-brand {
  width: 150px;
  height: 100%;
  padding-right: 20px;
}

.navbar-toggler{
  border: 1px solid white !important;
  color: white;
}

.nav-item a:hover {
  background-color: #e8e8e8;
}

.delete-item-button:hover {
  cursor: pointer;
}

.copy-icon:hover {
  cursor: pointer;
}

.token-area {
  max-width: 90%;
  overflow-wrap: break-word;
  padding: 10px;
  background-color: #f2f2f2;
  border-radius: 20px;
  margin-top: 5px;
}

.token-area:hover {
  cursor: pointer;
}
</style>
