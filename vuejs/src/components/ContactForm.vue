<template>
    <div>
        <div class="form-group">
            <label class="form-label" for="first">First Name</label>
            <input class="form-input" id="first" type="text" placeholder="First Name" v-model="fname">
        </div>
        <div class="form-group">
            <label class="form-label" for="last">Last Name</label>
            <input class="form-input" id="last" type="text" placeholder="Last Name" v-model="lname">
        </div>
        <date-picker title="Date of Birth"></date-picker>
    </div>
</template>

<script>
 import DatePicker from './DatePicker.vue';

 export default {
     components: {
         DatePicker
     },
     props: {
     },
     data() {
         return {
             fname: '',
             lname: '',
             dob: ''
         };
     }
 }
</script>
