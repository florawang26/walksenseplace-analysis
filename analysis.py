import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# load both files
grass = pd.read_csv('data/grass.csv')
concrete = pd.read_csv('data/concrete.csv')

# initial data exploration
print(grass.head())
print(grass.columns.tolist())
print(grass['sole_id'].value_counts())

# filter out corrupt rows
grass = grass[grass['corrupt'] == 0]
concrete = concrete[concrete['corrupt'] == 0]

# define pressure columns
pressure_cols = [f'pressure_{i:02d}' for i in range(1, 13)]

# separate left and right foot - .copy() avoids pandas warnings
# sole_id 1 = right foot, sole_id 2 = left foot
grass_right = grass[grass['sole_id'] == 1].copy()
grass_left = grass[grass['sole_id'] == 2].copy()
concrete_right = concrete[concrete['sole_id'] == 1].copy()
concrete_left = concrete[concrete['sole_id'] == 2].copy()

# convert timestamp to seconds starting from 0
grass_right['time_s'] = (grass_right['timestamp'] - grass_right['timestamp'].min()) / 1000
grass_left['time_s'] = (grass_left['timestamp'] - grass_left['timestamp'].min()) / 1000
concrete_right['time_s'] = (concrete_right['timestamp'] - concrete_right['timestamp'].min()) / 1000
concrete_left['time_s'] = (concrete_left['timestamp'] - concrete_left['timestamp'].min()) / 1000

# sum all 12 sensors = total foot load per row
grass_right['total_pressure'] = grass_right[pressure_cols].sum(axis=1)
grass_left['total_pressure'] = grass_left[pressure_cols].sum(axis=1)
concrete_right['total_pressure'] = concrete_right[pressure_cols].sum(axis=1)
concrete_left['total_pressure'] = concrete_left[pressure_cols].sum(axis=1)

# plot total pressure over time for grass - both feet
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(grass_right['time_s'], grass_right['total_pressure'], label='right foot')
ax.plot(grass_left['time_s'], grass_left['total_pressure'], label='left foot')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Total Pressure')
ax.set_title('Grass - Total Pressure Over Time')
ax.legend()
plt.tight_layout()
plt.savefig('figures/grass_pressure.png')
plt.show()
plt.close()

# plot total pressure over time for concrete - both feet
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(concrete_right['time_s'], concrete_right['total_pressure'], label='right foot')
ax.plot(concrete_left['time_s'], concrete_left['total_pressure'], label='left foot')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Total Pressure')
ax.set_title('Concrete - Total Pressure Over Time')
ax.legend()
plt.tight_layout()
plt.savefig('figures/concrete_pressure.png')
plt.show()
plt.close()

# simple step detection without scipy
# a peak is where pressure is higher than both neighbors
def find_steps(pressure_series, min_pressure=4000):
    values = pressure_series.values
    peaks = []
    for i in range(1, len(values) - 1):
        # check if this point is higher than neighbors
        if values[i] > values[i-1] and values[i] > values[i+1]:
            # only count if pressure is high enough to filter noise
            if values[i] > min_pressure:
                peaks.append(i)
    return peaks

# find steps for each foot and surface
grass_right_steps = find_steps(grass_right['total_pressure'])
grass_left_steps = find_steps(grass_left['total_pressure'])
concrete_right_steps = find_steps(concrete_right['total_pressure'])
concrete_left_steps = find_steps(concrete_left['total_pressure'])

# print step counts
print(f'Grass right foot steps: {len(grass_right_steps)}')
print(f'Grass left foot steps: {len(grass_left_steps)}')
print(f'Concrete right foot steps: {len(concrete_right_steps)}')
print(f'Concrete left foot steps: {len(concrete_left_steps)}')

# calculate duration of each recording in seconds
grass_duration = (grass_right['timestamp'].max() - grass_right['timestamp'].min()) / 1000
concrete_duration = (concrete_right['timestamp'].max() - concrete_right['timestamp'].min()) / 1000

print(f'Grass duration: {grass_duration:.1f} seconds')
print(f'Concrete duration: {concrete_duration:.1f} seconds')

# calculate cadence in steps per minute
grass_right_cadence = (len(grass_right_steps) / grass_duration) * 60
grass_left_cadence = (len(grass_left_steps) / grass_duration) * 60
concrete_right_cadence = (len(concrete_right_steps) / concrete_duration) * 60
concrete_left_cadence = (len(concrete_left_steps) / concrete_duration) * 60

print(f'Grass right cadence: {grass_right_cadence:.1f} steps/min')
print(f'Grass left cadence: {grass_left_cadence:.1f} steps/min')
print(f'Concrete right cadence: {concrete_right_cadence:.1f} steps/min')
print(f'Concrete left cadence: {concrete_left_cadence:.1f} steps/min')

# average pressure per sensor for each surface
grass_avg = grass[pressure_cols].mean()
concrete_avg = concrete[pressure_cols].mean()

# plot average pressure per sensor - grass vs concrete
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(12)
width = 0.35
ax.bar(x - width/2, grass_avg, width, label='Grass')
ax.bar(x + width/2, concrete_avg, width, label='Concrete')
ax.set_xlabel('Sensor')
ax.set_ylabel('Average Pressure')
ax.set_title('Average Pressure per Sensor Zone - Grass vs Concrete')
ax.set_xticks(x)
ax.set_xticklabels([f'S{i}' for i in range(1, 13)])
ax.legend()
plt.tight_layout()
plt.savefig('figures/sensor_comparison.png')
plt.show()
plt.close()

# plot grass right foot pressure with detected steps marked
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(grass_right['time_s'], grass_right['total_pressure'], label='pressure')
step_times = grass_right['time_s'].values[grass_right_steps]
step_pressures = grass_right['total_pressure'].values[grass_right_steps]
ax.scatter(step_times, step_pressures, color='red', zorder=5, label='detected steps')
ax.set_xlabel('Time (seconds)')
ax.set_ylabel('Total Pressure')
ax.set_title('Grass - Detected Steps on Right Foot')
ax.legend()
plt.tight_layout()
plt.savefig('figures/grass_steps_detected.png')
plt.show()
plt.close()