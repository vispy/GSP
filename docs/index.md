
# Introduction

The Graphic Server Protocol (GSP) is meant to be an API between hardware and software, targeted at developpers who do not want to dive into the arcane of [OpenGL], [Metal] or [Vulkan] but still want to benefit from GPU speed, versatily and quality.

The overall goal of GSP is not to provide a general graphics API but rather to address **only** scientific visualization, which requires a far fewer number of objects and concepts, with specific requirements on rendering quality though. The API is voluntarily small and targets the smallest set of visuals that allow to render the vast majority of scientific plots (2d or 3d).

[OpenGL]: https://www.opengl.org
[Metal]: https://developer.apple.com/metal
[Vulkan]: https://www.vulkan.org/
