<template>
  	<div class="container">
        <div class="row my-5 justify-content-center">
            <div class="col-sm-6">
                <h1 class="text-center">Welcome to the world of Vue</h1>
                <checkbox-component personName="James"></checkbox-component>
            </div>
        </div>
    </div>
</template>

<script>
import CheckboxComponent from './CheckboxComponent';
export default {
    components: {
        'checkbox-component': CheckboxComponent
    }
}
</script>

<style>

</style>