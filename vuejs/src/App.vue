<template>
  <div id="app">
      <router-view></router-view>
  </div>
</template>

<script>
 export default {
     name: 'app',
     /*
     mounted() {
         this.$store.commit('setGlobalAlertComponent', this.$refs.alert);
     }
     */
 }
</script>

<style scoped>
 #app {
     width:100%;
     max-width: 1024px;
     margin: 0 auto;
 }
</style>
