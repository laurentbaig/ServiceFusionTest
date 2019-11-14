<template>
    <div>
        <h1>Contacts</h1>
        <div class="columns">
            <div class="col-3">
                <button class="btn btn-primary"
                        @click="onAddContactClicked"
                >
                    Add Contact
                </button>
            </div>
            <div class="col-2"></div>
            <div class="col-4">
                <div class="input-group">
                    <input type="text"
                           class="form-input"
                           v-model="searchString"
                           @input="debouncedUpdateSearchOptions"
                    >
                    <div class="dropdown dropdown-right"
                         :class="{active: isSearching}"
                    >
                        <button class="btn btn-primary input-group-btn dropdown-toggle">
                            <i class="icon icon-search"></i>
                        </button>
                        <ul class="menu">
                            <li v-for="(option, index) in searchOptions"
                                class="menu-item"
                                :key="index"
                            >
                                <router-link :to="'/contact/'+option.id">
                                    {{ option.fname }} {{ option.lname }}
                                </router-link>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-3">
                <span class="float-right">
                    {{ fromRow }} - {{ toRow }} of {{ totalRecords }}
                    <button class="btn"
                            @click="changePage(-1)"
                            :disabled="!canPageLeft"
                    ><i class="icon icon-arrow-left"></i></button>
                    <button class="btn"
                            @click="changePage(1)"
                            :disabled="!canPageRight"
                    ><i class="icon icon-arrow-right"></i></button>
                </span>
            </div>
        </div>
        <table class="table">
            <thead>
                <tr>
                    <th @click="sortBy('id')">Id<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('lname')">Last<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('fname')">First<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('dob')">DoB<i class="icon icon-resize-vert"></i></th>
                    <th>Phones</th>
                    <th>Emails</th>
                    <th>&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in contacts" :key="row.id"> <!-- @click="onRowClicked(row)"> -->
                    <td>{{ row.id }}</td>
                    <td>{{ row.lname }}</td>
                    <td>{{ row.fname }}</td>
                    <td>{{ row.dob.substring(0,10) }}</td>
                    <td>{{ firstPhone(row) }}</td>
                    <td>{{ firstEmail(row) }}
                        <div v-if="row.emails.length > 0" class="dropdown dropdown-right">
                            <a href="#" class="btn btn-link dropdown-toggle" tabindex="0" @click.stop>+</a>
                            <ul class="menu">
                                <li v-for="email in row.emails" :key="email.id">
                                    <button class="btn btn-link">
                                        {{ email.email }}
                                    </button>
                                </li>
                            </ul>
                        </div>
                    </td>
                    <td>
                        <button class="btn btn-primary"
                                @click.stop="onEditClicked(row)"
                        ><i class="icon icon-edit"></i></button>
                        &nbsp;
                        <button class="btn btn-error"
                                @click.stop="onDeleteClicked(row)"
                        ><i class="icon icon-delete"></i></button>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Modal for Adding new contact -->
        <spectre-modal :title="modalTitle"
                       ref="contactModal"
        >
            <contact-form v-model="form"></contact-form>
            <template v-slot:footer>
                <button class="btn btn-primary"
                        @click="onSaveContact"
                >{{ saveButtonText }}</button>
            </template>
        </spectre-modal>

        <!-- The alert box -->
        <alert ref="alert" :message="alertMessage" :autohide="true"></alert>
    </div>
</template>

<style scoped>
 tbody td {
     transition: all .2s ease-in-out;
 }
 tbody tr:hover td {
     background-color: #ddd;
 }
</style>

