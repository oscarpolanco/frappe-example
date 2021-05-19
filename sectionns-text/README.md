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

## Controller methods

A `controller` is a normal `python` class that extends from `frappe.model.Document` and it handles how the values load from the database, how they are parsed and save back to the database.

In this section, we will create a new `doctype` to add one little function as an example of a `controller` so let get to it!!

- On your terminal; go to the root of the `frappe` project
- Use the `start` command to run your local server(Remember that you need to be on development mode to create a new `doctype`)
- On your browser go to the `login` page
- Login with your `admin` account
- On the `Shortcut` section choose `DocType`
- Click on the `Add DocType` button
- On the `Name` input add `Library Member`
- Click on the `Module` input
- A dropdown should popup
- Choose your `app`
- Scroll down to the `Fields` section
- Add the following rows:
  <!-- prettier-ignore-start -->

  |     Label     | Type |
  | :-----------: | :--: |
  |  First Name   | Data |
  |   Last Name   | Data |
  |   Full Name   | Data |
  | Email Address | Data |
  |     Phone     | Data |

  <!-- prettier-ignore-end -->

  On the `Full Name field`; click on the `edit` button and scroll to the `Permission` checkbox and check `Read Only`

- Click the save button
- Go to the `Library Member` list
- Click on the `refresh` button at the top
- Click on the `Create your first List Member`
- You will see that the `Full Name field` is not on the form. This is because is a `read-only field`
- Now go to your editor
- On your `app` directory inside of the `doctype` folder should be a new `library_member` directory
- Go to the `library_member.py` file inside of the `library_member` directory
- Delete `pass`
- Add the following function
  ```python
  class LibraryMember(Document):
    def before_save(self):
      self.full_name = f'{self.first_name} {self.last_name or ""}'
  ```
  We use the `before_save` method that will run every time a document is saved, you can see more on these hooks on [this page](https://frappeframework.com/docs/user/en/basics/doctypes/controllers), and the function will fill the `full_name field` with the concatenation of the `first_name` and `last_name`
- Go back to the `Library Member` list and create a new `Library Member`
- You should create the `Library Member` without issue and will see the `full name field` with the correct information

## Types of DocTypes

Now we are going to check different `docType` that can be used on `frappe` and some more logic to validate the data that we use on the different `controllers` of the `docTypes`.

### Linked DocTypes

The `linked docTypes` are the ones that are linked to other `docTypes` with `link fields`. We can classify into 2 types are `master` and `transitional` based on the type of data that will store; for example, the `Article` and `Library Member` are `master docTypes` because they represent an entity. We don't have any `transitional doctype` yet but we will work on some beginning on this section like the `Library Membership` that will the data related to the `membership` of a previously created `member` so its data will depend on the `Library Member docType` that is why is `transitional`.

Source: https://frappeframework.com/docs/user/en/tutorial/types-of-doctype#linked-doctypes

### Submittable DocType

Before continuing to creating the actual example of this `docTypes` we need to continue checking some definitions like the `submittable DocType` that is considered like this when you enable the option `Is Submittable` and this will enable 3 states on the `docType`:

- `Draft`: This state will allow you to continue updating the document
- `Submitted`: When you `submit` the document any `field` cannot be change
- `Cancelled`: After `submitting` a document you can `cancel` it that will make invalid that document but won't delete it

When you create a `submittable DocType` on the `fields` section you will see that an extra `field` is created `Amended From` automatically and this `field` is take action when you `cancel` a document from that moment that document can only be `amended` that means that it can be duplicated and the `cancel` document will be related to the new one via this `field`

### Creating the Library Membership docType and add validation to it controller

- On your terminal; go to the root of the `frappe` project and run your local server
- On your browser; go to the `login` page
- Login with a valid `admin` user
- On the `Shortcut` section; choose the `DocType` option
- Click on the `Add DocType` button at the top
- On the `Name` input add `Library Membership`
- Click on the `Module` input
- A dropdown should popup
- Choose your `app`
- Click the `Is Submittable` checkbox that is below the `Module` input. This will make the `Library Membership` a `submittable DocType`
- Scroll to the `fields` section
- Add the following `fields`
  <!-- prettier-ignore-start -->

  |     Label      | Type  | Mandatory |    Options     |                                 Edit                                 |
  | :------------: | :---: | :-------: | :------------: | :------------------------------------------------------------------: |
  | Library Member | Link  |     ✔     | Library Member |                                                                      |
  |   Full Name    | Data  |           |                | Check Read Only, Fetch form textarea add: `library_member.full_name` |
  |   From Date    | Date  |           |                |                                                                      |
  |    To Date     | Date  |           |                |                                                                      |
  |      Paid      | Check |           |                |                                                                      |

  <!-- prettier-ignore-end -->

- On the `Naming` section put `LMS.#####` to the `Auto Name` input. Putting the `auto name` this way you `name` of each entry will have the `LMS` prefix and the `#` will be replaced by numbers that will begin in `000001` for the first entry and will increment itself on every new entry
- Go to the `View Settings` section and on the `Title Field` put `full_name`
- Go to the `Permission` section and add the `Librarian` role
- Click on the Save button at the top

As you can see the `Library Member` is similar to a `foreign key` on other frameworks and it will let you link the value to a record of another `docType`. Also the `Full Name field` is fetched from the `Library Member docType`.

- Go to the `Library Membership` list
- Click on the `Create your first library membership` button
- Click on the `Library Member` input
- A dropdown with some `Library Members` should popup(If you don't have any go a create one)
- Choose one of them
- You should see that the `Full Name` input fill itself
- Fill the other `fields` and click save
- You will see that the document is on `draft` mode
- Click the `submit` button and you should see that the entry is added without errors

#### Controller validation for the membership

Now we will be adding some code to make sure that whoever is added to a `membership` doesn't have an active one yet.

- On your editor; go to the `apps/my_custom_app/` directory on the `frappe` project
- In the `doctype/library_membership` directory; open the `library_membership.py` file
- Uncomment the `import frappe` line
- Delete `pass` on the `LibraryMembership` class
- Add a function call `before_submit` that recive `self`
  ```python
  class LibraryMembership(Document):
    def before_submit(self):
  ```
  The `before_submit` method as we mentioned before is a hook that will run before we `submit` the data of our document
- Create a variable call `exists` that it value will be `exists` method from `frappe.db`
  ```python
  class LibraryMembership(Document):
    def before_submit(self):
      exists = frappe.db.exists()
  ```
  The `exists` method is a filter provided by `frappe` that will help us to determinine if a specific entry exists
- Add the following as parameters of the `exists` filter
  ```python
  class LibraryMembership(Document):
    def before_submit(self):
      exists = frappe.db.exists(
        "Library Membership",
        {
          "library_member": self.library_member,
          "docstatus": 1,
          "to_date": (">", self.from_date),
        },
      )
  ```
  This will use the data of the `Library Membership docType` and search for the current `member` that you are trying to make the new `membership`; making sure that the document exists and the `date` is bigger than the current `date` that you are using
- Add an `if` that check if the `exists` variable has a value and if it does throw a message for the user

  ```python
  class LibraryMembership(Document):
    def before_submit(self):
      exists = frappe.db.exists(
        "Library Membership",
        {
          "library_member": self.library_member,
          "docstatus": 1,
          "to_date": (">", self.from_date),
        },
      )

      if exists:
        frappe.throw("There is an active membership for this member")
  ```

- Now go back to the `Library Membership` on your browser and try to do a `membership` for a `member` that already have one
- You should see a modal with the message that you added before on the `controller`

### Library transaction docType and validation

At this moment we can begin to work with a `docType` that represents the `transaction` that will record that is `issue` or `return` of an `article` by a `member`.

- On your terminal; go to the root of the `frappe` project and start your local server
- Go to the login page and log in as `Administrator`
- On the `shortcut` section; choose `DocType`
- Click on the `Add DocType` button
- On the `name` input add `Library Transaction`
- Click on the `Module` input
- You should see a dropdown popup
- Choose your `app`
- Check the `Is Submittable` checkbox
- Co to the `Fields` section and add the following
  <!-- prettier-ignore-start -->

  |     Label      |  Type  |      Name      | Mandatory |    Options     |
  | :------------: | :----: | :------------: | :-------: | :------------: |
  |    Article     |  Link  |    Article     |     ✔     |    Article     |
  | Library Member |  Link  | library_member |     ✔     | Library Member |
  |      Type      | Select |      type      |     ✔     |  Issue Return  |
  |      Date      |  Date  |      date      |           |                |

  <!-- prettier-ignore-end -->

- Go to the `Naming` section and add in the `Auto Name` input `LT.#####`
- Go to the `Permission` section and add the `Librarian` role
- Click on the Save button at the top

#### Validation for the transaction

Now we will continue adding some validations that will set the `articles` status depending on the `transaction` and we will control if the one that makes the `transaction` is a valid member also depending on the status of that `article` we will permit that the `transaction` continue

- On your editor; go to the `apps/my_custom_app/doctype/library_transaction/` directory
- Open the `library_transaction.py`
- Uncomment the `import frappe`
- Add the `before_submit` method
  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
  ```
- Add the following condition for the `transaction` that have the `type` equals to `Issue`
  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
      if self.type == "Issue":
        self.validate_issue()
        article = frappe.get_doc("Article", self.article)
        article.status = "Issue"
        article.save()
  ```
  This condition will catch every `transaction` that have the `type Issue` and will run the `validate_issue`(We will make this function in a bit) that will check if the `article` is not `issued` by another member them if it not `issued` we will get the `article` and change its status to `Issue` and will `save` the update
- Now add another condition for the `Return type` with the following content

  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
      if self.type == "Issue":
        self.validate_issue()
        article = frappe.get_doc("Article", self.article)
        article.status = "Issue"
        article.save()

      elif self.type == "Return":
        self.validate_return()
        article = frappe.get_doc("Article", self.article)
        article.status = "Available"
        article.save()
  ```

  This condition will check if the `transaction` has the `Return type` and if it does it will run the `validate_return`(we will make this function in a little bit) that will check if the `article` already have the `Available` status that means that we can't return something that is not being `issued` before then if it doesn't have the `available` status will get the actual `article` and set it status as `Available` and finally `save` the update

- Then we can begin with the `validate` functions. First with the `validate_issue` function

  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
      if self.type == "Issue":
        ...

      elif self.type == "Return":
        ...

      def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        if article.status == "Issue":
          frappe.throw("Article is already issued by another member")
  ```

  Here we will run the `validate_membership`(We will make this function in a bit) to know if the one that is issuing a `transaction` has a valid `membership` and if it does we get the actual `article` and check if the status is `Issue` throwing a message if the `article` is already been issue by another `member`

- Now create a `validate_return` function with the following

  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
      if self.type == "Issue":
        ...

      elif self.type == "Return":
        ...

      def validate_issue(self):
        ...

      def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        if article.status == "Available":
          frappe.throw("Article cannot be returned without being issued first")
  ```

  For this function, we will check the status of the `article` to see if is `Available` that will mean that we can't continue with the `transaction`

- Finally, make the `validate_membership` function with the following

  ```python
  class LibraryTransaction(Document):
    def before_submit(self):
      if self.type == "Issue":
        ...

      elif self.type == "Return":
        ...

      def validate_issue(self):
        ...

      def validate_return(self):
        ...

      def validate_membership(self):
        valid_membership = frappe.db.exists(
          "Library Membership",
          {
            "library_member": self.library_member,
            "docstatus": 1,
            "from_date": ("<", self.date),
            "to_date": (">", self.date),
            },
          )

        if not valid_membership:
          frappe.throw("The member does not have a valid membership")
  ```

  As we did before we will check if is an actual `member` that is issuing the `transaction`

Now that you are aware of the different conditions of the `transaction` so try to test creating different `transactions` that match all cases.

### Single DocTypes

A `single doctype` is like a single record of data; it will not create a table on the database; it will store all single values on a table called `tabSingle` that is usually used for global settings. In our case, we will create a `single doctype` to control the maximum time that a `loan` should last and the maximum of `articles` that a `member` can `issue`.

#### Creating the library settings doctype

- On your terminal; go to the root of the `frappe` project and start your local server
- On your browser; go to the login page and log in to the `admin` user
- On the `Shortcut` section choose `DocType`
- Click on the `Add DocType` button
- On the `Name` input add `Library Settings`
- Click on the `Module` input and a dropdown should popup
- Choose your `app`
- Check the `Is Single` checkbox below the `module` input
- Scroll to the `Fields` section and add the following
  <!-- prettier-ignore-start -->

  |               Label               | Type |     Name     |
  | :-------------------------------: | :--: | :----------: |
  |            Loan Period            | Int  |              |
  | Maximum Number of Issued Articles | Int  | max_articles |

  <!-- prettier-ignore-end -->

- Click on the Save button at the top
- Now click on the `Go to library settings` button at the top
- Now you should see only the `form view` of the `library settings` not a list. Add the values that you want and save
- The values should be added without any errors

#### Validation for library settings

Now we will make some `validations` function that use the `library settings` values to prevent some `transactions` and to automatically add the `to_date field` of the `membership` on submission

- On your `apps` directory; go to the `library_membership.py`
- At the bottom of the `before_submit` method add the following
  ```python
  loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
  	self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)
  ```
  We will use the `get_single_value` method to obtain the `loan_period` of the `Library Settings` and assign it to the `loan_period` variable then use the `add_days` to calculate the `date` for the `to_date field` using the `from_date field` and the `loan_period` or `30` days. This will automatically put the `date` on `submit`
- Go to the `Library Membership` list and add a new entry(Do not fill the `to_date` input) and submit
- The `to_date field` should be fill when you submit the data
- Now get back to your editor and go to the `library_transaction.py`
- On the `before_submit` method create a new function call `validate_maximum_limit` with the following content
  ```python
  def validate_maximum_limit(self):
  	max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
  	count = frappe.db.count(
  		"Library Transaction",
  		{"library_member": self.library_member, "type": "Issue", "docstatus": 1},
  	)
  	if count >= max_articles:
  		frappe.throw("Maximum limit reached for issuing articles")
  ```
  Here as we did before we are going to obtain the `max_articles field` from `Library Settings` then we will `count` how many `articles` the current `member` have the type `Issue` and finally compare if we have more `Issue articles` that the maximum that we can have

Now test the conditions that you just saw for the `transactions` on the `admin`.

## Form scripts

A `form script` lets you add client-side logic on the `form views` to automatically fetch values, add validations and add contextual actions.

When you create a new `doctype` a `js` file with will be created on the `doctype` directory with the same name of that `doctype`. You will have some to add your code using the following syntax:

```js
frappe.ui.form.on(doctype, {
  event1() {
    // handle event 1
  },
  event2() {
    // handle event 2
  },
});
```

[Here](https://frappeframework.com/docs/user/en/api/form) you have some more deep information about `form scripts`.

Let's create a little example for our custom `app`. Imagine that you create a `member` then you will need a `membership` for that `member` so you will need to go first; to the `member` list to create it; then to the `membership` list to create it and if you want to add a `transaction` you will need to follow the same steps and that are a lot of steps that a user follows but we can make it a little easier using `form scripts`.

- On your editor; go to your custom `app` directory
- In there go to the `doctype/library_member/` directory and open the `library_member.js`
- On that file; uncomment the `refresh` function
- Add the following
  ```js
  frappe.ui.form.on('Library Member', {
    refresh: function (frm) {
      frm.add_custom_button('Create Membership', () => {
        frappe.new_doc('Library Membership', {
          library_member: frm.doc.name,
        });
      });
    },
  });
  ```
  We use the `add_custom_button` of the `frm` object to create a button with the message `Create Membership` and send a callback function that using the `frappe.new_doc` method create a new `Library Membership` instantce sending the current `member` name
- Now we will do the same with the `transaction`
  ```js
  frappe.ui.form.on('Library Member', {
    refresh: function (frm) {
      frm.add_custom_button('Create Membership', () => {
        frappe.new_doc('Library Membership', {
          library_member: frm.doc.name,
        });
      });
      frm.add_custom_button('Create Transaction', () => {
        frappe.new_doc('Library Transaction', {
          library_member: frm.doc.name,
        });
      });
    },
  });
  ```
- On your terminal; go to the root of the `frappe` project and start your local server
- Go to the login page and log in as an `admin`
- Go to the `member` list page
- Choose one of the `members` that you already created
- You will see 2 buttons at the top right one for creating `membership` and the other for creating `transaction`
- Click on both buttons and you will see that you are redirected to the respective `form view` page with the name of the `member` put automatically on the name input

Sources:
https://frappeframework.com/docs/user/en/tutorial/form-scripts
https://frappeframework.com/docs/user/en/api/form
