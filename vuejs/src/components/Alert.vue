<template>
    <div v-if="visible" class="toast toast-alert" :class="toastClass">
        <button class="btn btn-clear float-right" @click="close"></button>
        {{ msg }}
    </div>
</template>

<style scoped>
 .toast-alert {
     position: fixed;
     top: 10px;
     left: 50%;
     max-width: 60%;
     transform: translateX(-50%);
     z-index: 1000;
 }
</style>

<script>
 export default {
     props: {
         autohide: {
             type: Boolean,
             default: false
         },
     },
     data() {
         return {
             visible: false,
             msg: 'Hello',
             color: ''
         };
     },
     watch: {
         message: function(to, from) {
             this.msg = to;
         }
     },
     computed: {
         toastClass() {
             if (this.color.length > 0) {
                 let value = {};
                 value[`toast-${this.color}`] = true;
                 return value;
             }
             return {};
         }
     },
     methods: {
         close() {
             this.visible = false;
         },
         open() {
             this.visible = true;
             if (this.autohide) {
                 setTimeout(() => {
                     this.visible = false;
                 }, 5000);
             }
         },
         info(msg) {
             this.msg = msg;
             this.color = '';
             this.open();
         },
         error(msg) {
             this.msg = msg;
             this.color = 'error';
             this.open();
         },
         success(msg) {
             this.msg = msg;
             this.color = 'success';
             this.open();
         }
     }
 }
</script>
