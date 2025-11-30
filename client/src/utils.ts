

export type SolarMeasurement = [number, number];

export function analyseData(data: Array<SolarMeasurement>): [Array<number>, number] {
    let _total = [0]; // Initialize with 0 for the first point
    let _max = 0;

    for (let i = 1; i < data.length; i++) {
        const h = data[i][0] - data[i - 1][0]; // Width of the trapezoid
        const area = (data[i - 1][1] + data[i][1]) / 2 * h; // Area of the trapezoid
        _total.push(_total[i - 1] + (area / (60 * 60 * 1000))); // Add to the cumulative sum
        if (data[i][1] > _max) _max = data[i][1];
    }

    return [_total, _max];
}

export function roundCumulativeValue(value: number) {
    return Math.round(10 * value) / 10;
}
