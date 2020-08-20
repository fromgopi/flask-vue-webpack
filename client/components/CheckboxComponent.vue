<template>
    <div>
        <div class="text-center">{{ personName }} as {{ title }}</div>
    </div>
</template>

<script>
export default {
    props: ['personName'],
    data() {
        return {
            title: 'check me'
        }
    }
}
</script>

<style>

</style>