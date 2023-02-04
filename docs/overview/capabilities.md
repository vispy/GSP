---
Title:     Graphic Server Protocol (GSP) / Capabilities
Authors:   Nicolas P. Rougier
Date:      February 4, 2023
License:   BSD 2 Clauses licence
Homepage:  https://vispy.org/GSP
---

# Capabilities

## Core

- [x] [**Canvas**](../protocol/core/canvas.md)  *:octicons-tag-24: alpha*{.push-right}

       2D drawing areas, onscreen or offscreen.

- [x] [**Viewport**](../protocol/core/viewport.md)  *:octicons-tag-24: alpha*{.push-right}

       Subdivision of a canvas

- [x] [**Buffer**](../protocol/core/buffer.md)  *:octicons-tag-24: alpha*{.push-right}

       Arbitrary one-dimensional data representation 

## Visuals

- [x] [**Pixels**](../protocol/visual/pixels.md)  *:octicons-tag-24: alpha*{.push-right}

       Collection of pixesl with arbitrary positon and color.

- [x] [**Points**](../protocol/visual/points.md)  *:octicons-tag-24: alpha*{.push-right .not-done}

       Collection of points with arbitrary position, size, edge color,
       edge thickness and fill color.

- [ ] **Markers** *:octicons-tag-24: alpha*{.push-right .not-done}

       Collection of pre-defined markers with arbitrary size, edge color, edge
       thickness and fill color.

- [ ] **Segments** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of anti-aliased line segments with arbitrary thickness, color
      and pre-defined end caps.

- [ ] **Polylines** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of anti-aliased polylines with arbitrary thickness, color and
      pre-defined joins and end caps.

- [ ] **Polygons** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of anti-aliased polygons with arbitrary edge and fill color,
      edge tickness and pre-defined joins.

- [ ] **Meshes** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of meshes with arbitrary fill color.

- [ ] **Volumes** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of volumes

- [ ] **Text** *:octicons-tag-24: alpha*{.push-right .not-done}

      Collection of text strings

## Transforms

- [ ] **Linear transforms** *:octicons-tag-24: alpha*{.push-right .not-done}

      Zoom, translate and rotations (2D/3D)

- [ ] **Colormaps** *:octicons-tag-24: alpha*{.push-right .not-done}

      Arbitrary color mapping from a scale

- [ ] **Projections** *:octicons-tag-24: alpha*{.push-right .not-done}

      Arbitrary data projections
