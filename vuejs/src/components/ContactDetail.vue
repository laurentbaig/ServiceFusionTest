<template>
    <div class="container">
        <router-link to="/">Back to list</router-link>
        <h1>Contact Detail</h1>
        <template v-if="contact">
            <div class="card">
                <div class="card-body">
                    <h2>{{ contact.lname }}, {{ contact.fname }}</h2>
                    <div>
                        <p>
                            Date of Birth: {{ contact.dob }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="card space-top">
                <div class="card-body">
                    <h3>
                        Emails
                        <button class="btn btn-primary float-right"
                                @click="onCreateNewEmail"
                        >
                            <i class="icon icon-plus"></i>
                        </button>
                    </h3>
                    <div>
                        <div v-for="(email,index) in emails"
                             class="columns py-1 px-2"
                             :key="email.id"
                             :class="{odd: index % 2}"
                        >
                            <div class="col-11">
                                <editable-object-field :value="emails[index]"
                                                       field="email"
                                                       @input="onEmailUpdated(emails[index])"
                                ></editable-object-field>
                            </div>
                            <div v-if="index > 0" class="col-1 text-right">
                                <button class="btn btn-sm btn-error"
                                        @click="deleteEmailClicked(email)"
                                >
                                    <i class="icon icon-cross"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card space-top">
                <div class="card-body">

                    <h3>
                        Phones
                        <button class="btn btn-primary float-right"
                                @click="onCreateNewPhone"
                        >
                            <i class="icon icon-plus"></i>
                        </button>
                    </h3>
                    <div v-if="phones.length > 0">
                        <div v-for="(phone,index) in phones"
                             class="columns py-1 px-2"
                             :key="phone.id"
                             :class="{odd: index % 2}"
                        >
                            <div class="col-11">
                                <editable-object-field v-model="phones[index]"
                                                       field="phone"
                                                       @input="onPhoneUpdated(phones[index])"
                                ></editable-object-field>
                            </div>
                            <div v-if="index > 0" class="col-1 text-right">
                                <button class="btn btn-sm btn-error"
                                        @click="deletePhoneClicked(phone)"
                                >
                                    <i class="icon icon-cross"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div v-else class="empty">
                        <div class="empty-icon">
                            <i class="icon icon-people"></i>
                        </div>
                        <p class="empty-title h5">You have no phones for this contact</p>
                        <p class="empty-subtitle">Click the button to create a phoone.</p>
                        <div class="empty-action">
                            <button class="btn btn-primary"
                                    @click="onCreateNewPhone"
                            >Add a phone</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="card space-top">
                <div class="card-body">

                    <h3>
                        Addresses
                        <button class="btn btn-primary float-right"
                                @click="onCreateNewAddress"
                        >
                            <i class="icon icon-plus"></i>
                        </button>
                    </h3>
                    <div v-if="addresses.length > 0">
                        <div v-for="(address,index) in addresses"
                             class="columns py-1 px-2"
                             :key="address.id"
                             :class="{odd: index % 2}"
                        >
                            <div class="col-11">
                                <editable-object-field v-model="addresses[index]"
                                                       field="full_address"
                                                       @input="onAddressUpdated(addresses[index])"
                                ></editable-object-field>
                            </div>
                            <div class="col-1 text-right">
                                <button class="btn btn-sm btn-error"
                                        @click="deleteAddressClicked(address)"
                                >
                                    <i class="icon icon-cross"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div v-else class="empty">
                        <div class="empty-icon">
                            <i class="icon icon-location"></i>
                        </div>
                        <p class="empty-title h5">You have no addresses</p>
                        <p class="empty-subtitle">Click the button to create an address.</p>
                        <div class="empty-action">
                            <button class="btn btn-primary"
                                    @click="onCreateNewAddress"
                            >Add an address</button>
                        </div>
                    </div>
                </div>
            </div>
        </template>

        <spectre-modal title="New Email" ref="emailModal">
            <div class="form-group">
                <label>Email</label>
                <input class="form-input" type="email" v-model="newEmail">
            </div>
            <template v-slot:footer>
                <button class="btn btn-primary"
                        @click="onSaveNewEmail"
                >Create</button>
            </template>
        </spectre-modal>

        <spectre-modal title="New Phone" ref="phoneModal">
            <div class="form-group">
                <label>Phone</label>
                <input class="form-input" type="tel" v-model="newPhone">
            </div>
            <template v-slot:footer>
                <button class="btn btn-primary"
                        @click="onSaveNewPhone"
                >Create</button>
            </template>
        </spectre-modal>

        <spectre-modal title="New Address" ref="addressModal">
            <div class="form-group">
                <label>Address</label>
                <input class="form-input" type="text" v-model="newAddress">
            </div>
            <template v-slot:footer>
                <button class="btn btn-primary"
                        @click="onSaveNewAddress"
                >Create</button>
            </template>
        </spectre-modal>

        <alert ref="alert" :autohide="true"></alert>

    </div>
</template>

<style scoped>
 .odd {
     background-color: #eee;
 }
 .space-top {
     margin-top: 20px;
 }
</style>

<script>
 import axios from 'axios';
 import Alert from './Alert.vue';
 import EditableObjectField from './EditableObjectField.vue';
 import SpectreModal from './SpectreModal.vue';
 
 export default {
     components: {
         Alert,
         EditableObjectField,
         SpectreModal
     },
     props: {
         id: String
     },
     data() {
         return {
             contact: {},
             addresses: [],
             emails: [],
             phones: [],
             newEmail: '',
             newPhone: '',
             newAddress: ''
         };
     },
     mounted() {
         this.getContact();
         this.getEmails();
         this.getPhones();
         this.getAddresses();
     },
     methods: {
         getContact() {
             axios.get(`/contacts/${this.id}`)
                  .then(response => {
                      this.contact = response.data;
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         getEmails() {
             axios.get(`/contacts/${this.id}/emails`)
                  .then(response => {
                      this.emails = response.data;
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         getPhones() {
             axios.get(`/contacts/${this.id}/phones`)
                  .then(response => {
                      this.phones = response.data;
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         getAddresses() {
             axios.get(`/contacts/${this.id}/addresses`)
                  .then(response => {
                      this.addresses = response.data;
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         deleteAddressClicked(phone) {
             if (window.confirm(`Are you sure you wish to delete ${phone.phone}`)) {
                 axios.delete(`/addresses/${phone.id}`)
                      .then(response => {
                          this.$refs.alert.success('Address successfully delete');
                          this.getAddresses();
                      })
                      .catch(err => {
                          console.log(err);
                      });
             }
         },
         deleteEmailClicked(email) {
             if (window.confirm(`Are you sure you wish to delete ${email.email}`)) {
                 axios.delete(`/emails/${email.id}`)
                      .then(response => {
                          this.$refs.alert.success('Email successfully delete');
                          this.getEmails();
                      })
                      .catch(err => {
                          console.log(err);
                      });
             }
         },
         deletePhoneClicked(phone) {
             if (window.confirm(`Are you sure you wish to delete ${phone.phone}`)) {
                 axios.delete(`/phones/${phone.id}`)
                      .then(response => {
                          this.$refs.alert.success('Phone successfully delete');
                          this.getPhones();
                      })
                      .catch(err => {
                          console.log(err);
                      });
             }
         },
         onAddressUpdated(address) {
             axios.put(`/addresses/${address.id}`, address)
                  .then(response => {
                      this.$refs.alert.success('Address updated');
                      this.getAddresses();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onEmailUpdated(email) {
             axios.put(`/emails/${email.id}`, email)
                  .then(response => {
                      this.$refs.alert.success('Email updated');
                      this.getEmails();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onPhoneUpdated(phone) {
             axios.put(`/phones/${phone.id}`, phone)
                  .then(response => {
                      this.$refs.alert.success('Phone updated');
                      this.getPhones();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onCreateNewAddress() {
             this.newAddress = '';
             this.$refs.addressModal.open();
         },
         onCreateNewEmail() {
             this.newEmail = '';
             this.$refs.emailModal.open();
         },
         onCreateNewPhone() {
             this.newPhone = '';
             this.$refs.phoneModal.open();
         },
         onSaveNewAddress() {
             axios.post(`/contacts/${this.contact.id}/addresses`, {
                 address: this.newAddress
             })
                  .then(response => {
                      this.$refs.addressModal.close();
                      this.getAddresses();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onSaveNewEmail() {
             axios.post(`/contacts/${this.contact.id}/emails`, {
                 email: this.newEmail
             })
                  .then(response => {
                      this.$refs.emailModal.close();
                      this.getEmails();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onSaveNewPhone() {
             axios.post(`/contacts/${this.contact.id}/phones`, {
                 phone: this.newPhone
             })
                  .then(response => {
                      this.$refs.phoneModal.close();
                      this.getPhones();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
     }
 }
</script>
