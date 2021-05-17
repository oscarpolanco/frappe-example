# Frappe framework tutorial

This will be a example project inspire on the `tutorial` of the [frappe docs](https://frappeframework.com/docs)

## Pre-requisites

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

### Installation process(pre-requisites, macOs)

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

## Run this example locally

Here are the steps to run this example locally

### Creating the frappe directory

- On your terminal go to the path that you want to store this directory
- Use the `bench init` command with the name of your project
  `bench init name_of_the_project`
- A directory with the name that you specify before will be created

### Add the app to the frappe project

- On your terminal; go to the root of the `frappe` project that you just added before
- Use the `get-app` to get the `app` that we create on this example
  `bench get-app frappe_example git@github.com:oscarpolanco/frappe_example.git`
- You should have a `frappe_example` directory that is our custom `app`

### Create your site for the custom app and run the project

- On your terminal; go to the root of the `frappe` project that you just added before
- Use the `new-site` command to create your new `site`
  `bench new-site name.of.your.site`
- Since a database is created you will need to type your `mysql` password
- Add your `admin` password
- You should see that a new directory is created on the `sites` folder with the same name that you use on the `new-site` command
- Install our custom `app` on your `site` using the following command
  `bench --site name.of.your.site install-app frappe_example`
- On the root of the `frappe` project run the `start` command
  `bench start`
- On your browser go to `http://localhost:8000/`
- You should be redirected to the `login` page
- Log in with the `admin` user(the default user is `Administrator` and the password is the one that you defined when you created the new `site`)
