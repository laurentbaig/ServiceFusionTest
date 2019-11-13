<template>
    <div>
        <div>{{ title }}</div>
        <div class="form-group columns">
            <div class="column">
                <label>year</label>
                <select class="form-select" v-model="year">
                    <option v-for="yy in years" :key="yy" :value="yy">{{ yy }}</option>
                </select>
            </div>
            <div class="column">
                <label>month</label>
                <select class="form-select" v-model="month">
                    <option v-for="mo in months" :key="mo.id" :value="mo.id">{{ mo.name }}</option>
                </select>
            </div>
            <div class="column">
                <label>day</label>
                <select class="form-select" v-model="day">
                    <option v-for="dy in days" :key="dy" :value="dy">{{ dy }}</option>
                </select>
            </div>
        </div>
    </div>
</template>

<style scoped>
 label {
     color: #aaa;
 }
</style>

<script>
 export default {
     props: {
         value: {
             type: Date,
             default: () => new Date()
         },
         title: String
     },
     data() {
         let today = this.value;
         return {
             days: this.createDaysArray(today),
             months: [
                 { id: 1, name: 'January'},
                 { id: 2, name: 'February'},
                 { id: 3, name: 'March'},
                 { id: 4, name: 'April'},
                 { id: 5, name: 'May'},
                 { id: 6, name: 'June'},
                 { id: 7, name: 'July'},
                 { id: 8, name: 'August'},
                 { id: 9, name: 'September'},
                 { id: 10, name: 'October'},
                 { id: 11, name: 'November'},
                 { id: 12, name: 'December'}
             ],
             years: this.createYearsArray(today)
         };
     },
     computed: {
         year: {
             get() { return this.value.getUTCFullYear(); },
             set(v) { this.update(v, this.month, this.day); }
         },
         month: {
             get() { return this.value.getUTCMonth()+1; },
             set(v) { this.update(this.year, v, this.day); }
         },
         day: {
             get() { return this.value.getUTCDate(); },
             set(v) { this.update(this.year, this.month, v); }
         },
     },
     methods: {
         createDaysArray(today) {
             let ndays = this.getDaysForMonth(today.getMonth(), today.getYear());
             let days = [];
             for (let ii = 0; ii < ndays; ii++) {
                 days.push(ii+1);
             }
             return days;
         },
         createYearsArray(today) {
             let ylast = today.getYear() + 1900;
             let years = [];
             for (let yy = 1900; yy <= ylast; yy++) {
                 years.push(String(yy));
             }
             return years.reverse();
         },
         getDaysForMonth(mo, yy) {
             let d31 = [1,3,5,7,8,10,12];
             let d30 = [2,4,6,9,11];
             if (d31.indexOf(mo) >= 0) {
                 return 31;
             }
             else if (d30.indexOf(mo) >= 0) {
                 return 30;
             }
             if (yy % 4 == 0) {
                 return 29;
             }
             return 28;
         },
         update(y, m, d) {
             let newDate = new Date(Date.UTC(y, m-1, d));
             this.$emit('input', newDate);
         }
     }

 }
</script>
