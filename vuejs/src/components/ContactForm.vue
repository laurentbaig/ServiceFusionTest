<template>
    <div>
        <div class="form-group">
            <label class="form-label"
                   for="first"
            >First Name</label>
            <input class="form-input" id="first" type="text"
                   placeholder="First Name"
                   v-model="fname"
                   @change="update"
            >
        </div>
        <div class="form-group">
            <label class="form-label" for="last">Last Name</label>
            <input class="form-input" id="last" type="text"
                   placeholder="Last Name"
                   v-model="lname"
                   @change="update"
            >
        </div>
        <date-picker title="Date of Birth"
                     v-model="dob"
        ></date-picker>

        <div class="form-group">
            <label class="form-label"
                   for="email"
            >Email</label>
            <input class="form-input" id="email" type="email"
                   placeholder="name@place.com"
                   v-model="email"
                   @change="update"
            >
        </div>

        <div class="form-group">
            <label class="form-label"
                   for="phone"
            >Phone</label>
            <input class="form-input" id="email" type="tel"
                   placeholder="111-222-3333"
                   v-model="phone"
                   @change="update"
            >
        </div>
    </div>
</template>

<script>
 import DatePicker from './DatePicker.vue';

 export default {
     components: {
         DatePicker
     },
     props: {
         value: {
             type: Object,
             default: () => ({
                 id: null,
                 fname: '',
                 lname: '',
                 dob: new Date(),
                 email: '',
                 phone: ''
             })
         }
     },
     data() {
         return {
             fname: '',
             lname: '',
             dob: new Date(),
             email: '',
             phone: ''
         };
     },
     methods: {
         update() {
             let base = {
                 fname: this.fname,
                 lname: this.lname,
                 dob: this.dob,
                 email: this.email,
                 phone: this.phone
             };
             this.$emit('input', base);
         },
     }
 }
</script>
