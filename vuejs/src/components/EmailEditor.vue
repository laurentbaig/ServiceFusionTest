<template>
    <div>
        <div v-for="(email, index) in internalEmails" class="form-group" :key="index">
            <button v-if="index > 0"
                    class="btn float-right"
                    @click="deleteEmail(index)"
            >
                <i class="icon icon-cross"></i>
            </button>
            <input type="email" class="form-input" v-model="internalEmails[index]" style="width: 90%">
        </div>
    </div>
</template>

<script>
 export default {
     props: {
         emails: {
             type: Array,
             default: () => ([''])
         }
     }
 }
</script>
