<template>
    <div>
        <h1>Contact Detail</h1>
        <template v-if="contact">
            <h2>{{ contact.lname }}, {{ contact.fname }}</h2>
            <p>
                Date of Birth: {{ contact.dob }}
            </p>
            <h3>Emails</h3>
            <ul>
                <li v-for="email in contact.emails" :key="email.id">
                    {{ email.email }}
                </li>
            </ul>
        </template>
        {{ contact }}
    </div>
</template>

<script>
 export default {
     props: {
         id: String
     },
     data() {
         return {
             contact: {}
         };
     },
     mounted() {
         this.getContact();
     },
     methods: {
         async getContact() {
             try {
                 const request = await fetch(`http://localhost:5000/api/contacts/${this.id}`);
                 const response = await request.json();
                 this.contact = response;
             }
             catch (error) {
                 console.log(error);
             }
         }
     }
 }
</script>
