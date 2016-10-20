Escapad parser library API
==========================

We present the source code of the Escapad parser AnyActivity located in ``src/model.py`` file.

The ordre of presentation follows the building of Course Program structure whereby :

* a CourseProgram contains one or several AnyActivitys and is stored in a repository
* A AnyActivity is made of one source file that is parsed and optionnaly a media folder
* Each AnyActivity has a header part for the metadata and is divided in Sections, each containing one or several AnyActivitys
* Each AnyActivity can be typed as
    - Cours : can contain also video parts
    - Activity that can be of 3 types:
          ~ ActiviteAvancee: for simple quizzes
          ~ Activite (simple) : for simple exercises involving personnal research
          ~ ActiviteAvancee : for more advanced activity involving both research and personnal reflexion

Course Program
---------------

.. autoclass:: model.CourseProgram
    :members:
    :undoc-members:
    :special-members:

Module
-------

.. autoclass:: model.Module
    :members:
    :undoc-members:
    :special-members:


Section
-------

.. autoclass:: model.Section
    :members:
    :undoc-members:
    :special-members:


Subsection
----------

.. autoclass:: model.Subsection
    :members:
    :undoc-members:
    :special-members:

Cours
------

Subclass of Subsection

.. autoclass:: model.Cours
    :members:
    :undoc-members:
    :special-members:

AnyActivity
-----------

Subclass of Subsection

.. autoclass:: model.AnyActivity
    :members:
    :undoc-members:
    :special-members:

Comprehension
--------------

Subclass of AnyActivity

.. autoclass:: model.Comprehension
    :members:
    :undoc-members:
    :special-members:

Activite
----------

Subclass of AnyActivity

.. autoclass:: model.Activite
    :members:
    :undoc-members:
    :special-members:

ActiviteAvancee
---------------

Subclass of AnyActivity

.. autoclass:: model.ActiviteAvancee
    :members:
    :undoc-members:
    :special-members:
