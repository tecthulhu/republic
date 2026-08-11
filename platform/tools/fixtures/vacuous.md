# Vacuous fixture (SPEC-0092)

A governed-looking markdown file that carries no atoms: no frontmatter, no
column-0 encoding markers. Before STORY-0003 this file — and any single-file
argument — made atom-lint report a pass over zero atoms. It must now fail
closed with reason `empty-input`.

The marker below is indented, so it is inert per ONT-070a and must not be
parsed as an atom:

    <!-- atom:begin id=SPEC-9999 -->
    ```yaml
    id: SPEC-9999
    ```
    <!-- atom:end id=SPEC-9999 -->
