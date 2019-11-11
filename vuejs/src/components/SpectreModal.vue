<template>
    <div v-if="isOpened" class="modal active" id="modal-id">
        <a href="#close"
           class="modal-overlay"
           aria-label="Close"
           @click="close()"
        ></a>
        <div class="modal-container">
            <div class="modal-header">
                <a href="#close"
                   class="btn btn-clear float-right"
                   aria-label="Close"
                   @click="close()"
                ></a>
                <div class="modal-title h5">{{ title }}</div>
            </div>
            <div class="modal-body">
                <div class="content">
                    <!-- content here -->
                    <slot></slot>
                </div>
            </div>
            <div class="modal-footer">
                <slot name="footer"></slot>
            </div>
        </div>
    </div>
</template>

<script>
 export default {
     props: {
         title: String
     },
     data() {
         return {
             isOpened: false
         };
     },
     methods: {
         open() {
             this.isOpened = true;
         },
         close() {
             this.isOpened = false;
         }
     }
 }
</script>
