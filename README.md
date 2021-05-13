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
