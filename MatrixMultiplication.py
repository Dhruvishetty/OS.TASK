# Matrix Multiplication using Threads and TensorFlow
# Animation is used to show the result matrix.

import tensorflow as tf
import numpy as np
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Size of the matrices
SIZE = 100


# Creating Matrix A
A = tf.random.uniform(
    (SIZE, SIZE),
    minval=1,
    maxval=10,
    dtype=tf.int32
)

# Creating Matrix B
B = tf.random.uniform(
    (SIZE, SIZE),
    minval=1,
    maxval=10,
    dtype=tf.int32
)


# Empty matrix for storing the final result
C = np.zeros((SIZE, SIZE), dtype=int)


# Stores the cells after they are calculated
completed = []

# Used when multiple threads update the list
lock = threading.Lock()


# This function calculates one cell of Matrix C
def calculate_cell(row, col):

    # Taking one row from A
    row_data = A[row, :]

    # Taking one column from B
    column_data = B[:, col]

    # TensorFlow performs the multiplication
    value = tf.reduce_sum(row_data * column_data)

    # Store the calculated value
    C[row][col] = int(value.numpy())

    # Save the completed cell
    with lock:
        completed.append((row, col))


# ---------------- MATRIX MULTIPLICATION ----------------

print("Starting matrix multiplication...")

start_time = time.time()

threads = []


# Create a thread for every cell of Matrix C
for i in range(SIZE):
    for j in range(SIZE):

        t = threading.Thread(
            target=calculate_cell,
            args=(i, j)
        )

        threads.append(t)
        t.start()


# Wait for all threads to finish
for t in threads:
    t.join()


end_time = time.time()

print("Matrix multiplication completed.")
print("Time taken:", round(end_time - start_time, 3), "seconds")


# Display a small part of the result
print("\nFirst 3 x 3 values of Matrix C:")

for i in range(3):
    print(C[i][:3])


# ==========================================================
#                       ANIMATION
# ==========================================================

# Convert matrices for displaying
A_display = A.numpy()
B_display = B.numpy()

# Start Matrix C as empty
C_display = np.full((SIZE, SIZE), np.nan)


# Create three sections for the matrices
fig, (ax1, ax2, ax3) = plt.subplots(
    1, 3,
    figsize=(15, 6)
)

fig.suptitle(
    "Matrix Multiplication using Threads + TensorFlow",
    fontsize=16,
    fontweight="bold"
)


# ---------------- MATRIX A ----------------

ax1.imshow(
    A_display,
    cmap="Blues",
    vmin=1,
    vmax=10
)

ax1.set_title("Matrix A")
ax1.set_xticks([])
ax1.set_yticks([])


# ---------------- MATRIX B ----------------

ax2.imshow(
    B_display,
    cmap="Greens",
    vmin=1,
    vmax=10
)

ax2.set_title("Matrix B")
ax2.set_xticks([])
ax2.set_yticks([])


# ---------------- MATRIX C ----------------

result_image = ax3.imshow(
    C_display,
    cmap="magma",
    vmin=np.min(C),
    vmax=np.max(C)
)

ax3.set_title("Matrix C - Result")
ax3.set_xticks([])
ax3.set_yticks([])


# Shows the current row in Matrix A
row_marker = plt.Rectangle(
    (-0.5, -0.5),
    SIZE,
    1,
    fill=False,
    edgecolor="yellow",
    linewidth=2
)

ax1.add_patch(row_marker)


# Shows the current column in Matrix B
column_marker = plt.Rectangle(
    (-0.5, -0.5),
    1,
    SIZE,
    fill=False,
    edgecolor="yellow",
    linewidth=2
)

ax2.add_patch(column_marker)


# Shows the current cell in Matrix C
cell_marker = plt.Rectangle(
    (-0.5, -0.5),
    1,
    1,
    fill=False,
    edgecolor="white",
    linewidth=2
)

ax3.add_patch(cell_marker)


# Text showing the progress
status = fig.text(
    0.5,
    0.035,
    "Starting animation...",
    ha="center",
    fontsize=11
)


# Progress bar
progress_ax = fig.add_axes(
    [0.25, 0.01, 0.5, 0.015]
)

progress_bar = progress_ax.barh(
    [0],
    [0],
    height=1
)

progress_ax.set_xlim(0, SIZE * SIZE)
progress_ax.set_yticks([])
progress_ax.set_xticks([])


# Number of cells shown in one animation frame
# Higher value makes the animation faster
CELLS_PER_FRAME = 100


# Animation update function
def update(frame):

    start = frame * CELLS_PER_FRAME

    end = min(
        start + CELLS_PER_FRAME,
        len(completed)
    )

    current_row = 0
    current_col = 0

    # Add the completed cells to the display
    for k in range(start, end):

        current_row, current_col = completed[k]

        C_display[current_row][current_col] = \
            C[current_row][current_col]


    # Update Matrix C
    result_image.set_data(C_display)


    # Move row marker
    row_marker.set_xy(
        (-0.5, current_row - 0.5)
    )


    # Move column marker
    column_marker.set_xy(
        (current_col - 0.5, -0.5)
    )


    # Move current cell marker
    cell_marker.set_xy(
        (current_col - 0.5, current_row - 0.5)
    )


    # Update progress bar
    progress_bar[0].set_width(end)


    # Update text
    status.set_text(
        "Progress: "
        + str(end)
        + " / "
        + str(SIZE * SIZE)
        + " cells completed"
        + "     Current cell: C["
        + str(current_row)
        + "]["
        + str(current_col)
        + "]"
    )


    return [
        result_image,
        row_marker,
        column_marker,
        cell_marker,
        progress_bar[0],
        status
    ]


# Number of animation frames
total_frames = (
    len(completed) + CELLS_PER_FRAME - 1
) // CELLS_PER_FRAME


# Create the animation
animation = FuncAnimation(
    fig,
    update,
    frames=total_frames,
    interval=10,
    repeat=False
)


# Adjust the layout
plt.tight_layout(
    rect=[0, 0.07, 1, 0.94]
)


# Show the animation
plt.show()
