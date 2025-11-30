<script setup lang="ts">
import { computed, ref } from "vue";
import SolarDayChart from "./pages/SolarDayChart.vue";

const today = new Date();

function dateToString(_date: Date) {
    return `${_date.getFullYear()}-${(_date.getMonth() + 1).toString().padStart(2, "0")}-${_date.getDate().toString().padStart(2, "0")}`
}

const selectedDate = ref<string>(dateToString(today));
const dateObject = computed(() => new Date(selectedDate.value));
const handleDateChange = (event: Event) => {
    const target = event.target as HTMLInputElement;
    selectedDate.value = target.value;
}
function setDate(delta: number) {
    const next = new Date(dateObject.value);
    next.setDate(dateObject.value.getDate() + delta);
    selectedDate.value = dateToString(next);
}
</script>

<template>
    <div>
        <button @click="() => setDate(-1)">Previous</button>
        <input style="margin: 0 10px;" type="date" v-model="selectedDate" @change="handleDateChange" />
        <button @click="() => setDate(1)">Next</button>
    </div>
    <SolarDayChart :date="dateObject" />
</template>

<style scoped>

</style>
