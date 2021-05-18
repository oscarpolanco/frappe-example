# Frappe tutorial

This will be a tutorial of the `frappe` framework using the example of the [frappe documentation](https://frappeframework.com/docs) and will have some notes.

## Installation

This installation guide will be concentrate on the `MacOs` distribution that is the one that I'm using on at the moment that I work on this tutorial

### Pre-requisites

```bash
  Python 3.6+
  Node.js 12
  Redis 5                                       (caching and realtime updates)
  MariaDB 10.3.x / Postgres 9.5.x               (to run database driven apps)
  yarn 1.12+                                    (js dependency manager)
  pip 20+                                       (py dependency manager)
  wkhtmltopdf (version 0.12.5 with patched qt)  (for pdf generation)
  cron                                          (bench scheduled jobs: automated certificate renewal, scheduled backups)
  NGINX                                         (proxying multitenant sites in production)
```

Also, you will need an editor; I use [vs code](https://code.visualstudio.com/); and a terminal; I will using [Iterm2](https://iterm2.com/)

### Installation process(pre-requisites)

- Install [Homebrew](https://brew.sh/)
- Use `homebrew` to install `python`, `git`, `redis`, `mariadb`
  `brew install python git redis mariadb`

  If you got an error with the permissions with the `brew link` step follow [this post](https://gist.github.com/dalegaspi/7d336944041f31466c0f9c7a17f7d601)

- Install `wkhtmltopdf` using [cask](https://github.com/Homebrew/homebrew-cask)
  `brew install --cask wkhtmltopdf`
- Use the `nano` command to update the `my.cnf` file
  `nano /usr/local/etc/my.cnf`

  If this path doesn't work use the following command to check the correct path:
  `mysql --help | grep "Default options" -A 1`

- Add the following to `my.cnf` file

  ```bash
  character-set-client-handshake = FALSE
  character-set-server = utf8mb4
  collation-server = utf8mb4_unicode_ci

  [mysql]
  default-character-set = utf8mb4
  ```

- Restart the `mysql` service using `brew`
  `brew services restart mariadb`
- Install [Nodejs](https://nodejs.org/en/)
- Instal [nvm](https://github.com/nvm-sh/nvm) to manage the `node` versions
  `curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash`
- Use the `12` version of `node`
  `nvm install 12`
- Check the `node` version to make sure you have the `12`
  `node -v`
- Install `yarm`
  `npm install -g yarn`

### Install bench CLI

- Use the `pip3` command to install the `frappe-bench` package
  `pip3 install frappe-bench`
- Make sure that is correct installed using checking the version
  `bench --version`

Now we are all set up, to begin with, the tutorial

## Some inside on the example

This will be the same example as shown on the [frappe tutorial section](https://frappeframework.com/docs/user/en/tutorial) where we are going to now a little bit of the `frappe` framework that is based on `python` and `MariaDB` with `jinja` for the templates.

For example, a `library manage system` will be building when a `librarian` can manage `articles` and `memberships`. We will have the following models:

- `Article`: A book o something similar item that can be rented
- `Library member`: `User` that can have a `membership`
- `Library transaction`: Get or return an `article`
- `Library Membership`: An active `member` of the `library`
- `Library settings`: Setting values of the action that will have with the `article`

The `Librarian` will have its own `admin` part that came by default on the `frappe` framework called `Desk`.

Source: https://frappeframework.com/docs/user/en/tutorial#what-are-we-building
Useful links to practice all parts of the `frappe` framework: https://frappeframework.com/docs/user/en/tutorial/prerequisites

## Setup a bench project

To continue with this section you need to follow the `Installation` section first.

- Go to your terminal and make sure you have `bench` installed using
  `bench --version`
- Now on your terminal; go where you want to place the project
- Run the `bench init` command putting the name of the project
  `bench init my_project`
  This will create a directory call it by the name that you put as `my_project` and will do the following:
  - Create a `python virtual environment`. A `virtual environment` is an isolated runtime`environment that allows`users` and applications to install and upgrade packages without interfering with the behavior of other` python` application running on the same system
  - Fetch and install the `frappe` app as a` python` package
  - Install `node modules` of` frappe`
  - Build the static assets

Source: https://frappeframework.com/docs/user/en/tutorial/install-and-setup-bench#create-the-frappe-bench-directory

### Directory structure

```bash
.
├── Procfile
├── apps
│   └── frappe
├── config
│   ├── pids
│   ├── redis_cache.conf
│   ├── redis_queue.conf
│   └── redis_socketio.conf
├── env
│   ├── bin
│   ├── include
│   ├── lib
│   └── share
├── logs
│   ├── backup.log
│   └── bench.log
└── sites
    ├── apps.txt
    ├── assets
    └── common_site_config.json
```

- `env`: `Python` virtual environment
- `config`: Config files for [Redis](https://redis.io/) and [Nginx](https://www.nginx.com/)
- `logs`: Log files for every process
- `sites`: Site directory
  - `assets`: Static assets that will be server
  - `app.txt`: List of installed `frappe` apps
  - `commonsiteconfig.json`: Site config that is available for all sites
- `apps`: Apps directory
  - `frappe`: The `frappe` app directory
- `Procfile`: List of processes that run in development

source: https://frappeframework.com/docs/user/en/tutorial/install-and-setup-bench#directory-structure

### Start your bench server

To check if everything goes as expected on the installation process we will need to start our development server(created on the previous section) so let get into it:

- On your terminal; go to the directory that was created in the previous section
- Use the `bench start` command to start your development server
- You should see the logs on the terminal without any errors

These steps will start several processes as you see on the logs of the terminal like:

- Run a `python` web server based on [gunicorn](https://gunicorn.org/)
- A `redis` server for caching
- A job queuing and `sockectio` pub-sub
- Background workers
- A `node` server for `socketio` and for compiling `js` and `css` files

Finally the dev server will be running on port `8000` but sadly we don't have any site yet so you will have a `404` error on your browser

### Creating an app

Now we will be creating an `app` that is a `python` package that uses the `frappe` framework. The default `app` is `frappe` that is created by the `bench init` command and acts as the framework for all `apps`.

All `apps` should have an entry on the `apps.txt` file that is located on the `sites` directory. This will be done automated using the `bench` command that we will see next.

- On your terminal; `frappe` project directory
- Use the `bench new-app` command
  `bench new-app my_custom_app`
- Fill in the options that will print on your terminal
- You should see that a new directory with the name that you use on the `bench new-app` command is created
- Now this is the files that you are going to track on `GitHub`
- Go with your terminal to your new `app` directory and you will see that the app `git` by default
- App your `remote` repository to `fetch` and `pull`
  `git remote add my_repo_clone_url`
- Use the `-v` option to see that the `remote` URL is correctly added
  `git remote -v`
- You should see the correct `remote` URL for `pull` and `fetch`

#### Directory structure

```bash
apps/my_custom_app
├── MANIFEST.in
├── README.md
├── my_custom_app
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── desktop.py
│   │   └── docs.py
│   ├── my_custom_app
│   │   └── __init__.py
│   ├── hooks.py
│   ├── modules.txt
│   ├── patches.txt
│   ├── public
│   │   ├── css
│   │   └── js
│   ├── templates
│   │   ├── __init__.py
│   │   └── includes
│   └── www
├── custom_app.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   ├── not-zip-safe
│   ├── requires.txt
│   └── top_level.txt
├── license.txt
├── requirements.txt
├── package.json
└── setup.py
```

- `requirements.txt`: List of `python` dependencies
- `package.json`: List of `node` dependencies
- `my_custom_app`(inside of the main `my_custom_app` directory): Store the source files
- `my_custom_app/my_custom_app`: When you create a new `app` a new module with the same name will be created
- `my_custom_app/hooks.py`: File that store the [hooks](https://frappeframework.com/docs/user/en/python-api/hooks) that override the standard behavior of `frappe`
- `my_custom_app/module.txt`: The `frappe` app is organized on modules and every [Doctype](https://frappeframework.com/docs/user/en/basics/doctypes#module) is part of a module and these are listed on this file
- `my_custom_app/patches.txt`: This file contains a reference to the `patches` that run on every [database migration](https://frappeframework.com/docs/user/en/database-migrations#data-migrations)
- `my_custom_app/public`: This is the static folder that can be served by `nginx` on production. Files in this directory can be access via the `/assets/my_custom_app/**/*`
- `my_custom_app/templates`: Store the `jinja` templates
- `my_custom_app/www`: Files in this directory will be directly mapped to [portal pages](https://frappeframework.com/docs/user/en/portal-pages) that match the directory structure

## Creating a site

`Frappe` is a multitenant platform and each tenant is called `site`. A `site` has its own database and exists on the `sites` directory.

The `sites` directory contains some other files that came by default when you create the `frappe` project such as:

- `apps.txt`: List of `apps` of `frappe`. The `apps` should be listed here before you can install a `site`(later we will show how to install a `site`). The `apps` add automatically when you run the `get-app` or `new-app` commands
- `common_site_config.json`: [Configurations](https://frappeframework.com/docs/user/en/basics/site_config) that can be used on all `sites` can be put on this file
- `asset`: Statics files that are required to the server on the browser

Source: https://frappeframework.com/docs/user/en/basics/sites

### Creating your new site

- On your terminal; go to the `frappe` project
- Use the `new-site` command to create a `site`
  `bench new-site name.of.your.site`
- Since this command will create a database for your `site` it will ask you the `MySQL` root password(The `brew` installation create a user that you can access on the terminal just using `mysql` so you will need to add the `root` password)
- A new directory should be created on the `sites` folder with the same name as the one that you use on the `new-site` command
- Now on the root directory run the `start` command
- Go to http://localhost:8000/
- You should be redirected to the `login` page(Don't log just yet we will do another thing first this is just for a test that everything goes as expected)

### Site Directory Structure

After running the `new-site` command you should have the following file structure on your `sites` directory

```bash
sites/mysite.local
├── locks
├── private
│   ├── backups
│   └── files
├── public
│   └── files
├── site_config.json
└── task-logs
```

- `lock`: Directory to synchronize various jobs using [file locking](https://en.wikipedia.org/wiki/File_locking)
- `private`: Directory that contains files that are required on the authentication access and a database backup
- `pubic`: Contains the files that can be accessed without login
- `site_config.json`: File that contains a specific `site configuration`. The `site configuration` exist on every site directory and its value is available in the `frappe.conf` local variable

source: https://frappeframework.com/docs/user/en/basics/sites

### Access the site on your browser

`Frappe` allows you to create multiple `sites` and access them separately on the same port(This is call multi-tenancy) but all `sites` on the same `url` you can't do that so we will need to follow the next process to run each `site` on it own `url`

- On your terminal; go to the `frappe` project root
- Delete the `currentsite.txt` file on the `sites` directory(When you do this you won't be able to access http://localhost:8000 anymore)
  `rm sites/currentsite.txt`
- Now we need to associate the `localhost` with the `site` that you created and `bench` have the command to do this
  `bench --site name.of.your.site add-to-hosts`
- Now On the root of the `frappe` project run the `start` command
- Go to `http://name.of.your.site:8000`
- You should be redirected to the login page(Don't log in just yet we will finish soon)

### Install your app on the site

Now we need to install the `app` that you created before on our running site.

- On your terminal; go to the `frappe` project root
- Use the following command to install your `app` in the running `site`
  `bench --site name.of.your.site install-app my_custom_app`
- Verify the installed `apps` using the following command:
  `bench --site name.of.your.site list-apps`
  You will see a `frappe app` and is fine; this `app` came by default on the `frappe` installation

### Login to Desk

Now that you all set and done we can finally login to `desk`

- On your terminal; run the `start` command
- Go to `http://name.of.your.site:8000`
- You should be redirected to the `login` page
- Fill the `login` form and submit(The default user is `Administrator` and the `password` is the one that you specify when you created the `site`)

## DocType

The `doctype` describes the `model` and the `view` of your data. It contains what fields are stored for your data and how they will behave respect to each other. It enable a `ORM` and when you create a new `docType` a `JSON` object will be create on your `app` directory.

Before we begin to create our custom `docTypes` we will need to enable the development mode that will create a boilerplate for the creation of the new `docTypes` and we can track then into version control in the `app` directory. So follow this steps to be in the development mode:

- On your terminal; go to the root of the `frappe` project
- Use the following command
  `bench --site name.of.your.site set-config --global developer_mode 1`

Source:

- https://frappeframework.com/docs/user/en/basics/doctypes
- https://frappeframework.com/docs/user/en/tutorial/create-a-doctype

### Creating a docType

Now we are going to create our first `docType` for our `library` project and we follow the next steps to do it:

- On your terminal; go to the root of the `frappe` project
- Use the `start` command to run your local server
  `bench start`
- On your browser; go to the `login` page
- Login with the `admin` user
- On the `Shortcuts` section click on the `DocType` options
- You will see a list of all `docTypes` that you have available(This are `docTypes` that are created by default when you created your `app`)
- Click on the `Add DocType` button
- You will see the `New DocType` form
- Add `Article` as the `docType` name and click on the `Module` input to see a dropdown
- On the dropdown choose the name of your custom `app`
- Now get to the `Fields` section and click `Add Row`
- Put `Article Name` as the label and `Data` as its `type`
- Add the following `fields` using the same process as the `Article Name`
  <!-- prettier-ignore-start -->

  |    Label    |     Type     |     Options      |
  | :---------: | :----------: | :--------------: |
  |    Image    | Attach Image |                  |
  | Description | Text Editor  |                  |
  |    ISBN     |     Data     |                  |
  |   Status    |    Select    | Issue, Available |
  |  Publisher  |     Data     |                  |

  <!-- prettier-ignore-end -->

- Click on the `Save` button at the top below the navbar
- You should redirect to the `Article docType` page
- Click on the `Go to Article List` button at the top
- You should be redirected to the `Article` list page(But at this moment we don't have any `Articles`)
- Now we need to clean the `cache` so click on the `refresh` button at the top
- Now Click on the `Create your first Article` button
- You should see a form that represents the `Article`
- Fill the inputs with some test information and click on the `Save` button at the top
- The `Article` should be created without any issues

Source: https://frappeframework.com/docs/user/en/tutorial/create-a-doctype

### What happened when we created the Article docType?

- First; on the database a table called `tabArticle` was created with the `fields` that we specified before. You can check this navigating into `MariaDB` using the terminal and `bench` have some commands that can help us:
  - On your terminal; go to the root of the `frappe` project
  - Use the following command to get into the `MariaDB` console
    `bench --site name.of.your.site mariadb`
  - On the `MariaDB` console type the following
    `desc tabArticle;`
    This will show you all the `fields` of the `tabArticle`. You will see all the `fields` that you created plus some that are created by default with every `docType`. Something important is that the `name field` will be the `primary key` column
  - Now use the following to see the record that you created before
    `select * from tabArticle;`
    This will `select` all `articles` that you created before but we just got one entry so it will show one. As you see the `name field` have the same content that you saw as the `name` of the `article` in the `admin`
- Then; a number of views were also created for the `doctype` like the `list view` that will have the `list` of all `articles` and the `form view` that will `create` new `article` or `view` an existing one
- Also; the `form layout` of the inputs are created according to the `fields` that you created before when you create the `article docType`
- Finally; you will see that on the `apps/my_custom_app` there are a bunch of new files added to your custom `app`. These files describe everything about the new `docType` on which you can see:
  - `article.json`: `JSON` file that define the `docTypes` attributes
  - `article.js`: `Client-side` controller for the `form view`
  - `article.py`: `Python` controller for `articles`
  - `test_article.py`: `Python` unit test boilerplate

Source: https://frappeframework.com/docs/user/en/tutorial/create-a-doctype

### DocType features

At this moment we can begin to customize the `article docType` that we created before so we can have a better experience using the UI.

### Naming

As you may notice the `names` on the `articles` that you created before are just a random `hash` generated automatically but we actually want the actual `article name` to be presented. Here is the step to do that:

- On your terminal; go to the root of the `frappe` project and start your local server using:
  `bench start`
- Go to the `login` page on your browser and access it with your account
- Click on the `DocType` button in the `Shortcut` section
- Choose the `Article docType`
- Scroll down to the `Naming` section
- On the `Auto Name` input add the following:
  `field:article_name`
  This will use the data of the `article name` field
- Click on the `save` button
- Click on the `Go to Article List` button at the top
- Create a new `article` and save it(Make sure that you fill the `article name` input)
- You should see that the new `article` on the list use the `article name field` data

Source: https://frappeframework.com/docs/user/en/tutorial/doctype-features

### Form Layout

Now we are going to make changes to the spacing of the `form view` of the `articles`

- Go to the `Article docType`
- Scroll to the `fields` section
- Click on the `Add Row` button
- Click on the `type` of the new column and choose `Column Break`(make sure that the label is empty)
- Move the new column below the `Article Name`
- Move the `Author` and `ISBN` rows to be before the `Column Break`
- Click on the `Add Row` button
- Click on `type` of the new row and choose `Section Break`
- Move the `Description` bellow of the `Section Break` row
- Click on the Save button
- Go to the `Article` list and choose an `article`
- You should see that the layout of the `form view` change and the `Author` and `ISBN` are on the same `column` and the `publisher` and `status` on the other. Also, the `Description` is in another `section`

Source: https://frappeframework.com/docs/user/en/tutorial/doctype-features

### Form settings

Now we want to show the `image` at the top left of the `form view` and activate the `rename` option for this file.

- Go to the `Article docType`
- Scroll down to the `Form Settings` section
- On the `Image Field` input add `image`(Name of the `field` that we created before)
- On the checkboxes at the left choose the `Allow Rename`
- Click the save button
- Go to the `article` list and choose one of the `articles`
- You should see the `image` to the top left of the `form view`
- Click on the `...` button
- You should see a `rename` option

### Permission

Finally; we are going to create some `roles` that restrict some functionality of a `docType` in this case the `Article` that we created before.

- Go to the `Article docType`
- Scroll down to the `Permission Rules` section
- Click on `Add Row`
- On the `Role` field add `Librarian`
- A dropdown should popup
- Choose the `Create new role` option
- Click save
- Leave all mark check
- Follow the same steps to create a `Library Member role`
- Just leave the `Read` check on that new `role`
- Click on the Save button

### Note:

All those changes that we did will be reflected on the `article.json` file inside of the `doctype` directory so after performing all those changes you will need to commit those changes
