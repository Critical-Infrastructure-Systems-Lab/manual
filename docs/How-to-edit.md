---
layout: page
title: How to edit this manual
description: >
  Resources for editing pages and blog posts of this manual.
hide_description: true
sitemap: false
permalink: /docs/how-to-edit
---

## About

This manual is hosted on [GitHub pages](https://pages.github.com), a feature of GitHub that allows us to host a static website from a public repository. This means that:

- Anybody can look at the material we create
- **Anybody within the CIS Lab can contribute to the manual!**

GitHub pages uses [Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/about-github-pages-and-jekyll#), a static site generator that takes Markdown and HTML files and creates a complete static website based on your choice of layouts. Among the several Jekyll themes available, **we chose [Hydejack](https://hydejack.com/)**. It is not only visually appealing, but it also provides many relevant features, such as [blogging](https://hydejack.com/blog/) or [writing math](https://hydejack.com/docs/writing/#adding-math).

## Before moving forward

As explained above, this manual builds on GitHub, GitHub pages, Markdown, and Hydejack. You will thus need a basic level of familiarity with these tools before you can start contributing to the manual. Your **To do list**:

- Familiarize with [Markdown](https://critical-infrastructure-systems-lab.github.io/manual/docs/general-programming) 
- Take the introductory course to [GitHub](https://critical-infrastructure-systems-lab.github.io/manual/docs/general-programming). Note that the specific training we recommend includes a specific [section](https://github.com/skills/github-pages) on GitHub Pages.
- Take a quick look at the Hydejack [documentation](https://hydejack.com/docs/). Since the manual has already been setup, the key sections you will need are [Config](https://hydejack.com/docs/config/), [Basics](https://hydejack.com/docs/basics/), and [Writing](https://hydejack.com/docs/writing/). Also, note that this website was forked from [https://github.com/hydecorp/hydejack-starter-kit](https://github.com/hydecorp/hydejack-starter-kit), so you can always check out that repo for some additional examples.
- Ask [Stefano](emailto:galelli@cornell.edu) for access to the GitHub [repo](https://github.com/Critical-Infrastructure-Systems-Lab/manual) containing this website.

## The file structure

The last step before editing the manual is to get to know the **file structure**. These are the main **folders** you will likely have to deal with:

- The `root` folder contains the `about.md`, `README.md`, and `_config.yml` files. As explained below, these files can be edited, but **please check with Stefano before doing so**.
- `_data` contains the `authors.yml` file that provides specifications on the authors of blog posts.
- `assets/img/docs` is the folder containing documents linked to pages, such as `.pdf` files.
- `docs` contains all webpages, with the exception of `about.md` and blog posts (more below).

## Specific types of contribution

Here, we illustrate the steps needed to implement the most common contributions to the manual.

### Editing an existing page

This is probably the easiest step. All `.md` files supporting the **existing pages** are contained in the folder `docs`, so you just have to navigate to that folder, click *edit* and then *Commit changes*. Once done, **please wait for a few seconds**; it takes some time for GitHub pages to build the website. When you open the [website](https://critical-infrastructure-systems-lab.github.io/manual/), **remember to refresh the webpage** to clear the cache of your browser.

The only page that you will not find in the folder `docs` is `about.md`, which is contained in the root folder. 

### Adding a new page

Creating a new `.md` file is also easy: just navigate to the folder `docs` and add a new file. As for its content, you can start from scratch or copy-and-then-edit an existing file from either this repo or the [Hydejack starter kit](https://github.com/hydecorp/hydejack-starter-kit).

You will then have to make sure that new page appears on the website. You will have two options:

- Link the new page to the **sidebar**, a process that require editing the `_config.yml` file contained in the root folder:

```yml
# file: `_config.yml`
menu:
  - title:             About
    url:               /about/
#  - title:             Documentation
#    url:               /docs/
  - title:             How to edit this manual
    url:               /docs/how-to-edit
  - title:             Graduate studies matters
    url:               /docs/grad-studies-matters
```

This is not difficult--see this [example](https://hydecorp.github.io/hydejack-starter-kit/docs/basics/#adding-an-entry-to-the-sidebar)--but **please reach out to Stefano** if you are planning to do so.

- Link the new page to an existing page. This is done as shown in the examples below:

```
[Hydejack starter kit]([https://website-name.com](https://github.com/hydecorp/hydejack-starter-kit))
```

```
[General programming](docs/general-programming.md)
```

```
[Stefano](emailto:galelli@cornell.edu)
```  

### Adding a new file

You may want to add a new file--such as a `.pdf` or `ppt` presentation--and then link it to a webpage. To do so, follow these two steps:

- Files are contained in the folder `assets/img/docs`. Just navigate to the folder and upload the file.

- To link the file, follow the example reported below:

```
[Template](../assets/img/docs/Abstract-template.docx)
```

### Adding an author

Authors can be added by editing the `authors.yml` file in the `_data` folder. Additional details are reported [here](https://hydejack.com/docs/config/#adding-an-author).


### Adding a blog post

Blog posts, finally! First, you should note that posts are organized by categories or tags, such as `writing` or `programming`. 

If you are planning to write **a post about an existing category**, just navigate to the corresponding folder, such as `programming/_posts`, and then create a post taking one of the existing posts as an example.

If, on the other hand, you are planning to create a post about a new category, the process is a bit more nuanced:

- First, access the folder `_featured_categories` and create a `.md` file describing the category.
- Then, create a new folder (in the `root` one) that will contain all posts for that category.
- Finally, create your first post for that specific category.

More details on these steps are reported [here](https://hydejack.com/docs/basics/#adding-a-category-or-tag).




