## Heroku Deploy ⚕️

**Notes** 📝
1. Generate all your private files from h-code branch (rclone.conf) since the generators not available in heroku branch but you should add the private files in heroku branch not in master or use variables links in `config.env`.
2. Add variables in heroku Environment.
3. Don't deploy using hmanager or github integration.
4. After that u should add fill `UPSTREAM_REPO` of your fork and `UPSTREAM_BRANCH` to `h-code`.
5. Now, Wait for your Bot to Get Ban !! Have a Healthy Day !!

------

## Deploy With Github Workflow

1. Go to Repository Settings -> Secrets

![Secrets](https://telegra.ph/file/9d6ed26f8981c2d2f226c.jpg)

2. Add the below Required Variables one by one by clicking New Repository Secret every time.

   - HEROKU_EMAIL: Heroku Account Email Id in which the above app will be deployed
   - HEROKU_API_KEY: Your Heroku API key, get it from https://dashboard.heroku.com/account
   - HEROKU_APP_NAME: Your Heroku app name, Name Must be unique

![Steps from 1 to 3](https://telegra.ph/file/2a27cf34dc0bdba885de9.jpg)

![Step 4](https://telegra.ph/file/fb3b92a1d2c3c1b612ad0.jpg)

![Step 5](https://telegra.ph/file/f0b208e4ea980b575dbe2.jpg)

3. Remove commit id from raw link to be able to change variables without updating the CONFIG_FILE_URL in secrets. Should be in this form: https://gist.githubusercontent.com/username/gist-id/raw/config.env
   - Before: https://gist.githubusercontent.com/anasty17/8cce4a4b4e7f4ea47e948b2d058e52ac/raw/19ba5ab5eb43016422193319f28bc3c7dfb60f25/config.env
   - After: https://gist.githubusercontent.com/anasty17/8cce4a4b4e7f4ea47e948b2d058e52ac/raw/config.env

4. After adding all the above Required Variables go to Github Actions tab in your repository.
   - Select Manually Deploy to Heroku workflow as shown below:

![Select Manual Deploy](https://telegra.ph/file/cff1c24de42c271b23239.jpg)

5. Choose `heroku` branch and click on Run workflow

![Run Workflow](https://telegra.ph/file/f44c7465d58f9f046328b.png)

---

## Deploy Guide By [Anasty17](https://github.com/anasty17/)

---
