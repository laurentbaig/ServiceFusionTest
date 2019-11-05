<template>
    <div>
        <h1>Contacts</h1>
        <div>
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
        <table class="table">
            <thead>
                <tr>
                    <th @click="sortBy('id')">Id<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('lname')">Last<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('fname')">First<i class="icon icon-resize-vert"></i></th>
                    <th @click="sortBy('dob')">DoB<i class="icon icon-resize-vert"></i></th>
                    <th>Emails</th>
                    <th>&nbsp;</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="row in contacts" :key="row.id">
                    <td>{{ row.id }}</td>
                    <td>{{ row.lname }}</td>
                    <td>{{ row.fname }}</td>
                    <td>{{ row.dob }}</td>
                    <td>{{ firstEmail(row) }}
                        <div v-if="row.emails.length > 0" class="dropdown dropdown-right">
                            <a href="#" class="btn btn-link dropdown-toggle" tabindex="0">+</a>
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
                                @click="onRowClick(row)"
                        ><i class="icon icon-edit"></i></button>
                    </td>
                </tr>
            </tbody>
        </table>
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
 import { mapState } from 'vuex';
 
 export default {
     components: {
     },
     data() {
         return {
             contacts: [],
             fromRow: 1,
             toRow: 10,
             totalRecords: 0,
             xxx: {}
         };
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
             //this.pageno += val;
             this.getPage();
         },
         firstEmail(row) {
             return row.emails && row.emails.length > 0 ? row.emails[0].email : '(no email)';
         },
         async getPage() {
             try {
                 const request = await fetch(`http://localhost:5000/api/contacts?${this.queryParameters}`);
                 const response = await request.json();
                 this.contacts = response.data;
                 this.totalRecords = response.numberRecords;
                 this.fromRow = (response.page-1) * response.pagesize + 1;
                 this.toRow = response.page * response.pagesize;
                 this.xxx = response;
             }
             catch(error) {
                 console.error(error);
             }
         },
         onRowClick(row) {
             this.$router.push({ path: `/${row.id}` });
         },
         sortBy(field) {
             if (field == this.listSortField) {
                 this.$store.commit('setListSortDir', this.listSortDir == 'asc' ? 'desc' : 'asc');
             }
             this.$store.commit('setListSortField', field);
             this.getPage();
         }

     }
 }
</script>