<script>
 import axios from 'axios';
 import { mapState } from 'vuex';
 import Alert from '../components/Alert.vue';
 import ContactForm from '../components/ContactForm.vue';
 import SpectreModal from '../components/SpectreModal.vue';
 import _ from 'lodash';
 
 export default {
     components: {
         Alert,
         ContactForm,
         SpectreModal
     },
     data() {
         return {
             alertMessage: '',
             contacts: [],
             form: {
                 id: 0,
                 fname: '',
                 lname: '',
                 dob: new Date(),
                 email: '',
                 phone: ''
             },
             fromRow: 1,
             isSearching: false,
             searchOptions: [],
             searchString: '',
             toRow: 10,
             totalRecords: 0,
         };
     },
     created() {
         /* create a debounced version of the search here */
         this.debouncedUpdateSearchOptions = _.debounce(() => { this.updateSearchOptions(); }, 300);
     },
     mounted() {
         this.getPage();
     },
     computed: {
         canPageLeft() {
             return this.listPage > 1;
         },
         canPageRight() {
             return this.listPage < Math.ceil(this.totalRecords / this.listPageSize);
         },
         queryParameters() {
             return `page=${this.listPage}&pagesize=${this.listPageSize}&sortby=${this.listSortField}&sortdir=${this.listSortDir}`;
         },
         modalTitle() {
             return (this.form.id > 0 ? 'Update' : 'Create') + ' Contact';
         },
         saveButtonText() {
             return this.form.id > 0 ? 'Update' : 'Create';
         },
         // computed properties on the store
         ...mapState([
             'listPage',
             'listPageSize',
             'listSortField',
             'listSortDir'
         ])
     },
     methods: {
         changePage(val) {
             this.$store.commit('setListPage', this.listPage + val);
             this.getPage();
         },
         firstEmail(row) {
             return row.emails && row.emails.length > 0 ? row.emails[0].email : '(no email)';
         },
         firstPhone(row) {
             return row.phones && row.phones.length > 0 ? row.phones[0].phone : '(no phone)';
         },
         getPage() {
             axios.get(`/contacts?${this.queryParameters}`)
                  .then(response => {
                      let payload = response.data;
                      this.contacts = payload.data;
                      this.totalRecords = payload.numberRecords;
                      this.fromRow = (payload.page-1) * payload.pagesize + 1;
                      this.toRow = payload.page * payload.pagesize;
                      this.$refs.contactModal.close();
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
         onAddContactClicked() {
             this.form.id = null;
             this.form.fname = '';
             this.form.lname = '';
             this.form.dob = new Date();
             this.form.email = '';
             this.form.phone = '';
             this.$refs.contactModal.open();
         },
         onRowClicked(row) {
             this.$router.push({ path: `/contact/${row.id}` });
         },
         onEditClicked(row) {
             this.$router.push({ path: `/contact/${row.id}` });
             /*
             this.form.id = row.id;
             this.form.fname = row.fname;
             this.form.lname = row.lname;
             this.form.dob = new Date(row.dob.length <= 10 ? row.dob+'T00:00:00Z' : row.dob);
             this.form.emails = row.emails;
             this.form.phones = row.phones;
             this.$refs.contactModal.open();
             */
         },
         onDeleteClicked(row) {
             if (window.confirm(`Are you sure you wish to delete ${row.fname} ${row.lname}?`)) {
                 axios.delete(`/contacts/${row.id}`)
                      .then(response => {
                          this.$refs.alert.success('Contact successfully deleted');
                          this.getPage();
                      })
                      .catch(err => {
                          console.log(err);
                      });
             }
         },
         async onSaveContact() {
             /*
             if (this.form.id > 0) {
                 axios.put(`/contacts/${this.form.id}`, this.form)
                      .then(response => {
                          this.$refs.alert.success('Contact successfully updated');
                          this.getPage();
                      })
                      .catch(err => {
                          console.log(err);
                      });
                 return;
             }
             */
             if (this.form.fname.length == 0 || this.form.lname.lenth == 0) {
                 this.$refs.alert.error("You must enter a first name and a last name");
                 return;
             }
             let data = await axios.post(`/contacts`, {
                 ...this.form,
                 dob: this.form.dob.toISOString()
             });
             let c = data.data;
             await Promise.all([
                 axios.post(`/contacts/${c.id}/phones`, {
                     phone: this.form.phone
                 }),
                 axios.post(`/contacts/${c.id}/emails`, {
                     email: this.form.email
                 })
             ]);
             this.$refs.alert.success('Contact successfully created');
             this.$router.push({ path: `/contact/${c.id}` });
         },
         sortBy(field) {
             if (field == this.listSortField) {
                 this.$store.commit('setListSortDir', this.listSortDir == 'asc' ? 'desc' : 'asc');
             }
             this.$store.commit('setListSortField', field);
             this.getPage();
         },
         updateSearchOptions() {
             this.isSearching = true;
             axios.get(`/contacts?search=${this.searchString}`)
                  .then(response => {
                      this.searchOptions = response.data.data;
                  })
                  .catch(err => {
                      console.log(err);
                  });
         },
     }
 }
</script>
