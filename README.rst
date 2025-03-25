===========================
Darca Space Git
===========================

**darca-space-git** integrates Git operations into space-managed environments from `darca-space-manager`.

It acts as a high-level bridge between the `darca-git` Git abstraction and space/file management.

Features
========

- ⛺ Git operations are scoped to logical spaces
- 🔒 No direct file system access required
- 🧪 Full test coverage & modular design
- 💡 Supports dry-run & file-level restore
- 🔁 Clean separation of Git vs Space responsibilities

Install
=======

Install everything needed:

.. code-block:: bash

    make install

Usage
=====

.. code-block:: python

    from darca_space_git.space_git import SpaceGitManager

    git_mgr = SpaceGitManager()
    git_mgr.init_repo("myspace")
    git_mgr.get_status("myspace")

Run Tests
=========

.. code-block:: bash

    make test

Run Pre-Commit Hooks
====================

.. code-block:: bash

    make precommit

Run Everything
==============

.. code-block:: bash

    make check
