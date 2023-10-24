# ICPSR Metadata 

This repository includes the ICPSR  schema and associated documentation.

## Quick links:

- [ICPSR Metadata Documentation Portal](https://icpsr.github.io/metadata/)
- [JSON Schema](./schema/icpsr_study_schema.json) (machine actionable) version of the ICPSR Metadata Schema.

## Updating the ICPSR Metadata Documentation Portal

If new content will be added to the ICPSR Metadata Documentation Portal:

- Create a new repository branch from `main` (if working from the command line, make sure your local `main` is up to date by first running `git pull`).
- Edit the [JSON Schema or YAML files](/schema) (if making changes to the metadata schema itself) or edit/create markdown files in the [Markdown](/markdown) folder (if making changes to other metadata documentation). [1]
- If new markdown pages have been added, they must be included in the "nav" section of the [mkdocs.yaml](/resources/mkdocs.yaml) configuration file so that they will appear in the documentation portal's navigation. Each "nav" entry must include a page title and the path to the markdown file (relative to the Markdown folder), as illustrated below:  
  ![ICPSR mkdocs.yaml file](/resources/images/mkdocs_yaml.png) [2]  
 - Commit your changes and push to the remote repository. If the JSON Schema or any YAML file has been modified, this will trigger an automated GitHub Actions [workflow](/.github/workflows/update_md.yaml) that will generate a new markdown copy of the ICPSR  Schema.
 - When all edits are complete, submit a pull request and assign it to a repository member with the appropriate permissions.
 - Once the pull request is confirmed, an automated GitHub Actions [workflow](/.github/workflows/update_html.yaml) will be triggered, which:
   - Produces a new HTML version of the ICPSR Metadata Documentation Portal
   - Pushes the HTML files to the `gh-pages` repository branch, where they are made publicly accessible in the [Documentation Portal](https://icpsr.github.io/metadata/)] as soon as the workflow is completed.
 - Check the GitHub "[Actions](https://github.com/ICPSR/metadata/actions)" tab to see the workflow progress (and any error messages, should an issue arise).

 [1] For information on creating markdown documents, see [the Markdown Guide](https://www.markdownguide.org/basic-syntax/).  
 [2] For more information on MkDocs (and the [readthedocs theme](https://www.mkdocs.org/user-guide/choosing-your-theme/#readthedocs)), see the [project website](https://www.mkdocs.org/).
