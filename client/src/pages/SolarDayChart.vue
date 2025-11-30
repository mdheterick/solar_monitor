<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { analyseData, roundCumulativeValue, type SolarMeasurement } from "../utils";
import SolarChart from "../components/SolarChart.vue";


const { date } = defineProps<{ date: Date }>();
const xRange = computed<[Date, Date]>(() => {
    const start = new Date(date);
    const end = new Date(date);
    start.setHours(4);
    start.setMinutes(0);
    start.setSeconds(0);
    start.setMilliseconds(0);
    end.setHours(19);
    end.setMinutes(0);
    end.setSeconds(0);
    end.setMilliseconds(0);
    return [start, end];
});
const cumulative = ref<boolean>(false);
const yRange = computed<[number, number]>(() => {
    return cumulative.value ? [0, 35] : [0, 5500];
})


const toggleCumulative = () => {
    cumulative.value = !cumulative.value;
}

const measurements = ref<Array<SolarMeasurement>>([]);
const analysis = computed(() => analyseData(measurements.value));
const server = window.location.origin.replace(window.location.port, "8080");

async function doRequest(_date: Date) {
    const dateString = `/solar/day/${_date.getFullYear()}-${_date.getMonth() + 1}-${_date.getDate()}`;
    const response = await fetch(server + dateString);
    measurements.value = await response.json();
}

onMounted(async () => {
    await doRequest(date);
});

watch(() => date, async (newDate) => {
    await doRequest(newDate);
});
</script>

<template>
    <div class="solar-chart-tools">
        <button @click="toggleCumulative">Show {{ cumulative ? "instantaneous" : "cumulative" }}</button>
    </div>
    <SolarChart :measurements="measurements" :cumulative="cumulative" :xRange="xRange" :yRange="yRange" />
    <div>
        <div>
            <label>Total Energy Produced</label>
            <p>{{ roundCumulativeValue(analysis[0][analysis[0].length - 1]) }} kWh</p>
        </div>
        <div>
            <label>Peak Energy Produced</label>
            <p>{{ analysis[1] }} W</p>
        </div>
    </div>
</template>

<style scoped>
.solar-chart-tools {
    margin-top: 1rem;
}
</style>
