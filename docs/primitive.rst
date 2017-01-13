===============================
Image Processing with Primitive
===============================

How It Works
------------

`Primitive`_ is a machine-learning based program which converts images to its geometric primitives form (written in Go).

.. autofunction:: maidchan.primitive.process_image

Initially, Maid-chan will validate whether the image input is either `.png` or `.jpg`.

.. autofunction:: maidchan.primitive.create_primitive_image

Maid-chan creates 3 different images via Primitive. The shell command which is executed:

.. code-block:: bash

   $ primitive -i /tmp/{input_file} -o /tmp/{primitive_output_file} -n 175 -v

.. autofunction:: maidchan.primitive.generate_gif_file_from_primitive

Finally, `ImageMagick`_ converts those 3 generated images to a GIF file with:

.. code-block:: bash

   $ convert -delay 1x5 -loop 0 /tmp/{primitive_output_files} /tmp/{gif_output_file}

Since primitive uses hill climbing and simulated annealing in image generation,
the entire process might take several minutes depending on CPU capacity.

How to Run
----------

1. Ensure you have `ImageMagick`_ installed.

2. Then, you can start running Maid-chan primitive worker by executing:

.. code-block:: bash

   $ maidchan_primitive

.. _Primitive: https://github.com/fogleman/primitive
.. _ImageMagick: https://www.imagemagick.org/script/index.php
