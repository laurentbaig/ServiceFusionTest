<template>
    <div v-if="isEditing">
        <div class="form-group">
        <input type="text"
               class="form-input"
               v-model="cachedValue">
        <button class="btn btn-error"
                @click="onEditCanceled"
        ><i class="icon icon-cross"></i>
        </button>
        <button class="btn btn-primary"
                @click="onEditAccepted"
        ><i class="icon icon-check"></i>
        </button>
        </div>
    </div>
    <div v-else>
        {{ shownValue }}
        <button class="btn btn-sm btn-link" @click="onEditClicked">Edit</button>
    </div>
</template>

<style scoped>
 .form-group {
     display: flex;
 }
 .form-input {
     flex: 1;
 }
 .form-group .btn {
     flex: 0 0 36px;
 }
</style>

<script>
 export default {
     props: {
         value: {
             type: Object,
             default: () => ({})
         },
         field: {
             type: String,
             default: ''
         }
     },
     data() {
         return {
             cachedValue: '',
             isEditing: false
         };
     },
     computed: {
         shownValue() {
             return this.value[this.field];
         }
     },
     methods: {
         onEditAccepted() {
             let emitval = this.value;
             emitval[this.field] = this.cachedValue;
             this.$emit('input', emitval);
             this.isEditing = false;
         },
         onEditCanceled() {
             this.cachedValue = this.shownValue;
             this.isEditing = false;
         },
         onEditClicked() {
             this.cachedValue = this.shownValue;
             this.isEditing = true;
         },
     }
 }
</script>
