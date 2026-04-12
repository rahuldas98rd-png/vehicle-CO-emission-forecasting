# Fuel Consumption Dataset

## Overview

This dataset contains fuel consumption ratings and CO₂ emission figures for model year 2000 passenger vehicles sold in Canada. It covers 639 vehicle configurations across 36 manufacturers and is split across two sheets that share a common key (`Snr`).

---

## File Structure

**File:** `Fuel_consumption.xlsx`  
**Total Records:** 639 rows per sheet  
**Sheets:** 2 (`Sheet1`, `Sheet2`)

### Sheet1 — Vehicle Identity

Contains basic vehicle identification information.

| Column | Type    | Description                                      |
|--------|---------|--------------------------------------------------|
| `Snr`  | Integer | Unique serial number (primary key); ranges 1101–1739 |
| `Year` | Integer | Model year (all records: 2000)                   |
| `MAKE` | String  | Vehicle manufacturer (e.g., ACURA, FORD, TOYOTA) |
| `MODEL`| String  | Vehicle model name (e.g., 1.6EL, MUSTANG, CAMRY) |

### Sheet2 — Technical & Emissions Specifications

Contains engine specs, transmission, fuel type, consumption, and emissions data.

| Column             | Type    | Description                                                |
|--------------------|---------|------------------------------------------------------------|
| `Snr`              | Integer | Unique serial number (foreign key linking to Sheet1)       |
| `ENGINE SIZE`      | Float   | Engine displacement in litres (range: 1.0 – 8.0 L)        |
| `CYLINDERS`        | Integer | Number of engine cylinders (3, 4, 5, 6, 8, 10, or 12)     |
| `TRANSMISSION`     | String  | Transmission type and number of gears (see codes below)    |
| `FUEL`             | String  | Fuel type code (see codes below)                           |
| `FUEL CONSUMPTION` | Float   | Combined city/highway fuel consumption in L/100 km (range: 4.9 – 30.2) |
| `COEMISSIONS`      | Integer | CO₂ tailpipe emissions in g/km (range: 104 – 582)          |

---

## Code Reference

### Transmission Codes

| Code | Meaning                        |
|------|--------------------------------|
| `A3` | Automatic, 3 speeds            |
| `A4` | Automatic, 4 speeds            |
| `A5` | Automatic, 5 speeds            |
| `AS4`| Automatic with select-shift, 4 speeds |
| `AS5`| Automatic with select-shift, 5 speeds |
| `AS6`| Automatic with select-shift, 6 speeds |
| `M5` | Manual, 5 speeds               |
| `M6` | Manual, 6 speeds               |

### Fuel Type Codes

| Code | Meaning                  |
|------|--------------------------|
| `X`  | Regular gasoline (87 octane) |
| `Z`  | Premium gasoline (91+ octane) |
| `D`  | Diesel                   |
| `E`  | Ethanol (E85)            |
| `N`  | Natural gas              |

---

## Key Statistics

| Metric                | Min   | Mean   | Max    |
|-----------------------|-------|--------|--------|
| Engine Size (L)       | 1.0   | 3.27   | 8.0    |
| Fuel Consumption (L/100 km) | 4.9 | 14.71 | 30.2 |
| CO₂ Emissions (g/km)  | 104   | 296.8  | 582    |

- **Total vehicles:** 639
- **Manufacturers:** 36 (most represented: CHEVROLET with 63 records)
- **Unique models:** 328
- **Missing values:** None in either sheet

---

## How to Use

The two sheets are linked by the `Snr` column. To work with the full dataset, join them on `Snr`:

```python
import pandas as pd

sheet1 = pd.read_excel("Fuel_consumption.xlsx", sheet_name="Sheet1")
sheet2 = pd.read_excel("Fuel_consumption.xlsx", sheet_name="Sheet2")

df = pd.merge(sheet1, sheet2, on="Snr")
```

---

## Potential Use Cases

- Comparing fuel efficiency across vehicle makes and models
- Analysing the relationship between engine size, cylinders, and CO₂ emissions
- Studying the impact of transmission type or fuel type on fuel consumption
- Building regression models to predict emissions from vehicle specifications
- Exploring the distribution of vehicle classes available in the 2000 model year

---

## Notes

- All records correspond to the model year **2000**; the `Year` column has no variance.
- The `COEMISSIONS` column name contains a trailing space in the raw file — trim it when reading programmatically.
- Fuel consumption figures represent a combined city/highway estimate in **litres per 100 kilometres (L/100 km)**, which is the standard used in Canada (lower = more efficient).
