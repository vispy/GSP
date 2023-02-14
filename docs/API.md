
# Graphic Server Protocol

The Graphic Server Protocol (GSP) is meant to be an API between hardware and software, targeted at developpers who do not want to dive into the arcane of [OpenGL](https://www.opengl.org/), [Metal](https://developer.apple.com/metal/) or [Vulkan](https://www.vulkan.org/). The overall goal of GPS is not to provide a generic graphics API but to address instead scientific visualization, which requires a fewer number of objects and concepts.

* [Core](#core)  
* [Transform](#transform)  
* [Visual](#visual)

## [Core]()

Core objects

* [x] [core.Canvas]() - create a drawing surface
* [x] [core.Viewport]() - define a region over a drawing surface
* [x] [core.Buffer]() - encapsulate raw data of any type  
* [ ] [core.Texture]() - define a 1D, 2D or 3D Buffer
* [x] [core.Color]() - define a color
* [ ] [core.Font]() - define a font specification
* [ ] [core.Style]() - define a drawing style

## [Visual]()

Visual objects

### Zero dimension

* [x] [visual.Pixels]() - create a collection of pixels
* [x] [visual.Points]() - create a collection of points
* [ ] [visual.Markers]() - create a collection of markers

### One dimension

* [ ] [visual.Segments]() - create a collection of line segments
* [ ] [visual.Lines]() - create a collection of straight lines
* [ ] [visual.Paths]() - create a collection of smooth lines

### Two dimensions

* [ ] [visual.Quads]() - create a collection of quads
* [ ] [visual.Triangles]() - create a collection of triangles
* [ ] [visual.Polygons]() - create a collection of polygons
* [ ] [visual.Glyphs]() - create a collection of glyphs

### Three dimensions

* [x] [visual.Mesh]() - create a mesh
* [ ] [visual.Volume]() - create a volume


## [Transform]()

Transformations allows to transform a Buffer and can be composed with other transforms.

### Base

* [x] [transform.Transform]() - Generic transform

### Arithmetic operators
  
* [x] [transform.Add]() - Addition
* [x] [transform.Sub]() - Subtraction
* [x] [transform.Mul]() - Multiplication
* [x] [transform.Div]() - Division

### Geometry / color accessors

* [x] [transform.X]() / [transform.R]() - First component
* [x] [transform.Y]() / [transform.G]() - Second component
* [x] [transform.Z]() / [transform.B]() - Third component
* [x] [transform.W]() / [transform.A]() - Fourth component

### Datetime accessors

* [ ] [transform.Second]() - Access to second
* [ ] [transform.Minute]() - Access to minute
* [ ] [transform.Hour]() - Access to hour
* [ ] [transform.Day]() - Access to day
* [ ] [transform.Month]() - Access to month
* [ ] [transform.Year]() - Access to year

### Geometry

* [ ] [transform.Scale]() - Abritrary scaling
* [ ] [transform.Translate]() - Arbitraty translation
* [ ] [transform.Rotate]() - Arbitraty rotation

### Screen access (JIT)

  * [ ] [transform.ScreenX]() - Screen X coordinates
  * [ ] [transform.ScreenY]() - Screen Y coordinates
  * [x] [transform.ScreenZ]() - Screen Z (depth) coordinates 

### Unit conversion

  * [ ] [transform.Pixel]() - Conversion to pixel
  * [ ] [transform.Point]() - Conversion to point (1/72 inch)
  * [ ] [transform.Inch]() - Conversion to inch
  * [ ] [transform.Millimeter]() - Conversion to millimeter
  * [ ] [transform.Centimeter]() - Conversion to centimeter
  * [ ] [transform.Meter]() - Conversion to meter

### Time conversion

  * [ ] [transform.Second]() - Conversion to seconds
  * [ ] [transform.Minute]() - Conversion to minutes
  * [ ] [transform.Hour]() - Conversion to hours
  * [ ] [transform.Day]() - Conversion to days
  * [ ] [transform.Month]() - Conversion to month
  * [ ] [transform.Year]() - Conversion to years

### Miscellaneous

* [x] [transform.Colormap]() - map a scalar to a color
* [ ] [transform.Light]() - modifies a color according to a light



  
