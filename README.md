# cpf3d

> A python library to read and edit [3cpf](https://github.com/ruelalarcon/3cpf) files. Requires
> python 3.8.

**Features**

- Read 3cpf files into easily usable data
- Create new points and frames
- Apply basic position, scale, and rotation transformations to all points in a 3cpf file
- Write 3cpf data into 3cpf files

## Installation

The package can be installed with `pip`.

```bash
pip install cpf3d
```

## Usage

### Reading files

The `cpf3d.load` function can be used to load a 3cpf files as a `cpf3d.PointFrames` object, which has points and frames.

```python
import cpf3d

# Load a 3cpf file
pf = cpf3d.load('miku_example.3cpf')

# From here, we can access any necessary data
print('# of Points:', len(pf.points))
print('# of Frames:', len(pf.frames))

# Point colors
print('\nColors of First 5 Points:')
for point in pf.points[:5]:
    print(point.color)

# Position of specific point at specific frame
print('\nPositions of Point 0 Throughout First 5 Frames:')
for i in range(5):
    print(pf.get_position(0, i))
```
Output:
```
# of Points: 600
# of Frames: 60

Colors of First 5 Points:
(112, 112, 112)
(112, 112, 112)
(0, 0, 0)
(112, 112, 112)
(112, 112, 112)

Positions of Point 0 Throughout First 5 Frames:
[-0.01653824  0.05377164  1.10009   ]
[-0.01205087  0.05788074  1.0995283 ]
[-0.00502312  0.06201064  1.1008564 ]
[0.00529542 0.06594937 1.1022888 ]
[0.01859665 0.06944766 1.1035271 ]
```

If your use-case uses a different coordinate order (XYZ vs. YXZ for example), you can load a 3cpf with any coordinate order of your choice.
```python
import cpf3d

# Load a 3cpf file, with dimensions in the order of xzy, rather than the default xyz
pf = cpf3d.load('miku_example.3cpf', 'xzy')
```

### Editing and Creating 3cpf Files

You can edit instances of `cpf3d.PointFrames` and save them as 3cpf files.

```python
import cpf3d

# Editing an existing 3cpf file
pf = nbtlib.load('miku_example.3cpf')

# Rotate entire animation 90 degrees along the Z-axis
# Scale to half size across all dimensions
# And move 1 along the X-axis
pf.apply_rotation(0, 0, 90) \
  .apply_scale(.5, .5, .5) \
  .apply_offset(1, 0, 0)

# Save the now-transformed point frames into a new file
pf.save('miku_example_transformed.3cpf')
```

Or write a 3cpf file from scratch.
```python
import cpf3d
from cpf3d import PointFrames, Point, Frame

# Creating a 3cpf file from scratch
custom_pf = PointFrames()

point_r = Point(255, 0, 0) # Red point
point_g = Point(0, 255, 0) # Green point

custom_pf.add_point(point_r)
custom_pf.add_point(point_g)

# First frame: Red point at 1,1,1. Green point at 2,2,2
frame_1 = Frame([[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]])

# Second frame: Red point at 2,2,2. Green point at 4,4,4
frame_2 = Frame([[2.0, 2.0, 2.0], [4.0, 4.0, 4.0]])
custom_pf.add_frame(frame_1)
custom_pf.add_frame(frame_2)

# Scale it all by ten times
custom_pf.apply_scale(10, 10, 10)

# Export to a 3cpf file
custom_pf.save('my_pointframes.3cpf')
```

### Adding Points or Frames to Existing 3cpf Data

There are a variety of restrictions related to adding points or frames to existing 3cpf animations.

**Firstly,** you cannot add frames *before* adding any points.
```python
pf = PointFrames()

# Will cause an error, as there are no points to attach this positional data to
frame = Frame([[1.0, 2.0, 3.0]])
```

**Secondly,** when adding new frames, you must have one positional entry for each point.
```python
# Assume this 3cpf file contains 2 points
pf = cpf3d.load('2points.3cpf')

# Will cause an error, as we are adding a frame with 1 position, but there are 2 points
frame = Frame([[1.0, 2.0, 3.0]])
pf.add_frame(frame)

# Similarly, this would also error
frame = Frame([[1.0, 2.0, 3.0], [1.0, 2.0, 3.0], [1.0, 2.0, 3.0]])
pf.add_frame(frame)
```

**Lastly,** when adding new points, if you already have frames in your 3cpf file, you must provide positions for your new point at each frame.

```python
# Assume this 3cpf file contains 2 points and 2 frames
pf = cpf3d.load('2points2frames.3cpf')

# Will cause an error, as there are already frames in this 3cpf animation
point = Point(255, 255, 255)
pf.add_point(point)
```

We would instead need to do something like this:
```python
pf = cpf3d.load('2points2frames.3cpf')

point = Point(255, 255, 255)

# This point moves from 1,1,1 to 2,2,2 through frames 0 and 1
positions = [[1.0, 1.0, 1.0], [2.0, 2.0, 2.0]]

pf.add_frame(point, positions) # This works fine
```

This is necessary due to the nature of 3cpf files, in that each point must have corresponding positional data within each frame chunk.

## Contributing

Contributions are welcome. This project is packaged with python's built-in [setuptools](https://setuptools.pypa.io/en/latest/).

To install this package locally for development, you can clone or download this repository and navigate to it in your terminal.

You should now be able to install it locally, including development dependencies.

```bash
pip install -e .[dev]
```

You can run the tests by simply executing pytest from the top directory.

```bash
pytest
```