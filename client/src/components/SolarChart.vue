<script setup lang="ts">
import { computed } from 'vue';
import type { VueApexChartsComponent } from 'vue3-apexcharts';
import { analyseData, roundCumulativeValue, type SolarMeasurement } from '../utils';


const { measurements, cumulative, xRange, yRange } = defineProps<{measurements: Array<SolarMeasurement>, cumulative: boolean, xRange: [Date, Date], yRange: [number, number]}>();

function getCumulativeTotal(_measurements: Array<SolarMeasurement>) {
    const [total] = analyseData(_measurements);
    return total;
}

const options = computed<VueApexChartsComponent["options"]>(() => {
    const ret: VueApexChartsComponent["options"] = {
        xaxis: {
            type: "datetime",
            labels: {
                datetimeUTC: false
            },
            min: Number(xRange[0]),
            max: Number(xRange[1]),
        },
        yaxis: {
            min: Number(yRange[0]),
            max: Number(yRange[1]),
        },
        dataLabels: {
            enabled: false
        },
        fill: {
            type: "solid"
        },
        tooltip: {
            x: {
                format: "HH:mm:ss"
            }
        }
    };
    return ret;
});
const series = computed<VueApexChartsComponent["series"]>(() => {
    const cumulativeTotal = getCumulativeTotal(measurements);
    const readings = measurements.map((m, _i) => {
        const y = cumulative ? roundCumulativeValue(cumulativeTotal[_i]) : m[1];
        return [new Date(m[0] * 1000), y]
    });
    return [{
        name: cumulative ? "kWh" : "Watts",
        data: readings,
    }]
});

const width = Math.min(500, window.innerWidth);
</script>

<template>
<div>
    <apexchart :width="width" type="area" :options="options" :series="series"></apexchart>
</div>
</template>
